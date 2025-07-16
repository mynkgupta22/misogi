from typing import List, Dict, Any, Tuple
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import (
    PyPDFLoader,
    Docx2txtLoader,
    UnstructuredMarkdownLoader,
    CSVLoader
)
from PIL import Image
import io
import hashlib
import os
from datetime import datetime

class DocumentProcessor:
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
    
    async def process_document(self, file_path: str, file_type: str) -> List[Dict[str, Any]]:
        """Process document and return chunks with metadata"""
        if file_type in ['.pdf', '.docx', '.md', '.csv']:
            return await self._process_text_document(file_path, file_type)
        elif file_type in ['.jpg', '.jpeg', '.png']:
            return await self._process_image(file_path, file_type)
        else:
            raise ValueError(f"Unsupported file type: {file_type}")

    async def _process_text_document(self, file_path: str, file_type: str) -> List[Dict[str, Any]]:
        """Process text-based documents"""
        # Select appropriate loader
        if file_type == '.pdf':
            loader = PyPDFLoader(file_path)
        elif file_type == '.docx':
            loader = Docx2txtLoader(file_path)
        elif file_type == '.md':
            loader = UnstructuredMarkdownLoader(file_path)
        elif file_type == '.csv':
            loader = CSVLoader(file_path)
        
        # Load and split document
        documents = loader.load()
        chunks = []
        
        for doc in documents:
            doc_chunks = self.text_splitter.split_text(doc.page_content)
            
            for i, chunk in enumerate(doc_chunks):
                chunk_id = self._generate_chunk_id(chunk)
                metadata = {
                    "chunk_id": chunk_id,
                    "file_type": file_type,
                    "source": os.path.basename(file_path),
                    "page": doc.metadata.get("page", 1),
                    "section": f"chunk_{i+1}",
                    "created_at": datetime.utcnow().isoformat(),
                    "chunk_index": i,
                    "total_chunks": len(doc_chunks)
                }
                
                chunks.append({
                    "content": chunk,
                    "metadata": metadata,
                    "type": "text"
                })
        
        return chunks

    async def _process_image(self, file_path: str, file_type: str) -> List[Dict[str, Any]]:
        """Process image files"""
        with Image.open(file_path) as img:
            # Convert image to bytes
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format=img.format)
            img_byte_arr = img_byte_arr.getvalue()
            
            chunk_id = self._generate_chunk_id(img_byte_arr)
            metadata = {
                "chunk_id": chunk_id,
                "file_type": file_type,
                "source": os.path.basename(file_path),
                "width": img.width,
                "height": img.height,
                "format": img.format,
                "created_at": datetime.utcnow().isoformat()
            }
            
            return [{
                "content": img_byte_arr,
                "metadata": metadata,
                "type": "image"
            }]

    def _generate_chunk_id(self, content: Any) -> str:
        """Generate a unique ID for a chunk"""
        if isinstance(content, str):
            content = content.encode()
        elif isinstance(content, bytes):
            pass
        else:
            content = str(content).encode()
            
        return hashlib.sha256(content).hexdigest()[:16] 