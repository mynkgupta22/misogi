from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import shutil
from typing import Optional

from document_processor import DocumentProcessor
from query_handler import QueryHandler

app = FastAPI(title="HR Knowledge Assistant")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize document processor
doc_processor = DocumentProcessor()
query_handler: Optional[QueryHandler] = None

class Query(BaseModel):
    text: str

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """Upload and process a document"""
    try:
        # Create temp directory if it doesn't exist
        os.makedirs("temp", exist_ok=True)
        
        # Save file temporarily
        file_path = f"temp/{file.filename}"
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Process and store document
        global query_handler
        vectorstore = doc_processor.process_file(file_path)
        query_handler = QueryHandler(vectorstore)
        
        # Clean up
        os.remove(file_path)
        
        return {"message": "Document processed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query")
async def query(query: Query):
    """Query the knowledge base"""
    if not query_handler:
        vectorstore = doc_processor.get_vectorstore()
        if not vectorstore:
            raise HTTPException(
                status_code=400,
                detail="No documents have been uploaded yet"
            )
        global query_handler
        query_handler = QueryHandler(vectorstore)
    
    try:
        response = query_handler.get_response(query.text)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 