import json
import os
from typing import Dict, Any, List
from fastmcp import FastMCP, Context
from utils import analyze_text, get_sentiment, extract_keywords

app = FastMCP()

# Get the directory where server.py is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOCUMENTS_PATH = os.path.join(BASE_DIR, 'documents.json')

# Load documents from JSON file
with open(DOCUMENTS_PATH, 'r') as f:
    DOCUMENTS = json.load(f)['documents']

# In-memory document storage (dictionary for faster lookups)
DOCUMENTS_DICT = {doc['id']: doc for doc in DOCUMENTS}

@app.tool("analyze_document")
async def analyze_document(document_id: str, ctx: Context) -> Dict[str, Any]:
    """Analyze a specific document by ID"""
    if not document_id or document_id not in DOCUMENTS_DICT:
        ctx.error(f"Document {document_id} not found")
        return {"error": "Document not found"}
    
    document = DOCUMENTS_DICT[document_id]
    analysis = analyze_text(document['content'])
    
    return {
        "document": document,
        "analysis": analysis
    }

@app.tool("get_sentiment")
async def analyze_sentiment(text: str, ctx: Context) -> Dict[str, str]:
    """Analyze sentiment of provided text"""
    if not text:
        ctx.error("No text provided")
        return {"error": "No text provided"}
    
    sentiment = get_sentiment(text)
    return {"sentiment": sentiment}

@app.tool("extract_keywords")
async def get_keywords(text: str, ctx: Context, limit: int = 5) -> Dict[str, Any]:
    """Extract keywords from provided text"""
    if not text:
        ctx.error("No text provided")
        return {"error": "No text provided"}
    
    try:
        limit = int(limit)
    except (TypeError, ValueError):
        ctx.error("Invalid limit value")
        return {"error": "Invalid limit value"}
    
    keywords = extract_keywords(text, limit)
    return {"keywords": keywords}

@app.tool("add_document")
async def add_document(id: str, title: str, content: str, ctx: Context) -> Dict[str, Any]:
    """Add a new document to the collection"""
    document_data = {
        "id": id,
        "title": title,
        "content": content
    }
    
    if document_data['id'] in DOCUMENTS_DICT:
        ctx.error(f"Document ID {id} already exists")
        return {"error": "Document ID already exists"}
    
    DOCUMENTS.append(document_data)
    DOCUMENTS_DICT[document_data['id']] = document_data
    
    # Save the updated documents to file
    with open(DOCUMENTS_PATH, 'w') as f:
        json.dump({"documents": DOCUMENTS}, f, indent=4)
    
    return {"message": "Document added successfully", "document": document_data}

@app.tool("search_documents")
async def search_documents(query: str, ctx: Context) -> Dict[str, Any]:
    """Search documents by keyword"""
    if not query:
        ctx.error("No search query provided")
        return {"error": "No search query provided"}
    
    # Simple keyword matching in title and content
    results = []
    query = query.lower()
    for doc in DOCUMENTS:
        if (query in doc['title'].lower() or 
            query in doc['content'].lower()):
            results.append(doc)
    
    return {
        "query": query,
        "results": results,
        "count": len(results)
    }

if __name__ == "__main__":
    app.run() 