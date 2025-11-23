from pydantic import BaseModel, Field

class IndexData(BaseModel):
    phash: str = Field(default="", description="Perceptual hash of the content")
    sha256: str = Field(default="", description="SHA256 hash of the content")
    embedding: list[float] = Field(default_factory=list, description="Embedding vector of the content")

    def milvus_dump(self) -> dict:
        return {
            "id": self.phash,
            "sha256": self.sha256,
            "embedding": self.embedding,
        }
    
class IndexResponse(BaseModel):
    id: str = Field(default="", description="Identifier of the created index entry")
    detail: str = Field(default="", description="Additional information about the indexing process")
    elapsed_time: float = Field(default=0.0, description="Time taken to create the index entry in seconds")