import pytest
from pymongo.collection import Collection
from motor.motor_asyncio import AsyncIOMotorCollection
from unittest.mock import patch, MagicMock, AsyncMock

from brick.api.core.db import (
    get_session_collection_motor,
    get_session_collection_pymongo,
)


@pytest.fixture
def mock_motor_client():
    with patch(
        "motor.motor_asyncio.AsyncIOMotorClient", new_callable=AsyncMock
    ) as mock:
        mock.return_value.__getitem__.return_value.__getitem__.return_value = (
            AsyncMock()
        )
        yield mock


@pytest.fixture
def mock_pymongo_client():
    with patch("pymongo.MongoClient", new_callable=MagicMock) as mock:
        mock.return_value.__getitem__.return_value.__getitem__.return_value = (
            MagicMock()
        )
        yield mock


def test_get_session_collection_pymongo(mock_pymongo_client):
    collection = get_session_collection_pymongo()
    assert isinstance(collection, Collection)


@pytest.mark.asyncio
async def test_get_session_collection_motor(mock_motor_client):
    collection = await get_session_collection_motor()
    assert isinstance(collection, AsyncIOMotorCollection)
