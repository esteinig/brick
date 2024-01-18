from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from datetime import datetime
from typing import List

from ...rings import Ring
from ..models import Session
from ..schemas import RingUpdate
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

@router.put("/{session_id}/ring")
async def update_session_ring(session_id: str, ring_update: RingUpdate):
    collection = await get_session_collection_motor()

    print(ring_update)

    existing_session: dict = await collection.find_one({"id": session_id})

    if not existing_session:
        raise HTTPException(status_code=404, detail="Session not found")
    else:
        existing_session: Session = Session(**existing_session)


    # If an index update is requested we have to change the other ring
    # indices in the current filtered ring view (by reference sequence)
    # their identifiers are provided as `index_group`
    
    if ring_update.index_group:
        updated_rings = update_ring_indices(session=existing_session, ring_update=ring_update)
        
        for ring in updated_rings:
            await collection.update_one(
                {"id": session_id, "rings.id": ring.id},
                {"$set": {"rings.$[elem].index": ring.index}},
                array_filters=[{"elem.id": ring.id}]
            )
    else:
        update_data = {"$set": {}}
        for key, value in ring_update.model_dump(exclude_none=True, exclude=['id', 'index_group']).items():
            update_data["$set"][f"rings.$[elem].{key}"] = value

        if update_data["$set"]:
            # Update the specific ring in the session
            await collection.update_one(
                {"id": session_id, "rings.id": ring_update.id},
                update_data,
                array_filters=[{"elem.id": ring_update.id}]
            )

    # Return standard JSON response for application
    return JSONResponse(
        status_code=200, 
        content={
            "message": "Ring updated successfully",
            "session_id": session_id,
            "ring_id": ring_update.id
        }
    )


@router.delete("/{session_id}/ring")
async def delete_session_ring(session_id: str, ring_update: RingUpdate):
    collection = await get_session_collection_motor()

    # Retrieve the session
    existing_session: dict = await collection.find_one({"id": session_id})
    if not existing_session:
        raise HTTPException(status_code=404, detail="Session not found")
    else:
        existing_session: Session = Session(**existing_session)


    # Check if the ring exists in the session
    if not any(ring.id == ring_update.id for ring in existing_session.rings):
        raise HTTPException(status_code=404, detail="Ring not found in session")

    # Update the session to remove the specific ring
    await collection.update_one(
        {"id": session_id},
        {"$pull": {"rings": {"id": ring_update.id}}}
    )

    # Filter and reindex only the rings in the index_group (which contains also the identifier of the deleted ring)
    index_group_rings = {
        ring.id: ring for ring in  existing_session.rings
        if ring.id in ring_update.index_group and ring.id != ring_update.id
    }

    reindexed_rings = sorted(
        (ring for ring in index_group_rings.values() if ring.id != ring_update.id), key=lambda x: x.index
    )

    for i, ring in enumerate(reindexed_rings):
        index_group_rings[ring.id].index = i

    # Update the entire rings array in the session
    updated_rings = [
        index_group_rings.get(ring.id, ring).model_dump() 
        for ring in existing_session.rings 
        if ring.id != ring_update.id
    ]

    await collection.update_one(
        {"id": session_id},
        {"$set": {"rings": updated_rings}}
    )

    # Return standard JSON response for application
    return JSONResponse(
        status_code=200, 
        content={
            "message": "Ring deleted and specified indices updated successfully",
            "session_id": session_id,
            "ring_id": ring_update.id
        }
    )

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

# Helper


def update_ring_indices(session: Session, ring_update: RingUpdate) -> List[Ring]:
    # Extract the subset of rings to be reindexed
    subset_rings = [ring for ring in session.rings if ring.id in ring_update.index_group]

    # Sort the subset based on their current index
    subset_rings.sort(key=lambda ring: ring.index)

    # Find the current index of the ring to be updated
    current_index = next((ring.index for ring in subset_rings if ring.id == ring_update.id), None)
    new_index = ring_update.index

    # Only proceed with reindexing if the ring is found and the index is changing
    if current_index is not None and current_index != new_index:
        # Return if the ring is not found or the index is not changing
        if current_index is None or current_index == new_index:
            return

        # Moving a ring outside: increase the index of rings between the current and new index
        if new_index > current_index:
            for ring in subset_rings:
                if current_index < ring.index <= new_index:
                    ring.index -= 1

        # Moving a ring inside: increase the index of rings that are now after the new index
        else:
            for ring in subset_rings:
                if ring.index >= new_index and ring.id != ring_update.id:
                    ring.index += 1

        # Set the updated ring's index to the new index
        for ring in subset_rings:
            if ring.id == ring_update.id:
                ring.index = new_index

        # Normalize indices to start from 0 and be continuous
        subset_rings.sort(key=lambda ring: ring.index)
        for i, ring in enumerate(subset_rings):
            ring.index = i

    return subset_rings