import json
import logging

from fastapi import FastAPI
from typing import Dict
from pathlib import Path
from contextlib import asynccontextmanager
from pydantic import AnyHttpUrl, field_validator, model_validator
from pydantic_settings import BaseSettings
from typing import List, Optional
from pathlib import Path

from ...utils import get_cpu_count, get_process_threads


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
    CELERY_THREADS_PER_WORKER: int | None = None
    CELERY_THREADS_PER_PROCESS: int | None = None
    CELERY_TASK_SOFT_TIMEOUT: int = 12000
    CELERY_TASK_HARD_TIMEOUT: int = 18000

    # CORS configuration
    CORS_ORIGINS: List[str] | str = ["http://app:5173"]

    # Database configuration
    MONGODB_URL: str = ""
    MONGODB_USERNAME: str = ""
    MONGODB_PASSWORD: str = ""
    MONGODB_DATABASE: str = "brick"
    MONGODB_SESSION_COLLECTION: str = "sessions"

    # Local database in the database:/data volume
    GENOMAD_DATABASE: Path = Path("/data/genomad_db")
    GENOMAD_SPLITS_ARG: int | None = None

    class ConfigDict:
        case_sensitive = True

    @field_validator("CORS_ORIGINS", mode="before")
    def assemble_cors_origins(cls, v: Optional[str]) -> List[AnyHttpUrl]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        return []

    @field_validator("MONGODB_USERNAME", mode="before")
    def get_mongodb_secret_username(cls, v: str):
        if v:
            path = Path(v)
            if path.is_file() and path.exists():
                v = path.read_text().strip("\n")
        return v

    @field_validator("MONGODB_PASSWORD", mode="before")
    def get_mongodb_secret_pwd(cls, v: str):
        if v and Path(v).exists():
            v = Path(v).read_text().strip("\n")
        return v

    @field_validator("GENOMAD_DATABASE", mode="after")
    def check_genomad_database(cls, v: Path):
        if v and not v.exists():
            logging.warn(f"geNomad database directory not found! ({v})")
            logging.warn(
                f"Attempts to execute `genomad` will fail in the `process_genomad_ring` worker!"
            )
        return v

    @model_validator(mode="after")
    def get_default_mongodb_url(self) -> "Settings":
        if not self.MONGODB_URL:
            self.MONGODB_URL = f"mongodb://{self.MONGODB_USERNAME}:{self.MONGODB_PASSWORD}@mongodb:27017?authSource=admin"
        return self

    @model_validator(mode="after")
    def get_resource_config(self) -> "Settings":
        if not self.CELERY_THREADS_PER_WORKER:
            self.CELERY_THREADS_PER_WORKER = get_cpu_count(
                fallback=1
            )  # if CPU count cannot be determined use 1 thread
            print(
                f"Set default threads per worker {self.CELERY_THREADS_PER_WORKER}",
                flush=True,
            )
        if not self.CELERY_THREADS_PER_PROCESS:
            self.CELERY_THREADS_PER_PROCESS = get_process_threads(
                fraction=1, fallback=2
            )  # if CPU counts <= 4 use 1 thread, else use fraction of total (all available)
            print(
                f"Set default threads per process {self.CELERY_THREADS_PER_PROCESS}",
                flush=True,
            )
        return self


def get_settings():
    logging.info("Initiating settings for FastAPI")
    return Settings()


# Global settings intitiation note that this will initiate
# settings for any execution of tasks in the CLI
settings = get_settings()

# Default session for session endpoint
DEFAULT_SESSIONS: Dict[str, dict] = {}


def read_default_session(path: Path) -> dict or None:
    session_data = None
    if path.exists() and path.is_file():
        with path.open() as default_session:
            session_data = json.load(default_session)
        logging.info("Loaded default session for session endpoint")
    else:
        logging.info(f"Could not find default session for session endpoint ({path})")

    return session_data


@asynccontextmanager
async def lifespan(_: FastAPI):
    DEFAULT_SESSIONS["default"] = read_default_session(
        path=Path("default.json")  # /app in container
    )
    yield
    DEFAULT_SESSIONS.clear()
