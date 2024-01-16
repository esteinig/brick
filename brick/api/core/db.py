import motor.motor_asyncio
import logging

from pymongo import MongoClient
from .config import settings


# Client for use in FastAPI endpoints (async)
try:
    async_client = motor.motor_asyncio.AsyncIOMotorClient(f"mongodb://{settings.MONGODB_USERNAME}:{settings.MONGODB_PASSWORD}@mongodb:27017?authSource=admin")
except Exception as e:
    logging.error(f"Failed to initiate Motor database client: {str(e)}")
    exit(1)

# Client for use in Celery workers (sync)
try:
    client = MongoClient(f"mongodb://{settings.MONGODB_USERNAME}:{settings.MONGODB_PASSWORD}@mongodb:27017?authSource=admin")
except Exception as e:
    logging.error(f"Failed to initiate PyMongo database client: {str(e)}")
    exit(1)

async def get_session_collection_motor():
    db = async_client[settings.MONGODB_DATABASE]
    return db[settings.MONGODB_SESSION_COLLECTION]

def get_session_collection_pymongo():
    db = client[settings.MONGODB_DATABASE]
    return db[settings.MONGODB_SESSION_COLLECTION]
