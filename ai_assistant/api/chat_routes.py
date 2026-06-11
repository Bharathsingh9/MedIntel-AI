import os
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional

from ai_assistant.services.chat_service import ChatService

router = APIRouter()

# Initialize Chat Service Singleton
KB_PATH = "D:\\health-analytics-ai\\knowledge_base"
INDEX_PATH = "D:\\health-analytics-ai\\ai_assistant\\faiss_index"
try:
    chat_service = ChatService(kb_path=KB_PATH, index_path=INDEX_PATH, llm_provider="groq")
except Exception as e:
    print(f"Failed to initialize ChatService: {e}")
    chat_service = None

class ChatRequest(BaseModel):
    message: str
    patient_state: Optional[Dict[str, Any]] = None

class ChatResponse(BaseModel):
    answer: str

@router.post("/chat", response_model=ChatResponse)
def handle_chat(request: ChatRequest):
    if not chat_service:
        raise HTTPException(status_code=500, detail="Chat Service unavailable (missing API keys or FAISS index).")
    
    try:
        answer = chat_service.answer_question(request.message, request.patient_state)
        return ChatResponse(answer=answer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
