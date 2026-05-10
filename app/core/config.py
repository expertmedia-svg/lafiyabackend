import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "LAFIYA Platform"
    API_V1_STR: str = "/api/v1"
    
    SECRET_KEY: str = os.getenv("SECRET_KEY", "super_secret_jwt_key_to_change_in_production")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7 # 7 days
    
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./lafiya.db")
    
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "sk-dummy-key-for-testing")
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "AIzaSyCH5_EAKT38eejmnITBc1EAaZvTZQDZXns")

settings = Settings()
