import os
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from ai_assistant.rag.vector_store import VectorDBManager
from ai_assistant.llm.provider import LLMProvider
from ai_assistant.prompts.system_prompt import HEALTH_ASSISTANT_PROMPT

class ChatService:
    def __init__(self, kb_path: str, index_path: str, llm_provider: str = "gemini"):
        # Initialize Vector DB
        self.vector_db = VectorDBManager(kb_path, index_path)
        self.retriever = self.vector_db.get_retriever(k=3)
        
        # Initialize LLM
        self.llm = LLMProvider.get_llm(llm_provider)
        
        # Build RAG Chain
        self.question_answer_chain = create_stuff_documents_chain(self.llm, HEALTH_ASSISTANT_PROMPT)
        self.rag_chain = create_retrieval_chain(self.retriever, self.question_answer_chain)

    def format_patient_context(self, state: dict) -> str:
        """Converts the raw patient biomarker and prediction state into a readable string for the LLM."""
        if not state:
            return "No patient context available. Provide general medical information."
            
        context = []
        if 'patientData' in state:
            d = state['patientData']
            context.append(f"Biomarkers: Age {d.get('age')}, BMI {d.get('bmi')}, BP {d.get('systolic_bp')} mmHg, "
                           f"Glucose {d.get('fasting_glucose')} mg/dL, HbA1c {d.get('hba1c')}%, "
                           f"Smoking: {d.get('smoking_status')}.")
        if 'predictionResult' in state:
            p = state['predictionResult']
            if p:
                context.append(f"ML Risk Predictions: Diabetes {p.get('diabetes_risk')}%, "
                               f"Heart {p.get('heart_risk')}%, Stroke {p.get('stroke_risk')}%, "
                               f"Kidney {p.get('kidney_risk')}%.")
                context.append(f"Health Intelligence: Overall Score {p.get('overall_health_score')}/100 "
                               f"({p.get('health_category')}), Bio-Age {p.get('biological_age')} years.")
                           
        return "\n".join(context)

    def answer_question(self, question: str, patient_state: dict = None) -> str:
        patient_context_str = self.format_patient_context(patient_state)
        
        # Run RAG
        response = self.rag_chain.invoke({
            "input": question, # Used by the retriever under the hood
            "question": question, # Used by our prompt template
            "patient_context": patient_context_str
        })
        
        return response["answer"]
