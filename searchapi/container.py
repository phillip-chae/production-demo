from dependency_injector import containers, providers

from shared.storage.s3 import S3
from searchapi.config import cfg
from searchapi.repo.image import ImageRepository
from searchapi.service.image import ImageService

class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    storage: providers.Provider[S3] = providers.Singleton(
        S3,
        cfg=cfg.s3
    )

    repo: providers.Provider[ImageRepository] = providers.Singleton(
        ImageRepository,
        cfg=cfg.milvus_db,
    )

    svc = providers.Singleton(
        ImageService,
        repo=repo,
        storage=storage,
    )