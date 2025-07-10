from pydantic import BaseModel
from typing import Dict, Optional

class Settings(BaseModel):
    APP_NAME: str = "SaaS Support System"
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    CHROMA_PERSIST_DIR: str = "./data/chroma"
    MAX_QUEUE_SIZE: int = 100
    MODEL_NAME: str = "llama2"
    OPENAI_API_KEY: Optional[str] = None
    
    # Intent classification thresholds
    INTENT_CONFIDENCE_THRESHOLD: float = 0.7
    
    # Vector store settings
    VECTOR_STORE_SETTINGS: Dict = {
        "technical": {
            "collection_name": "technical_docs",
            "distance_func": "cosine"
        },
        "billing": {
            "collection_name": "billing_docs",
            "distance_func": "cosine"
        },
        "feature": {
            "collection_name": "feature_docs",
            "distance_func": "cosine"
        }
    }

settings = Settings() 