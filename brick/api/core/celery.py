from celery import Celery
from .config import settings

celery_app = Celery(
    "worker",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    broker_connection_retry_on_startup=True
)
celery_app.autodiscover_tasks(
    ['brick.api.tasks']
)