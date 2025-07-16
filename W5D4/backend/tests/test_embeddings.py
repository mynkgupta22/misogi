import pytest
from app.services.embeddings import MultimodalEmbeddingService
from PIL import Image
import numpy as np
import io
import torch

@pytest.fixture(scope="module")
def embedding_service():
    return MultimodalEmbeddingService()

@pytest.fixture
def sample_image():
    # Create a sample image
    img_array = np.random.randint(0, 255, (224, 224, 3), dtype=np.uint8)
    img = Image.fromarray(img_array)
    
    # Convert to bytes
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    return img_byte_arr.getvalue()

@pytest.fixture
def sample_metadata():
    return {
        "chunk_id": "test123",
        "file_type": ".txt",
        "source": "test.txt",
        "page": 1,
        "section": "introduction"
    }

@pytest.mark.asyncio
async def test_embed_text(embedding_service, sample_metadata):
    text = "This is a test document for embedding."
    
    # Test embedding text
    await embedding_service.embed_text(text, sample_metadata)
    
    # Search for the embedded text
    results = await embedding_service.search(
        query=text,
        collection="text_chunks",
        limit=1
    )
    
    assert len(results) == 1
    assert results[0]["score"] > 0.5  # High similarity expected
    assert results[0]["metadata"]["chunk_id"] == sample_metadata["chunk_id"]

@pytest.mark.asyncio
async def test_embed_image(embedding_service, sample_image, sample_metadata):
    # Test embedding image
    await embedding_service.embed_image(sample_image, sample_metadata)
    
    # Search for the embedded image using text
    results = await embedding_service.search(
        query="an image",
        collection="image_chunks",
        limit=1
    )
    
    assert len(results) == 1
    assert "image_hash" in results[0]["metadata"]
    assert results[0]["metadata"]["chunk_id"] == sample_metadata["chunk_id"]

@pytest.mark.asyncio
async def test_search_with_filters(embedding_service, sample_metadata):
    text = "This is another test document for filtered search."
    
    # Embed multiple documents
    await embedding_service.embed_text(text, sample_metadata)
    await embedding_service.embed_text(
        "Different content",
        {**sample_metadata, "chunk_id": "different", "section": "conclusion"}
    )
    
    # Search with filters
    results = await embedding_service.search(
        query=text,
        collection="text_chunks",
        filter_conditions={"section": "introduction"},
        limit=1
    )
    
    assert len(results) == 1
    assert results[0]["metadata"]["section"] == "introduction"

def test_clip_text_embedding(embedding_service):
    text = "A test query for CLIP"
    embedding = embedding_service._get_clip_text_embedding(text)
    
    assert isinstance(embedding, list)
    assert len(embedding) == 512  # CLIP embedding size
    assert all(isinstance(x, float) for x in embedding)

def test_clip_image_embedding(embedding_service, sample_image):
    embedding = embedding_service._get_clip_image_embedding(sample_image)
    
    assert isinstance(embedding, list)
    assert len(embedding) == 512  # CLIP embedding size
    assert all(isinstance(x, float) for x in embedding)

@pytest.mark.asyncio
async def test_cross_modal_search(embedding_service, sample_image, sample_metadata):
    # Embed an image
    await embedding_service.embed_image(sample_image, sample_metadata)
    
    # Search with text query
    results = await embedding_service.search(
        query="a colorful image",
        collection="image_chunks",
        limit=1
    )
    
    assert len(results) == 1
    assert isinstance(results[0]["score"], float)
    assert 0 <= results[0]["score"] <= 1  # Normalized similarity score 