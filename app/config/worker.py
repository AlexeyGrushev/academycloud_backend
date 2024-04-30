from celery import Celery

from app.config.app_settings import settings


celery = Celery(
    "worker",
    broker=f"{settings.APP_BROKER_URL}",
)

celery.autodiscover_tasks(
    ["app.tasks.*"],
)
