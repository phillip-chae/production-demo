from dependency_injector import containers, providers
from celery import Celery

from shared.storage import new_storage, Storage
from searchapi.config import Config, conf_path, service_name
from searchapi.repo.image import ImageRepository
from searchapi.service.image import ImageService

cfg = Config.from_yaml(conf_path)

def get_celery(broker_url: str) -> Celery:
    from ingestworker.task import QUEUE, task_routes
    return Celery(
        service_name,
        queue=QUEUE,
        broker=broker_url,
        backend=broker_url,
        task_routes=task_routes,
    )

class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    storage: providers.Provider[Storage] = providers.Singleton(
        new_storage,
        cfg=cfg.storage
    )

    celery: providers.Provider[Celery] = providers.Singleton(
        get_celery,
        broker_url=cfg.redis.url,
    )

    repo: providers.Provider[ImageRepository] = providers.Singleton(
        ImageRepository,
        cfg=cfg.milvus_db,
    )

    svc = providers.Singleton(
        ImageService,
        storage=storage,
        celery=celery,
    )