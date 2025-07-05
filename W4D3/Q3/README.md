# RAG Chunking Strategy Visualizer

This project provides a web application for visualizing different text chunking strategies commonly used in RAG (Retrieval Augmented Generation) systems.

## Features

- PDF Upload & Text Extraction
- Multiple Chunking Strategies:
  - Fixed Size Chunking
  - Sentence-based Chunking
  - Paragraph-based Chunking
  - Sliding Window with Overlap
- Chunk Visualization
- Chunk Metadata Display

## Backend Setup

1. Create and activate virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
cd backend
pip install -r requirements.txt
```

3. Run the backend server:
```bash
cd backend
uvicorn app.main:app --reload
```

The backend will be available at http://localhost:8000

## API Endpoints

- `POST /upload`: Upload PDF file
  - Input: PDF file
  - Output: Extracted text

- `POST /chunk`: Chunk text using specified strategy
  - Input: 
    ```json
    {
      "text": "text to chunk",
      "strategy": "fixed|sentence|paragraph|sliding",
      "chunk_size": 500,
      "overlap": 50
    }
    ```
  - Output: Chunks and metadata

## Frontend Setup (To be completed)

The frontend setup is pending due to Node.js installation issues. Once Node.js is properly installed, we'll add React-based frontend implementation. 