from celery import Celery
from celery.signals import worker_process_init
import logging

from ingestworker.config import service_name
from ingestworker.container import Container, cfg
from ingestworker.task import task_routes

logger = logging.getLogger(__name__)

app = Celery(
    service_name,
    broker=cfg.redis.url,
    backend=cfg.redis.url,
    include = [
        "ingestworker.task.ingest",
    ]
)

app.conf.update(task_routes = task_routes)

container = Container()
container.wire(packages=[
    "ingestworker.task",
    "ingestworker.service",
])

@worker_process_init.connect
def init_svcs(**kwargs):
    """Initialize services in worker process. Before task execution."""
    logger.info("preloading services in worker process")
    _ = container.ingest_service()
    logger.info("services preloaded successfully")