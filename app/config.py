import os
from pydantic import BaseModel, Field
from functools import lru_cache
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseModel):
    """
    NOISEKILLER Configuration Model using Core Pydantic V2.
    """
    # App Identity
    app_name: str = "NOISEKILLER"
    environment: str = os.getenv("ENVIRONMENT", "development")
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    
    # AI Engine Configuration
    # We pull directly from os.getenv and use Field for validation
    gemini_api_key: str = Field(default_factory=lambda: os.getenv("GEMINI_API_KEY", ""))

    def validate_keys(self):
        """Ensures critical keys are present."""
        if not self.gemini_api_key:
            raise ValueError("GEMINI_API_KEY is missing from .env file!")

@lru_cache
def get_settings():
    """
    Returns a cached instance of the settings.
    """
    s = Settings()
    s.validate_keys()
    return s

# Global instance for project-wide access
settings = get_settings()