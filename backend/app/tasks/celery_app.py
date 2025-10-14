from celery import Celery
from app.core.config import settings

celery_app = Celery(
    "quantflow",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
)

celery_app.conf.update(
    task_routes={
        "tasks.backtest.*": {"queue": "backtests"},
    },
    task_time_limit=60 * 30,
)

# Import tasks to register them
from app.tasks import backtest
