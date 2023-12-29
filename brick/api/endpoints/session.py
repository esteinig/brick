import shutil
import os
import uuid

from pathlib import Path
from pydantic import ValidationError
from celery.result import AsyncResult
from fastapi.responses import JSONResponse
from fastapi import APIRouter,  HTTPException

from ..models import Session
from ..core.config import settings
from ..core.celery import celery_app
from ..core.db import get_session_collection_motor

router = APIRouter(
    prefix="/sessions",
    tags=["session"],
)


@router.get("/{session_id}", response_model=Session)
async def get_session(session_id: str):

    collection = await get_session_collection_motor()
    session_data = await collection.find_one({"id": session_id})

    if not session_data:
        raise HTTPException(status_code=404, detail="Session not found")

    return session_data
