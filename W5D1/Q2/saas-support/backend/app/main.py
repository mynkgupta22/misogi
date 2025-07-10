from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Optional, List, Any
import time

from app.models.intent_classifier import IntentClassifier
from app.models.llm_manager import LLMManager
from app.models.rag_pipeline import RAGPipeline
from app.core.config import settings

# Initialize components
app = FastAPI(title=settings.APP_NAME)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React development server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
intent_classifier = IntentClassifier()
llm_manager = LLMManager()
rag_pipeline = RAGPipeline()

class Query(BaseModel):
    text: str

class Document(BaseModel):
    content: str
    metadata: Dict[str, Any]

class DocumentUpload(BaseModel):
    documents: List[Document]
    intent: str

class Response(BaseModel):
    intent: str
    confidence: float
    response: str
    context: str
    metrics: Dict[str, float]
    processing_time: float

@app.post("/api/query", response_model=Response)
async def process_query(query: Query):
    start_time = time.time()
    
    try:
        # 1. Classify intent
        intent, confidence = intent_classifier.classify(query.text)
        
        # 2. Get relevant context
        context = rag_pipeline.get_relevant_context(query.text, intent)
        
        # 3. Generate response
        response = await llm_manager.generate_response(query.text, context, intent)
        
        # 4. Evaluate
        intent_metrics = intent_classifier.evaluate_response(query.text, response, intent)
        retrieval_metrics = rag_pipeline.evaluate_retrieval(query.text, context, intent)
        
        # Combine metrics
        metrics = {
            **intent_metrics,
            **retrieval_metrics,
            "processing_time": time.time() - start_time
        }
        
        return Response(
            intent=intent,
            confidence=confidence,
            response=response,
            context=context,
            metrics=metrics,
            processing_time=time.time() - start_time
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/documents")
async def add_documents(upload: DocumentUpload):
    try:
        # Convert to list of dictionaries
        documents = [doc.dict() for doc in upload.documents]
        
        # Add documents to RAG pipeline
        rag_pipeline.add_documents(documents, upload.intent)
        
        return {"message": f"Successfully added {len(documents)} documents"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "components": {
            "intent_classifier": True,
            "llm_manager": True,
            "rag_pipeline": True
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 