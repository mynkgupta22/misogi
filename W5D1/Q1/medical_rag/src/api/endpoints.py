"""
FastAPI endpoints for the medical RAG system.
"""
from typing import List, Dict, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.vectorstore.chroma_manager import ChromaManager
from src.generation.medical_llm import MedicalResponseGenerator
from src.evaluation.ragas_evaluator import RAGASEvaluator
from src.config import QUERY_TYPES

app = FastAPI(
    title="Medical Knowledge Assistant API",
    description="API for querying medical literature with RAGAS evaluation",
    version="1.0.0"
)

# Initialize components
vector_store = ChromaManager()
generator = MedicalResponseGenerator()
evaluator = RAGASEvaluator()

class Query(BaseModel):
    """Query request model."""
    text: str
    query_type: Optional[str] = QUERY_TYPES["GENERAL_MEDICAL"]
    num_contexts: Optional[int] = 5

class Response(BaseModel):
    """Response model with evaluation metrics."""
    answer: str
    query_type: str
    sources: List[str]
    evaluation: Dict
    safety_check: Dict

@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Medical Knowledge Assistant API"}

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    try:
        # Check vector store
        stats = vector_store.get_collection_stats()
        return {
            "status": "healthy",
            "vector_store": stats
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query", response_model=Response)
async def query_medical_knowledge(query: Query):
    """
    Query medical knowledge with RAGAS evaluation.
    
    Args:
        query: Query request
        
    Returns:
        Response with answer, sources, and evaluation metrics
    """
    try:
        # Retrieve relevant documents
        documents = vector_store.similarity_search(
            query=query.text,
            n_results=query.num_contexts
        )
        
        # Generate response
        response = generator.generate_response(
            query=query.text,
            documents=documents,
            query_type=query.query_type
        )
        
        # Perform safety check
        safety_check = generator.generate_safety_check(response["answer"])
        
        # Evaluate response
        evaluation = evaluator.evaluate_response(
            query=query.text,
            response=response["answer"],
            contexts=[doc["text"] for doc in documents]
        )
        
        return Response(
            answer=response["answer"],
            query_type=response["query_type"],
            sources=response["sources"],
            evaluation=evaluation,
            safety_check=safety_check
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/query_types")
async def get_query_types():
    """Get available query types."""
    return {"query_types": list(QUERY_TYPES.values())}

@app.get("/stats")
async def get_stats():
    """Get system statistics."""
    try:
        vector_store_stats = vector_store.get_collection_stats()
        return {
            "vector_store": vector_store_stats,
            "query_types": list(QUERY_TYPES.values())
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 