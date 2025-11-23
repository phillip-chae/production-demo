from pathlib import Path
from typing import BinaryIO
import torch
from PIL import Image
import numpy as np
import hashlib

from shared.logger import get_logger
from shared.model.index import IndexData
from shared.hash.phash import Phasher
from shared.http_client.index import AsyncHttpIndexClient

logger = get_logger(__name__)

class IngestService:
    def __init__(
        self,
        index_client: AsyncHttpIndexClient
    ):
        self.index_client = index_client
        self.feature_extractor = self.FeatureExtractor("tf_efficientnetv2_s")
        self.phasher = Phasher()
    
    async def ingest(self, image_file: str | Path | BinaryIO):
        
        if isinstance(image_file, (str, Path)):
            file = open(image_file, "rb")
            should_close = True
        else:
            file = image_file
            should_close = False
        try:
            embedding = self.feature_extractor(file)
            file.seek(0)
            sha256 = self._calculate_sha256(file)
            phash = self._calculate_phash(file)
            
        finally:
            if should_close:
                file.close()

        data = IndexData(
            sha256=sha256,
            phash=phash,
            embedding=embedding.tolist()
        )
        logger.debug("Ingested data prepared", extra={
            "sha256": sha256,
            "phash": phash
        })
        return await self.index_client.create_index(data)
    
    def _calculate_sha256(self, image_file: BinaryIO) -> str:
        h = hashlib.sha256()
        with image_file as f:
            f.seek(0)
            while chunk := f.read(8192):
                h.update(chunk)
            f.seek(0)
            return h.hexdigest()
    
    def _calculate_phash(self, image_file: BinaryIO) -> str:
        with image_file as f:
            f.seek(0)
            phash = self.phasher(f)
            f.seek(0)
            return phash

    class FeatureExtractor:
        def __init__(
            self, 
            model_name: str,
            normalize: bool = True
        ):
            import timm
            from timm.data import resolve_model_data_config
            from timm.data.transforms_factory import create_transform
            self.normalize = normalize
            # Load the pre-trained model
            self.model = timm.create_model(
                model_name, pretrained=True, num_classes=0, global_pool="avg"
            )
            self.model.eval()

            config = resolve_model_data_config(self.model)
            # Get the preprocessing function provided by TIMM for the model
            self.transform = create_transform(**config)

        def __call__(self, image_file: str | Path | BinaryIO) -> np.ndarray:
            # Preprocess the input image
            img = Image.open(image_file).convert("RGB")  # Convert to RGB if needed
            tensor = self.transform(img).unsqueeze(0)  # type: ignore

            with torch.no_grad():
                features = self.model(tensor)

            # Extract the feature vector
            feature_vector = features.squeeze().numpy()
        
            if self.normalize:
                feature_vector = feature_vector / np.linalg.norm(feature_vector)

            return feature_vector