from typing import List, Dict, Any, Optional
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_community.vectorstores.qdrant import Qdrant
from qdrant_client import QdrantClient
from qdrant_client.http import models
from PIL import Image
import io
import base64
import torch
from transformers import CLIPProcessor, CLIPModel
from app.core.config import settings

class MultimodalEmbeddingService:
    def __init__(self):
        # Initialize text embeddings (BGE)
        self.text_embedder = HuggingFaceBgeEmbeddings(
            model_name="BAAI/bge-large-en-v1.5",
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )
        
        # Initialize CLIP for image embeddings
        self.clip_model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
        self.clip_processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.clip_model.to(self.device)
        
        # Initialize Qdrant client
        self.qdrant_client = QdrantClient(
            host=settings.QDRANT_HOST,
            port=settings.QDRANT_PORT
        )
        
        # Initialize collections
        self._init_collections()
    
    def _init_collections(self):
        """Initialize Qdrant collections for text and images"""
        # Text collection
        self.qdrant_client.recreate_collection(
            collection_name="text_chunks",
            vectors_config=models.VectorParams(
                size=1024,  # BGE embedding size
                distance=models.Distance.COSINE
            )
        )
        
        # Image collection
        self.qdrant_client.recreate_collection(
            collection_name="image_chunks",
            vectors_config=models.VectorParams(
                size=512,  # CLIP embedding size
                distance=models.Distance.COSINE
            )
        )

    def _get_clip_image_embedding(self, image_data: bytes) -> List[float]:
        """Generate CLIP embedding for an image"""
        # Convert bytes to PIL Image
        image = Image.open(io.BytesIO(image_data))
        
        # Prepare image for CLIP
        inputs = self.clip_processor(
            images=image,
            return_tensors="pt"
        ).to(self.device)
        
        # Generate embedding
        with torch.no_grad():
            image_features = self.clip_model.get_image_features(**inputs)
            
        # Normalize and convert to list
        image_embedding = image_features.squeeze(0)
        image_embedding = image_embedding / image_embedding.norm(dim=-1, keepdim=True)
        return image_embedding.cpu().tolist()

    def _get_clip_text_embedding(self, text: str) -> List[float]:
        """Generate CLIP embedding for text (used for image search)"""
        inputs = self.clip_processor(
            text=[text],
            return_tensors="pt",
            padding=True
        ).to(self.device)
        
        with torch.no_grad():
            text_features = self.clip_model.get_text_features(**inputs)
            
        text_embedding = text_features.squeeze(0)
        text_embedding = text_embedding / text_embedding.norm(dim=-1, keepdim=True)
        return text_embedding.cpu().tolist()

    async def embed_text(self, text: str, metadata: Dict[str, Any]) -> None:
        """Embed text and store in Qdrant with metadata"""
        embeddings = self.text_embedder.embed_documents([text])
        
        # Store in Qdrant
        self.qdrant_client.upsert(
            collection_name="text_chunks",
            points=[
                models.PointStruct(
                    id=metadata.get("chunk_id"),
                    vector=embeddings[0],
                    payload={
                        "text": text,
                        "section": metadata.get("section"),
                        "file_type": metadata.get("file_type"),
                        "source": metadata.get("source"),
                        "page": metadata.get("page"),
                        **metadata
                    }
                )
            ]
        )

    async def embed_image(self, image_data: bytes, metadata: Dict[str, Any]) -> None:
        """Embed image using CLIP and store in Qdrant with metadata"""
        # Generate CLIP embedding
        image_embedding = self._get_clip_image_embedding(image_data)
        
        # Store in Qdrant
        self.qdrant_client.upsert(
            collection_name="image_chunks",
            points=[
                models.PointStruct(
                    id=metadata.get("chunk_id"),
                    vector=image_embedding,
                    payload={
                        "image_hash": base64.b64encode(image_data).decode(),
                        "section": metadata.get("section"),
                        "file_type": metadata.get("file_type"),
                        "source": metadata.get("source"),
                        "page": metadata.get("page"),
                        **metadata
                    }
                )
            ]
        )

    async def search(
        self,
        query: str,
        collection: str = "text_chunks",
        filter_conditions: Optional[Dict[str, Any]] = None,
        limit: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Search for similar documents with optional metadata filtering
        """
        # Generate appropriate embedding based on collection
        if collection == "text_chunks":
            query_vector = self.text_embedder.embed_query(query)
        else:  # image_chunks
            query_vector = self._get_clip_text_embedding(query)
        
        # Prepare filter conditions for Qdrant
        filter_query = None
        if filter_conditions:
            filter_query = models.Filter(
                must=[
                    models.FieldCondition(
                        key=key,
                        match=models.MatchValue(value=value)
                    )
                    for key, value in filter_conditions.items()
                ]
            )
        
        # Search in Qdrant
        search_results = self.qdrant_client.search(
            collection_name=collection,
            query_vector=query_vector,
            query_filter=filter_query,
            limit=limit
        )
        
        return [
            {
                "score": hit.score,
                "metadata": hit.payload,
                "content": hit.payload.get("text") if collection == "text_chunks" else hit.payload.get("image_hash")
            }
            for hit in search_results
        ] 