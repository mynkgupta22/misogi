from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from app.services.summarizer import SummarizationService

router = APIRouter()
summarizer = SummarizationService()

class SummaryRequest(BaseModel):
    document_id: Optional[str] = None
    section: Optional[str] = None
    document_ids: Optional[List[str]] = None
    summary_type: str = "executive"  # executive, bullet, trend

class ConceptMapRequest(BaseModel):
    document_id: Optional[str] = None
    section: Optional[str] = None

@router.post("/summarize/document")
async def summarize_document(request: SummaryRequest) -> Dict[str, Any]:
    """Generate a summary for a single document"""
    if not request.document_id:
        raise HTTPException(
            status_code=400,
            detail="document_id is required"
        )
    
    return await summarizer.summarize_document(
        document_id=request.document_id,
        summary_type=request.summary_type
    )

@router.post("/summarize/section")
async def summarize_section(request: SummaryRequest) -> Dict[str, Any]:
    """Generate a summary for a specific section"""
    if not request.section:
        raise HTTPException(
            status_code=400,
            detail="section is required"
        )
    
    return await summarizer.summarize_section(
        section=request.section,
        summary_type=request.summary_type
    )

@router.post("/summarize/cross-document")
async def summarize_across_documents(request: SummaryRequest) -> Dict[str, Any]:
    """Generate a summary across multiple documents"""
    if not request.document_ids or len(request.document_ids) < 2:
        raise HTTPException(
            status_code=400,
            detail="At least two document_ids are required"
        )
    
    return await summarizer.summarize_across_documents(
        document_ids=request.document_ids,
        summary_type=request.summary_type
    )

@router.post("/concepts/map")
async def generate_concept_map(request: ConceptMapRequest) -> Dict[str, Any]:
    """Generate a concept map for a document or section"""
    if not request.document_id and not request.section:
        raise HTTPException(
            status_code=400,
            detail="Either document_id or section is required"
        )
    
    return await summarizer.generate_concept_map(
        document_id=request.document_id,
        section=request.section
    ) 