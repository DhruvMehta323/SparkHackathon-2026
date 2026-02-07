"""Configuration for FastAPI application."""
import os
from pathlib import Path


class Settings:
    """API Settings"""
    
    # API Settings
    API_V1_STR: str = "/api"
    PROJECT_NAME: str = "FairRank API"
    VERSION: str = "1.0.0"
    
    # Database
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent
    FAIRRANK_DB: str = os.getenv("FAIRRANK_DB", str(BASE_DIR / "fairrank.db"))
    
    # CORS - Frontend URLs
    BACKEND_CORS_ORIGINS: list = [
        "http://localhost:3000",      # React default
        "http://localhost:5173",      # Vite default
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
    ]
    
    # Background Tasks
    USE_BACKGROUND_TASKS: bool = True
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")


settings = Settings()