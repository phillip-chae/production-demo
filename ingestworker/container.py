from dependency_injector import containers, providers

from shared.storage import new_storage, Storage

from ingestworker.config import Config, conf_path
from ingestworker.repo.image import ImageRepository
from ingestworker.service.ingest import IngestService

cfg = Config.from_yaml(conf_path)

class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    storage: providers.Provider[Storage] = providers.Singleton(
        new_storage,
        cfg=cfg.storage
    )

    repo: providers.Provider[ImageRepository] = providers.Singleton(
        ImageRepository,
        cfg=cfg.milvus_db
    )

    ingest_service = providers.Singleton(
        IngestService,
        repo=repo,
        storage=storage,
    )