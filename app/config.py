import os
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    telegram_bot_token: str = ""
    webhook_path: str = "/telegram/webhook"
    base_url: str = ""
    
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama3.2"
    ollama_temperature: float = 0.0
    
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    
    faiss_index_dir: str = "faiss_index"
    
    docs_path: str = "data"
    
    port: int = 8000
    
    rag_k_documents: int = 3
    chunk_size: int = 800
    chunk_overlap: int = 100
    
    class Config:
        env_file = ".env"
        case_sensitive = False

@lru_cache()
def get_settings() -> Settings:
    return Settings()
