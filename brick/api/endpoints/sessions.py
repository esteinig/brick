from fastapi import APIRouter, HTTPException

from datetime import datetime

from ..models import Session
from ..schemas import SessionUpdateSchema, update_rings
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

@router.put("/{session_id}", response_model=Session)
async def update_session(session_id: str, session_update: SessionUpdateSchema):
    collection = await get_session_collection_motor()
    existing_session_data: dict = await collection.find_one({"id": session_id})

    if not existing_session_data:
        raise HTTPException(status_code=404, detail="Session not found")

    # Update session with new data
    existing_session_data: Session = Session(**existing_session_data)
    updated_session_data = existing_session_data.model_copy()

    updated_session_data.files = session_update.files
    updated_session_data.rings = update_rings(rings=existing_session_data.rings, updates=session_update.ring_updates)
    
    # Save updated session in the database
    await collection.replace_one({"id": session_id}, updated_session_data.model_dump())

    # Return updated session
    return updated_session_data

@router.post("/{session_id}", response_model=Session)
async def create_session(session_id: str):
    
    collection = await get_session_collection_motor()
    session_data = await collection.find_one({"id": session_id})

    if session_data:
        raise HTTPException(status_code=409, detail="Session already exists")
    
    new_session = Session(
        id=session_id, 
        date=datetime.now().isoformat(), 
        files=[],
        rings=[]
    )

    await collection.insert_one(
        new_session.model_dump()
    )

    return new_session