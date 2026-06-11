# 🧬 MedIntel AI

> **Explainable Multi-Disease Prediction & Health Analytics Platform**

MedIntel AI is a production-grade healthcare analytics platform that leverages Machine Learning, Explainable AI (SHAP/LIME), and Retrieval-Augmented Generation (RAG) to provide interpretable health risk assessments, biological age estimations, and actionable lifestyle recommendations.

## ✨ Core Features

* **🩺 Multi-Disease Risk Prediction:** Optimized ML pipelines predicting Diabetes, Heart Disease, Kidney Disease, and Stroke risks using complex patient biomarker data.
* **🧠 Explainable AI:** Full transparency into ML predictions using SHAP and LIME, ensuring clinical interpretability and trust for healthcare providers.
* **📈 Advanced Health Scoring:** Dynamic algorithms calculating Biological Age, Overall Health Index, and generating interactive health simulations.
* **🤖 RAG Health Assistant:** An embedded, context-aware clinical AI Consultant powered by Groq LLaMA 3 and a local FAISS vector database holding specific medical guidelines.
* **📊 Analytics Dashboard:** A blazing-fast, responsive React dashboard built with Vite, TypeScript, Tailwind CSS, Shadcn UI, and Recharts.

## 🛠️ Technology Stack

**Frontend Architecture:**
* React 18 & TypeScript
* Vite (Build Tool)
* Tailwind CSS & Shadcn UI (Styling & Components)
* Zustand (State Management)
* Recharts (Data Visualization)

**Backend & ML Architecture:**
* FastAPI (Python web framework)
* Scikit-learn, CatBoost (Predictive Modeling)
* SHAP & LIME (Explainability Engines)
* LangChain, FAISS, SentenceTransformers (RAG Pipeline)
* Groq LLaMA 3 API (LLM Inference)

## 🚀 Local Development Setup

### Prerequisites
* Python 3.10+
* Node.js 18+
* [Groq API Key](https://console.groq.com/) for the AI Assistant

### 1. Clone the Repository
```bash
git clone https://github.com/Bharathsingh9/MedIntel-AI.git
cd MedIntel-AI
```

### 2. Backend Setup
```bash
# Install Python dependencies
pip install -r requirements.txt

# Create an environment file for your API Keys
echo "GROQ_API_KEY=your_api_key_here" > .env

# Start the FastAPI Server
python -m uvicorn backend.main:app --reload
```
*The backend API will be available at `http://127.0.0.1:8000`*

### 3. Frontend Setup
```bash
cd frontend-v2

# Install Node dependencies
npm install

# Start the Vite Development Server
npm run dev
```
*The frontend dashboard will be available at `http://localhost:5173`*

## 📁 Repository Structure
```
MedIntel-AI/
├── ai_assistant/        # RAG pipeline, LLM Provider, FAISS integration
├── analytics/           # Data Quality & Exploratory Data Analysis Scripts
├── backend/             # FastAPI entrypoints, routers, and DB schemas
├── data/                # Synthetic healthcare dataset generators
├── explainability/      # SHAP & LIME engines
├── frontend-v2/         # React + Vite UI Dashboard
├── health_scoring/      # Biological Age and Health Index algorithms
├── knowledge_base/      # Markdown clinical guidelines for RAG retrieval
├── ml/                  # Model training and inference pipelines
├── reports/             # Auto-generated EDA charts and evaluation metrics
└── requirements.txt     # Python dependencies
```

## 🔒 Security & Privacy
This platform is designed as a modern analytics showcase. The repository's `.gitignore` explicitly blocks `.env` secrets, large vector databases, and cache folders from being pushed.

## 📄 License
This project is licensed under the MIT License.
