import httpx
import logging

from datetime import datetime, timedelta
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from typing import Generator

from .schemas import Session


class ApiClient:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.client = httpx.AsyncClient()

    async def get_session_ids(self):
        try:
            response = await self.client.get(f"{self.base_url}/sessions/identifiers")
            if response.status_code == 200:
                return response.json()
            else:
                logging.error(f"Failed to fetch session identifiers: {response.text}")
                return []
        except Exception as e:
            logging.error(f"{e}")
            return []

    async def delete_session(self, session_id: str, session_data: bool = True):

        try:
            response = await self.client.delete(
                f"{self.base_url}/sessions/{session_id}",
                params={"session_data": session_data},
            )
            return response.status_code, response.text
        except Exception as e:
            logging.error(f"{e}")
            return None, str(e)

    async def get_session(self, session_id: str):
        try:
            response = await self.client.get(f"{self.base_url}/sessions/{session_id}")
            if response.status_code == 200:
                return response.json()  # Assuming the response is JSON serializable
            else:
                logging.error(f"Failed to fetch session {session_id}: {response.text}")
                return None
        except Exception as e:
            logging.error(f"Error fetching session {session_id}: {e}")
            return None

    async def close(self):
        await self.client.aclose()


# Database cleaner


async def fetch_sessions_generator(
    api_client: ApiClient, logger: logging.Logger | None = None
) -> Generator[Session]:
    if logger:
        logger.info(f"Requesting session identifiers from API")

    session_ids = await api_client.get_session_ids()

    if logger:
        logger.info(f"Obtained {len(session_ids)} session identifiers from API")

    for session_id in session_ids:
        session_data = await api_client.get_session(session_id=session_id)
        if session_data:
            yield Session(**session_data)  # full session data


async def check_and_delete_expired_sessions(
    api_client: ApiClient, expire_days: int, logger: logging.Logger | None = None
):

    current_datetime = datetime.now()
    expiration_datetime = current_datetime - timedelta(days=expire_days)

    async for session in fetch_sessions_generator(api_client=api_client, logger=logger):
        session_date = datetime.fromisoformat(session.date)
        if session_date < expiration_datetime:
            if logger:
                logger.info(f"Session {session.id} is expired and will be deleted")

            status_code, response_text = await api_client.delete_session(
                session_id=session.id, session_data=True
            )  # delete session directory

            if status_code == 200:
                if logger:
                    logger.info(f"Session {session.id} deleted successfully")
            else:
                if logger:
                    logger.error(
                        f"Failed to delete session {session.id}: {response_text}"
                    )
        else:
            if logger:
                logger.info(f"Session {session.id} has not yet expired")


def schedule_session_cleanup(
    api_client: ApiClient,
    logger: logging.Logger | None = None,
    expire_days: int = 7,
    day_of_week: str = "*",
    time_of_day: str = "04:00",
):
    """
    Schedule the session cleanup and start the scheduler
    """

    async def job():
        await check_and_delete_expired_sessions(
            api_client=api_client, expire_days=expire_days, logger=logger
        )
        await api_client.close()

    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        job,
        trigger=CronTrigger(
            day_of_week=day_of_week,
            hour=time_of_day.split(":")[0],
            minute=time_of_day.split(":")[1],
        ),
    )
    scheduler.start()
