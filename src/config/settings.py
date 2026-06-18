"""Configuration management for the QA Platform"""
import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Settings:
    """Application settings"""
    
    # Environment
    ENV: str = os.getenv("ENV", "development")
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./data/qa_platform.db")
    
    # LangChain / LLM
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    MODEL_NAME: str = os.getenv("MODEL_NAME", "gpt-4")
    TEMPERATURE: float = float(os.getenv("TEMPERATURE", "0.7"))
    
    # LangSmith (Observability)
    LANGSMITH_API_KEY: str = os.getenv("LANGSMITH_API_KEY", "")
    LANGSMITH_PROJECT: str = os.getenv("LANGSMITH_PROJECT", "agentic-qa-platform")
    LANGSMITH_ENDPOINT: str = os.getenv("LANGSMITH_ENDPOINT", "https://api.smith.langchain.com")
    
    # Application
    APP_NAME: str = "Agentic QA Platform"
    APP_VERSION: str = "0.1.0"
    
    # Website Configuration
    TARGET_WEBSITE_URL: str = os.getenv("TARGET_WEBSITE_URL", "https://demo.opencart.com/")
    
    # Agent Configuration
    MAX_ITERATIONS: int = int(os.getenv("MAX_ITERATIONS", "10"))
    TIMEOUT_SECONDS: int = int(os.getenv("TIMEOUT_SECONDS", "300"))
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE: str = os.getenv("LOG_FILE", "logs/app.log")
    
    # Paths
    REQUIREMENTS_PATH: str = os.getenv("REQUIREMENTS_PATH", "./requirements_folder")
    DATA_PATH: str = os.getenv("DATA_PATH", "./data")
    
    def __init__(self):
        """Validate settings on initialization"""
        if self.ENV == "production" and not self.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is required in production")
    
    def is_production(self) -> bool:
        """Check if running in production"""
        return self.ENV == "production"
    
    def is_development(self) -> bool:
        """Check if running in development"""
        return self.ENV == "development"


# Global settings instance
settings = Settings()
