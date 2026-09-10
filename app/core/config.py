import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Charger les variables d'environnement depuis le fichier .env
load_dotenv(override=True)

class Settings(BaseSettings):
    PROJECT_NAME: str = "LAFIYA Platform"
    API_V1_STR: str = "/api/v1"
    
    SECRET_KEY: str = os.getenv("SECRET_KEY", "super_secret_jwt_key_to_change_in_production")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7 # 7 days
    
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./lafiya.db")
    
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "gsk_placeholder")
    GROQ_MODEL: str = os.getenv("GROQ_MODEL", "qwen/qwen3.6-27b")

settings = Settings()
