
from brick.api.core.celery import celery_app

if __name__ == "__main__":
    # Use the Celery CLI to start the worker
    argv = [
        'worker',
        '--loglevel=info'
    ]
    celery_app.worker_main(argv)