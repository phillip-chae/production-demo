from pathlib import Path
from pydantic import Field

from shared.config import BaseConfig, S3Config, RedisConfig, MilvusConfig

service_name = "searchapi"
conf_path = Path(__file__).parent.parent.parent / "conf" / f"{service_name}.yaml"

class Config(BaseConfig):
    s3: S3Config = Field(default_factory=S3Config)
    milvus_db: MilvusConfig = Field(default_factory=MilvusConfig)

cfg = Config.from_yaml(conf_path)