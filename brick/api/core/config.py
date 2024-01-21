import logging 

from pydantic import AnyHttpUrl, field_validator
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
    SECRET_KEY: str = "CURRENTLY_NOT_USED"

    # Working directory for session and tasks
    WORK_DIRECTORY: Path = Path(f"/tmp/brick-work")
    WORK_DISK_SPACE_GB: float = 5

    # Session directory limits
    SESSION_MAX_SIZE_MB: int = 200
    SESSION_MAX_FILES: int = 10000

    # Celery configuration
    CELERY_BROKER_URL: str = "redis://redis:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://redis:6379/1"

    # CORS configuration
    CORS_ORIGINS: List[str] | str = ['http://app:5173']

    # Database configuration
    MONGODB_USERNAME: str = ""
    MONGODB_PASSWORD: str = ""
    MONGODB_DATABASE: str = "brick"
    MONGODB_SESSION_COLLECTION: str = "sessions"

    class ConfigDict:
        case_sensitive = True

    @field_validator('CORS_ORIGINS', mode="before")
    def assemble_cors_origins(cls, v: Optional[str]) -> List[AnyHttpUrl]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        return []

    @field_validator('MONGODB_USERNAME', mode="before")
    def get_mongodb_secret_username(cls, v: str):   
        if v:
            path = Path(v)     
            if path.is_file() and path.exists():
                v = path.read_text()
        return v
    
    @field_validator('MONGODB_PASSWORD', mode="before")
    def get_mongodb_secret_pwd(cls, v: str):      
        if v and Path(v).exists():
            v = Path(v).read_text()
        return v
    

def get_settings():
    logging.info("Initiating settings for FastAPI")
    return Settings()


# Global settings intitiation
# note that this will initiate
# settings for any execution of
# tasks in the CLI
settings = get_settings()


