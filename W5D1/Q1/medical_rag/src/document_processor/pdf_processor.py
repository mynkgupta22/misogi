"""
Text processing module for medical documents.
"""
from pathlib import Path
from typing import List, Dict, Optional
from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.config import CHUNK_SIZE, CHUNK_OVERLAP

class MedicalTextProcessor:
    """Process medical text documents for RAG pipeline."""
    
    def __init__(self):
        """Initialize the medical text processor."""
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
            separators=["\n\n", "\n", ".", " ", ""]
        )
    
    def process_document(self, file_path: Path) -> List[Dict[str, str]]:
        """
        Process a single text document.
        
        Args:
            file_path: Path to the text file
            
        Returns:
            List of chunks with metadata
        """
        # Read text file
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
        
        # Split text into chunks
        chunks = self.text_splitter.split_text(text)
        
        # Create documents with metadata
        documents = []
        for i, chunk in enumerate(chunks):
            doc = {
                'text': chunk,
                'metadata': {
                    'source': str(file_path),
                    'chunk_id': i,
                    'total_chunks': len(chunks)
                }
            }
            documents.append(doc)
        
        return documents
    
    def process_documents(self, file_paths: List[Path]) -> List[Dict[str, str]]:
        """
        Process multiple text documents.
        
        Args:
            file_paths: List of paths to text files
            
        Returns:
            List of chunks with metadata
        """
        all_documents = []
        for file_path in file_paths:
            try:
                documents = self.process_document(file_path)
                all_documents.extend(documents)
            except Exception as e:
                print(f"Error processing {file_path}: {str(e)}")
                continue
        
        return all_documents 