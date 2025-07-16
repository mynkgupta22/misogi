from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from app.services.query_engine import QueryEngine

router = APIRouter()
query_engine = QueryEngine()

class ChatQuery(BaseModel):
    query: str
    use_decomposition: bool = False
    filters: Optional[Dict[str, Any]] = None

class ChatResponse(BaseModel):
    answer: str
    sources: List[Dict[str, Any]]
    subqueries: Optional[List[Dict[str, Any]]] = None

@router.post("/query", response_model=ChatResponse)
async def process_query(chat_query: ChatQuery) -> ChatResponse:
    """
    Process a chat query using the RAG pipeline
    """
    try:
        if chat_query.use_decomposition:
            response = await query_engine.decomposed_query(
                query=chat_query.query,
                filter_conditions=chat_query.filters
            )
        else:
            response = await query_engine.simple_query(
                query=chat_query.query,
                filter_conditions=chat_query.filters
            )
        
        return ChatResponse(
            answer=response["answer"],
            sources=response["sources"],
            subqueries=response.get("subqueries")
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing query: {str(e)}"
        ) 