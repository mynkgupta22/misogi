import pytest
from app.services.document_processor import DocumentProcessor
from pathlib import Path
import os
import shutil

# Test data directory
TEST_DATA_DIR = Path("tests/test_data")

@pytest.fixture(scope="module")
def document_processor():
    return DocumentProcessor()

@pytest.fixture(scope="module")
def setup_test_files():
    # Create test directory and files
    TEST_DATA_DIR.mkdir(exist_ok=True)
    
    # Create a test text file
    with open(TEST_DATA_DIR / "test.txt", "w") as f:
        f.write("This is a test document.\nIt has multiple lines.\nFor testing purposes.")
    
    # Create a test image
    from PIL import Image
    import numpy as np
    
    # Create a simple test image
    img_array = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
    img = Image.fromarray(img_array)
    img.save(TEST_DATA_DIR / "test.jpg")
    
    yield
    
    # Cleanup
    shutil.rmtree(TEST_DATA_DIR)

@pytest.mark.asyncio
async def test_process_text_document(document_processor, setup_test_files):
    # Test processing a text document
    chunks = await document_processor._process_text_document(
        str(TEST_DATA_DIR / "test.txt"),
        ".txt"
    )
    
    assert len(chunks) > 0
    assert all(isinstance(chunk["content"], str) for chunk in chunks)
    assert all(chunk["type"] == "text" for chunk in chunks)
    
    # Check metadata
    for chunk in chunks:
        assert "chunk_id" in chunk["metadata"]
        assert "file_type" in chunk["metadata"]
        assert "source" in chunk["metadata"]
        assert "page" in chunk["metadata"]
        assert "section" in chunk["metadata"]
        assert "created_at" in chunk["metadata"]

@pytest.mark.asyncio
async def test_process_image(document_processor, setup_test_files):
    # Test processing an image
    chunks = await document_processor._process_image(
        str(TEST_DATA_DIR / "test.jpg"),
        ".jpg"
    )
    
    assert len(chunks) == 1
    assert isinstance(chunks[0]["content"], bytes)
    assert chunks[0]["type"] == "image"
    
    # Check metadata
    metadata = chunks[0]["metadata"]
    assert "chunk_id" in metadata
    assert "file_type" in metadata
    assert "source" in metadata
    assert "width" in metadata
    assert "height" in metadata
    assert "format" in metadata
    assert "created_at" in metadata

@pytest.mark.asyncio
async def test_process_document_invalid_type(document_processor):
    # Test processing an unsupported file type
    with pytest.raises(ValueError):
        await document_processor.process_document(
            "test.invalid",
            ".invalid"
        )

def test_generate_chunk_id(document_processor):
    # Test chunk ID generation
    text1 = "Test content"
    text2 = "Different content"
    
    id1 = document_processor._generate_chunk_id(text1)
    id2 = document_processor._generate_chunk_id(text2)
    id1_repeat = document_processor._generate_chunk_id(text1)
    
    # IDs should be strings
    assert isinstance(id1, str)
    assert isinstance(id2, str)
    
    # Same content should generate same ID
    assert id1 == id1_repeat
    
    # Different content should generate different IDs
    assert id1 != id2 