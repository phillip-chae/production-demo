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
            search_params={
                "metric_type": "COSINE", 
                "params": {
                    "ef": 256,
                }
            },
            limit=20,
            output_fields=["file_name"],
        )
        print(results)
        hits = results[0] if results else []
        items = []
        for hit in hits:
            item = IndexItem()
            item.id = hit.get("id", "")
            item.distance = hit.get("distance", 0.0)
            item.file_name = hit.get("entity", {}).get("file_name", "")
            items.append(item)
        return items