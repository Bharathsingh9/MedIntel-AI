import os
from dotenv import load_dotenv

# Load env variables from .env
load_dotenv()

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq

class LLMProvider:
    @staticmethod
    def get_llm(provider="groq"):
        if provider == "gemini":
            return ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.3)
        elif provider == "openai":
            return ChatOpenAI(model="gpt-3.5-turbo", temperature=0.3)
        elif provider == "groq":
            return ChatGroq(model="llama-3.3-70b-versatile", temperature=0.3)
        elif provider == "ollama":
            raise NotImplementedError("Ollama provider requires a local server.")
        else:
            raise ValueError(f"Unknown provider: {provider}")
