from dependency_injector import containers, providers

from shared.storage import new_storage, Storage
from shared.http_client.index import AsyncHttpIndexClient
from ingestworker.config import Config, conf_path
from ingestworker.service.ingest import IngestService

cfg = Config.from_yaml(conf_path)

class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    storage: providers.Provider[Storage] = providers.Singleton(
        new_storage,
        cfg=cfg.storage
    )

    index_client: providers.Provider[AsyncHttpIndexClient] = providers.Factory(
        AsyncHttpIndexClient,
        base_url=cfg.indexapi.url
    )

    ingest_service = providers.Singleton(
        IngestService,
        index_client=index_client,
    )