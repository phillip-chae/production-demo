from pathlib import Path
from pydantic import Field

from shared.config import BaseConfig, StorageConfig, MilvusConfig, RedisConfig

service_name = "ingestworker"
conf_path = Path(__file__).parent.parent.parent / "conf" / f"{service_name}.yaml"

class Config(BaseConfig):
    redis: RedisConfig = Field(default_factory=RedisConfig)
    storage: StorageConfig = Field(default_factory=StorageConfig)
    milvus_db: MilvusConfig = Field(default_factory=MilvusConfig)