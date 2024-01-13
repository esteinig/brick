from fastapi import APIRouter, HTTPException

from ..models import Session
from ..core.db import get_session_collection_motor

router = APIRouter(
    prefix="/sessions",
    tags=["session"],
)


@router.get("/{session_id}", response_model=Session)
async def get_session(session_id: str, session_files_exist: bool = False):

    collection = await get_session_collection_motor()
    session_data = await collection.find_one({"id": session_id})

    if not session_data:
        raise HTTPException(status_code=404, detail="Session not found")
    else:
        session_data = Session(**session_data)

    if session_files_exist:
        session_data.validate_file_paths()
    
    return session_data
