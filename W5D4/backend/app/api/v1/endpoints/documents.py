from fastapi import APIRouter, UploadFile, File, HTTPException, Query
from typing import List, Optional, Dict, Any
from app.services.document_processor import DocumentProcessor
from app.services.embeddings import MultimodalEmbeddingService
import os
from pathlib import Path

from typing import List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.auth import fastapi_users
from app.models.user import User
from app.models.document import Document
from app.db.session import get_async_session
from app.schemas.document import DocumentCreate, DocumentResponse, DocumentUpdate

router = APIRouter()
document_processor = DocumentProcessor()
embedding_service = MultimodalEmbeddingService()

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

current_active_user = fastapi_users.current_user(active=True)

@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    section: Optional[str] = Query(None, description="Document section or category")
) -> Dict[str, Any]:
    """
    Upload and process a document for indexing
    """
    # Validate file type
    file_extension = os.path.splitext(file.filename)[1].lower()
    supported_extensions = ['.pdf', '.docx', '.md', '.csv', '.jpg', '.jpeg', '.png']
    
    if file_extension not in supported_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type. Supported types: {', '.join(supported_extensions)}"
        )
    
    # Save file temporarily
    file_path = UPLOAD_DIR / file.filename
    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)
    
    try:
        # Process document
        chunks = await document_processor.process_document(
            str(file_path),
            file_extension
        )
        
        # Index chunks
        for chunk in chunks:
            if chunk["type"] == "text":
                await embedding_service.embed_text(
                    text=chunk["content"],
                    metadata=chunk["metadata"]
                )
            else:  # image
                await embedding_service.embed_image(
                    image_data=chunk["content"],
                    metadata=chunk["metadata"]
                )
        
        return {
            "message": "Document processed successfully",
            "filename": file.filename,
            "chunks_processed": len(chunks)
        }
    
    finally:
        # Clean up temporary file
        os.remove(file_path)

@router.get("/search")
async def search_documents(
    query: str,
    collection: str = Query("text_chunks", enum=["text_chunks", "image_chunks"]),
    file_type: Optional[str] = Query(None, description="Filter by file type"),
    source: Optional[str] = Query(None, description="Filter by source document"),
    section: Optional[str] = Query(None, description="Filter by section"),
    limit: int = Query(5, ge=1, le=20)
) -> List[Dict[str, Any]]:
    """
    Search documents with metadata filtering
    """
    # Prepare filter conditions
    filter_conditions = {}
    if file_type:
        filter_conditions["file_type"] = file_type
    if source:
        filter_conditions["source"] = source
    if section:
        filter_conditions["section"] = section
    
    results = await embedding_service.search(
        query=query,
        collection=collection,
        filter_conditions=filter_conditions if filter_conditions else None,
        limit=limit
    )
    
    return results 

@router.get("/my-documents", response_model=List[DocumentResponse])
async def get_user_documents(
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
):
    """Get all documents owned by the current user"""
    query = select(Document).where(Document.owner_id == user.id)
    result = await session.execute(query)
    documents = result.scalars().all()
    return documents

@router.post("/documents", response_model=DocumentResponse)
async def create_document(
    title: str,
    file: UploadFile = File(...),
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
):
    """Upload a new document"""
    # Save file logic here
    document = Document(
        title=title,
        file_path=f"uploads/{file.filename}",  # Implement proper file storage
        file_type=file.content_type,
        owner_id=user.id
    )
    session.add(document)
    await session.commit()
    await session.refresh(document)
    return document

@router.delete("/documents/{document_id}")
async def delete_document(
    document_id: int,
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
):
    """Delete a document owned by the user"""
    query = select(Document).where(
        Document.id == document_id,
        Document.owner_id == user.id
    )
    result = await session.execute(query)
    document = result.scalar_one_or_none()
    
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    await session.delete(document)
    await session.commit()
    return {"message": "Document deleted successfully"} 