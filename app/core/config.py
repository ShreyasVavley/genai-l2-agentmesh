import os
from pydantic_settings import BaseSettings
from typing import Optional, List

class Settings(BaseSettings):
    PROJECT_NAME: str = "AgenticDevOps & Audit Mesh (GenAI L2)"
    VERSION: str = "2.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Models & Gateway
    DEFAULT_MODEL: str = os.getenv("DEFAULT_MODEL", "gemini/gemini-1.5-pro")
    FALLBACK_MODEL: str = os.getenv("FALLBACK_MODEL", "gpt-4o-mini")
    MAX_TOKENS_PER_TASK: int = 4000
    SIMULATION_MODE: bool = os.getenv("SIMULATION_MODE", "true").lower() == "true"
    
    # API Keys (Optional - automatically uses simulated inference if not provided)
    GEMINI_API_KEY: Optional[str] = os.getenv("GEMINI_API_KEY", None)
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY", None)
    
    # Observability & Security
    ENABLE_OTEL_TRACING: bool = True
    HITL_REQUIRED_FOR_SHELL: bool = True

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
