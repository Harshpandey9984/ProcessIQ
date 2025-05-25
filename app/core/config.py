"""
Configuration settings for the Digital Twin Optimization Platform.
"""

import os
import secrets
from typing import Any, Dict, List, Optional, Union

# Handle different pydantic versions
try:
    # For pydantic v2
    from pydantic_settings import BaseSettings
    from pydantic import field_validator as validator
except ImportError:
    # For pydantic v1
    from pydantic import BaseSettings, validator


class Settings(BaseSettings):
    """Application settings."""
    
    # API settings
    API_V1_STR: str = "/v1"
    # Use a fixed SECRET_KEY for development to ensure tokens remain valid
    # In production, this should be set via environment variable
    SECRET_KEY: str = os.environ.get("SECRET_KEY", "development_secret_key_for_testing_only_do_not_use_in_production")
    
    # Server settings
    SERVER_HOST: str = "0.0.0.0"
    SERVER_PORT: int = 8000
    DEBUG: bool = True
    
    # CORS settings
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]

    # Database settings
    DATABASE_URL: str = "sqlite:///./digital_twin.db"
    
    # Data directory
    DATA_DIR: str = "../data"
    
    # Model directories
    MODEL_DIR: str = "../app/models/saved"
    
    # Intel optimization flags
    USE_INTEL_OPTIMIZATIONS: bool = True
    USE_OPENVINO: bool = True
    USE_DAAL: bool = True
    
    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
