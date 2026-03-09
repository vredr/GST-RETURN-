"""Configuration settings for TaxNow GST Platform"""
import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    APP_NAME: str = "TaxNow GST API"
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    MONGODB_URI: str = os.getenv("MONGODB_URI", "mongodb://localhost:27017/taxnow")
    DATABASE_NAME: str = os.getenv("DATABASE_NAME", "taxnow")
    MAX_FILE_SIZE: int = 50 * 1024 * 1024
    UPLOAD_DIR: str = "/tmp/taxnow/uploads"
    OUTPUT_DIR: str = "/tmp/taxnow/outputs"
    DEFAULT_SUPPLIER_STATE: str = "Maharashtra"
    HSN_VALIDATION: bool = True
    CORS_ORIGINS: list = ["*"]
    
    class Config:
        env_file = ".env"

settings = Settings()
