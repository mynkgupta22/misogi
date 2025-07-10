"""
Configuration settings for the Medical RAG system.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base Paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
EVALUATION_DATA_DIR = DATA_DIR / "evaluation"

# Create directories if they don't exist
for dir_path in [RAW_DATA_DIR, PROCESSED_DATA_DIR, EVALUATION_DATA_DIR]:
    dir_path.mkdir(parents=True, exist_ok=True)

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-ada-002")
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4-1106-preview")
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.0"))
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "500"))

# Vector Database Configuration
CHROMA_PERSIST_DIRECTORY = os.getenv("CHROMA_PERSIST_DIRECTORY", "./data/chroma_db")

# API Configuration
API_HOST = os.getenv("API_HOST", "localhost")
API_PORT = int(os.getenv("API_PORT", "8000"))

# Monitoring Configuration
PROMETHEUS_PORT = int(os.getenv("PROMETHEUS_PORT", "9090"))

# RAGAS Evaluation Thresholds
FAITHFULNESS_THRESHOLD = 0.90
CONTEXT_PRECISION_THRESHOLD = 0.85

# Chunking Configuration
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# Query Types
QUERY_TYPES = {
    "DRUG_INTERACTION": "drug_interaction",
    "TREATMENT_PROTOCOL": "treatment_protocol",
    "DIAGNOSIS_GUIDELINES": "diagnosis_guidelines",
    "GENERAL_MEDICAL": "general_medical"
}

# System Messages for Different Query Types
SYSTEM_MESSAGES = {
    QUERY_TYPES["DRUG_INTERACTION"]: """You are a medical AI assistant specialized in drug interactions. 
    Provide accurate information about drug interactions based on the provided medical literature. 
    Always include relevant citations and safety warnings.""",
    
    QUERY_TYPES["TREATMENT_PROTOCOL"]: """You are a medical AI assistant specialized in treatment protocols. 
    Provide evidence-based treatment guidelines based on the provided medical literature. 
    Always include relevant citations and standard of care considerations.""",
    
    QUERY_TYPES["DIAGNOSIS_GUIDELINES"]: """You are a medical AI assistant specialized in diagnostic guidelines. 
    Provide evidence-based diagnostic criteria and procedures based on the provided medical literature. 
    Always include relevant citations and differential diagnosis considerations.""",
    
    QUERY_TYPES["GENERAL_MEDICAL"]: """You are a medical AI assistant providing general medical information. 
    Provide accurate, evidence-based information based on the provided medical literature. 
    Always include relevant citations and appropriate medical disclaimers."""
} 