import os
import logging 

from pydantic import AnyHttpUrl, validator
from pydantic_settings import BaseSettings
from typing import List, Optional
from pathlib import Path

class Settings(BaseSettings):

    # Basic application configuration
    APP_NAME: str = "BRICK"
    APP_VERSION: str = "0.1.0"
    API_PREFIX: str = "/api"
    DEBUG_MODE: bool = False

    # Secret key for instance
    SECRET_KEY: str = ""

    # Working directory for session and tasks
    WORK_DIRECTORY: Path = Path(f"/tmp/brick-work")

    # Session directory limits
    SESSION_MAX_SIZE_MB: int = 200
    SESSION_MAX_FILES: int = 10000

    # Celery configuration
    CELERY_BROKER_URL: str = "redis://redis:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://redis:6379/1"

    # CORS configuration
    CORS_ORIGINS: List[str] = ['http://app:5173']

    # Database configuration
    MONGODB_URL: str = "mongodb://root:example@mongodb:27017"
    MONGODB_DATABASE: str = "brick"
    MONGODB_SESSION_COLLECTION: str = "sessions"

    class ConfigDict:
        case_sensitive = True
        env_file = ".env"
        env_file_encoding = 'utf-8'
        env_prefix = "BRICK_"

    @validator('CORS_ORIGINS', pre=True)
    def assemble_cors_origins(cls, v: Optional[str]) -> List[AnyHttpUrl]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        return []

class DevelopmentSettings(Settings):
    class ConfigDict:
        env_prefix = "DEV_BRICK_"

class ProductionSettings(Settings):
    class ConfigDict:
        env_prefix = "PROD_BRICK_"

def get_settings():
    environment = os.getenv("BRICK_ENV", "").lower()
    
    if environment == "production":
        return ProductionSettings()
    elif environment == "development":
        return DevelopmentSettings()    
    else:
        return Settings()
    


settings = get_settings()

# TODO: add disk size checks with a minimum required

# Absolute working directory path
try:
    settings.WORK_DIRECTORY = settings.WORK_DIRECTORY.resolve()
except Exception as _:
    logging.error(f"Working directory path could not be resolved: {settings.WORK_DIRECTORY}")
    exit(1)

# Create working directory
if not settings.WORK_DIRECTORY.exists():
    logging.info(f"Working directory does not exist: {settings.WORK_DIRECTORY}")
    logging.info(f"Attempting to create working directory path for server operations...")
    try:
        settings.WORK_DIRECTORY.mkdir(parents=True)
    except Exception as _:
        logging.error(f"Working directory could not be created: {settings.WORK_DIRECTORY}")
        exit(1)