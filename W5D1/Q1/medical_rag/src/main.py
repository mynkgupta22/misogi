"""
Main script to run the Medical Knowledge Assistant API.
"""
import uvicorn
from pathlib import Path
from src.document_processor.pdf_processor import MedicalTextProcessor
from src.vectorstore.chroma_manager import ChromaManager
from src.utils.data_downloader import download_sample_documents
from src.config import RAW_DATA_DIR, API_HOST, API_PORT

def main():
    """Initialize and run the Medical Knowledge Assistant."""
    print("Initializing Medical Knowledge Assistant...")
    
    # Initialize components
    document_processor = MedicalTextProcessor()
    vector_store = ChromaManager()
    
    # Check if we have documents
    if not any(Path(RAW_DATA_DIR).glob("*.txt")):
        print("No documents found. Downloading sample documents...")
        file_paths = download_sample_documents()
    else:
        file_paths = list(Path(RAW_DATA_DIR).glob("*.txt"))
    
    # Process documents
    print("Processing documents...")
    documents = document_processor.process_documents([Path(f) for f in file_paths])
    
    # Store in vector store
    print("Storing documents in vector store...")
    vector_store.add_documents(documents)
    
    # Start API server
    print(f"Starting API server at http://{API_HOST}:{API_PORT}")
    uvicorn.run("src.api.endpoints:app", host=API_HOST, port=API_PORT)

if __name__ == "__main__":
    main() 