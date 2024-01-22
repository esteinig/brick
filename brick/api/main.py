import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .core.config import settings, Settings

from .endpoints import files
from .endpoints import sessions
from .endpoints import tasks
from .endpoints import rings

from ..utils import enough_disk_space

def init_working_directory(settings: Settings):

    logging.info("Initiating working directory")

    # Absolute working directory path
    try:
        settings.WORK_DIRECTORY = settings.WORK_DIRECTORY.resolve()
    except Exception as _:
        logging.error(f"Working directory path could not be resolved: {settings.WORK_DIRECTORY}")
        exit(1)

    # Create working directory
    if not settings.WORK_DIRECTORY.exists():
        logging.warn(f"Working directory does not exist: {settings.WORK_DIRECTORY}")
        logging.warn(f"Attempting to create working directory path for server operations...")

        try:
            settings.WORK_DIRECTORY.mkdir(parents=True)
            logging.info(f"Working directory created at: {settings.WORK_DIRECTORY}")

        except Exception as _:
            logging.error(f"Working directory could not be created: {settings.WORK_DIRECTORY}")
            exit(1)

    # Disk space check
    if not enough_disk_space(path=settings.WORK_DIRECTORY, disk_space_limit_gb=settings.WORK_DISK_SPACE_GB):
        logging.error("Not enough disk space for working directory")
        logging.error(f"Application requires at least {settings.WORK_DISK_SPACE_GB} gigabytes free disk space at {settings.WORK_DIRECTORY}")
        exit(1)
    else:
        logging.info(f"Sufficient disk space (>= {settings.WORK_DISK_SPACE_GB} GB) at working directory: {settings.WORK_DIRECTORY}")


def init_api():
    
    logging.info("Initiating FastAPI")

    init_working_directory(settings=settings)

    app = FastAPI(title="BRICK API")
    app.include_router(files.router)
    app.include_router(sessions.router)
    app.include_router(tasks.router)
    app.include_router(rings.router)

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=False,
        allow_methods=["GET", "POST", "PUT", "DELETE"],
        allow_headers=[
            "Content-Type",
            "Accept",
            "X-Requested-With",
            "User-Agent",
            "Cache-Control",
            "Expires",
            "Pragma",
            "X-CSRF-Token",
            "Access-Control-Allow-Headers",
            "Accept-Encoding",
            "Accept-Language",
        ]
    )

    return app


app = init_api()