from celery import Celery
import os
from app.config import settings

broker_url = (
    settings.CELERY_BROKER_URL
)
result_backend = (
    settings.CELERY_RESULT_BACKEND
)

celery_app = Celery(
    "price_tracker",
    broker=broker_url,
    backend=result_backend,
    include=["app.tasks.update_prices"],
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
)

celery_app.autodiscover_tasks(["app.tasks"])

try:
    from . import celery_beat_schedule
except Exception:
    pass
