from celery import Celery
from .config import settings

celery_app = Celery(
    "worker",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    broker_connection_retry_on_startup=True,
    task_serializer="json",
    accept_content=["json"],  # Ignore other content
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)

celery_app.autodiscover_tasks(["brick.api.tasks"])

celery_app.conf.worker_concurrency = settings.CELERY_THREADS_PER_WORKER
celery_app.conf.worker_prefetch_multiplier = 1  # For memory-intensive tasks
celery_app.conf.worker_max_tasks_per_child = 100  # Prevent memory leaks

celery_app.conf.task_soft_time_limit = (
    settings.CELERY_TASK_SOFT_TIMEOUT
)  # Soft time limit in seconds (10m)
celery_app.conf.task_time_limit = (
    settings.CELERY_TASK_HARD_TIMEOUT
)  # Hard time limit in seconds to kill the worker (20m)


# Genomad can be resource intensive - until we have implemented resource-managing
# workflows restrict task requests across all executions
celery_app.conf.task_annotations = {
    "worker.tasks.process_genomad_ring": {"rate_limit": "5/m"},
    "worker.tasks.process_blast_ring": {
        "rate_limit": "100/m"
    },  # Less strict, runs with minimal resources
}
