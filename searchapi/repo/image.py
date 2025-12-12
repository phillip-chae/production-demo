from shared.repo.milvus import AsyncMilvusRepository
from shared.model.index import IndexItem
from ingestworker.repo.image import INGEST_DB, VECTOR_COLLECTION, collection_schema, index_params

class ImageRepository(AsyncMilvusRepository[IndexItem]):
    model = IndexItem
    collection_name = VECTOR_COLLECTION
    database_name = INGEST_DB
    collection_schema = collection_schema
    index_params = index_params
    
    async def search(self, embedding: list[float]) -> list[IndexItem]:
        results = await self.client.search(
            collection_name=self.collection_name,
            data=[embedding],
            anns_field="vector",
            param={
                "metric_type": "COSINE", 
                "params": {
                    "ef": 256
                }
            },
            limit=20,
            output_fields=["id"],
        )
        hits = results[0] if results else []
        return [IndexItem(**hit) for hit in hits]