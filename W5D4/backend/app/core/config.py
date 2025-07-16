from typing import Optional
from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = "Research Assistant"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "your-secret-key-here"  # Change in production
    
    # Database
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "research_assistant"
    SQLALCHEMY_DATABASE_URI: Optional[str] = None

    # Vector Store
    QDRANT_HOST: str = "localhost"
    QDRANT_PORT: int = 6333
    
    # LLM
    GROQ_API_KEY: str = ""
    
    # Integrations
    NOTION_TOKEN: str = ""
    NOTION_DATABASE_ID: str = ""
    SLACK_TOKEN: str = ""
    SLACK_CHANNEL_ID: str = ""
    TEAMS_WEBHOOK_URL: str = ""

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()

# Construct database URI
if settings.SQLALCHEMY_DATABASE_URI is None:
    settings.SQLALCHEMY_DATABASE_URI = (
        f"postgresql+asyncpg://{settings.POSTGRES_USER}:"
        f"{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_SERVER}/{settings.POSTGRES_DB}"
    ) 