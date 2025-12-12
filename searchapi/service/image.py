from logging import getLogger
from magic import Magic

from shared.storage import Storage
from shared.constant import INGEST_BUCKET
from searchapi.repo.image import ImageRepository
from . import MilvusError

logger = getLogger(__name__)

class ImageService:
        
    def __init__(
        self,
        repo: ImageRepository,
        storage: Storage,
    ):
        from shared.ai.encode import ClipEncoder
        if not storage.check_connection(INGEST_BUCKET):
            storage.create_bucket(INGEST_BUCKET)
        self.repo = repo
        self.storage = storage
        self.mime_magic = Magic(mime=True)
        self.encoder = ClipEncoder()

    async def create_search(self, text: str) -> list[str]:
        """Create a search task to process the given file."""

        try:
            embedding = self.encoder.encode_text(text)
            results = await self.repo.search(embedding)
            return [item.id for item in results]
        except Exception as e:
            logger.error("failed to create search task", exc_info=e)
            raise MilvusError("failed to create search task") from e