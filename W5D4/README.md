# Multimodal Research Assistant

A production-ready multimodal RAG system that can process and reason over complex documents containing text, images, tables, charts, and code snippets.

## MVP Features

- Support for multiple file formats:
  - PDF
  - DOCX
  - Markdown
  - Images
  - CSV
- Text and Image processing capabilities
- Streamlit-based user interface
- FastAPI backend with authentication
- Qdrant vector database for efficient similarity search

## Project Structure

```
.
├── backend/
│   ├── app/
│   │   ├── api/        # API endpoints
│   │   ├── core/       # Core configurations
│   │   ├── db/         # Database models and connections
│   │   ├── models/     # Pydantic models
│   │   ├── schemas/    # Database schemas
│   │   └── services/   # Business logic
│   └── requirements.txt
├── frontend/
│   ├── src/           # Streamlit frontend code
│   └── requirements.txt
└── README.md

## Setup Instructions

1. Clone the repository
2. Set up the backend:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Set up the frontend:
   ```bash
   cd frontend
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   pip install -r requirements.txt
   ```

4. Create a .env file in the backend directory with the following variables:
   ```
   DATABASE_URL=sqlite:///./app.db
   SECRET_KEY=your-secret-key
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

5. Start the backend server:
   ```bash
   cd backend
   uvicorn app.main:app --reload
   ```

6. Start the frontend:
   ```bash
   cd frontend
   streamlit run src/main.py
   ```

## Features

- Document Processing:
  - Text extraction from multiple file formats
  - Image processing and analysis
  - Structured data handling (CSV)
  
- Search & Retrieval:
  - Vector similarity search using Qdrant
  - Hybrid search combining metadata and semantic search
  
- User Interface:
  - Document upload and management
  - Interactive query interface
  - Real-time search results
  - Document visualization

## Tech Stack

- Backend:
  - FastAPI
  - SQLAlchemy
  - Pydantic
  - Unstructured (document processing)
  - Sentence Transformers
  
- Frontend:
  - Streamlit
  
- Database:
  - SQLite (user data)
  - Qdrant (vector store)

## Contributing

Please read CONTRIBUTING.md for details on our code of conduct and the process for submitting pull requests.
