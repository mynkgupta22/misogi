# SaaS Support System with Local RAG Pipeline

A customer support system that uses local LLMs (via Ollama) with intent detection and RAG (Retrieval-Augmented Generation) to provide accurate responses to user queries.

## Features

- Intent classification for technical, billing, and feature requests
- Local LLM support via Ollama with OpenAI fallback
- RAG pipeline with ChromaDB for context retrieval
- Evaluation metrics for response quality
- Concurrent request handling with queue management
- Simple web UI for testing

## Prerequisites

- Python 3.10+
- [Ollama](https://ollama.ai/) installed and running
- Node.js and npm (for frontend)

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd saas-support
```

2. Set up the backend:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
pip install -r requirements.txt
```

3. Generate sample documents:
```bash
python app/data/generate_sample_docs.py
```

4. Start Ollama and pull the Llama2 model:
```bash
ollama pull llama2
```

5. Start the backend server:
```bash
python app/main.py
```

The server will start at `http://localhost:8000`

## API Endpoints

### POST /api/query
Process a user query through the RAG pipeline.

Request:
```json
{
    "text": "How do I integrate the API?"
}
```

Response:
```json
{
    "intent": "technical",
    "confidence": 0.85,
    "response": "Here's how to integrate our API...",
    "context": "Relevant documentation...",
    "metrics": {
        "response_relevance": 0.92,
        "context_utilization": 0.78,
        "intent_confidence": 0.85,
        "processing_time": 1.23
    }
}
```

### POST /api/documents
Add new documents to the knowledge base.

Request:
```json
{
    "documents": [
        {
            "content": "Document content...",
            "metadata": {
                "title": "API Guide",
                "type": "documentation"
            }
        }
    ],
    "intent": "technical"
}
```

## Testing

Run the test suite:
```bash
pytest tests/
```

## Evaluation Metrics

The system tracks several metrics:
- Intent classification accuracy
- Response relevance (cosine similarity)
- Context utilization score
- Processing time
- Token usage

## Architecture

1. **Intent Detection**
   - Uses sentence transformers for semantic similarity
   - Zero-shot classification with example queries
   - Confidence threshold for fallback handling

2. **RAG Pipeline**
   - ChromaDB for vector storage
   - Intent-based collection management
   - Configurable retrieval parameters

3. **LLM Integration**
   - Primary: Local Llama2 via Ollama
   - Fallback: OpenAI GPT-3.5
   - Concurrent request handling

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License 