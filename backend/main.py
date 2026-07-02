from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.database import database, models
from backend.routes import predict
from ai_assistant.api import chat_routes

# Create DB Tables
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="MedIntel AI API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(predict.router, prefix="/api")
app.include_router(chat_routes.router, prefix="/api")

@app.get("/")
def health_check() -> dict:
    return {"status": "MedIntel AI Backend is running"}
