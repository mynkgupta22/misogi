# Medical Knowledge Assistant

A production-ready Medical Knowledge Assistant RAG pipeline for healthcare professionals to query medical literature, drug interactions, and clinical guidelines using OpenAI API with a comprehensive RAGAS evaluation framework.

## Features

- **RAG Pipeline**
  - Medical document ingestion from PubMed Central
  - Vector storage using Chroma
  - Semantic retrieval with OpenAI embeddings
  - Response generation with GPT-4

- **RAGAS Evaluation**
  - Context Precision
  - Faithfulness
  - Answer Relevancy
  - Real-time response validation
  - Quality thresholds enforcement

- **Safety Features**
  - Response safety verification
  - Source citation tracking
  - Medical disclaimer inclusion
  - RAGAS-based filtering

- **API Features**
  - RESTful endpoints
  - Query type specialization
  - Comprehensive response metadata
  - Health monitoring

## Setup

1. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create `.env` file with your OpenAI API key:
```
OPENAI_API_KEY=your_key_here
```

## Usage

1. Start the API server:
```bash
python src/main.py
```

2. The server will:
   - Download sample medical documents if none exist
   - Process and index the documents
   - Start the API at http://localhost:8000

3. API Endpoints:
   - `GET /`: Welcome message
   - `GET /health`: System health check
   - `POST /query`: Query medical knowledge
   - `GET /query_types`: List available query types
   - `GET /stats`: System statistics

4. Example Query:
```bash
curl -X POST "http://localhost:8000/query" \
     -H "Content-Type: application/json" \
     -d '{
           "text": "What are the common side effects of aspirin?",
           "query_type": "general_medical",
           "num_contexts": 5
         }'
```

## Project Structure

```
medical_rag/
├── src/
│   ├── api/                 # FastAPI endpoints
│   ├── document_processor/  # PDF processing
│   ├── vectorstore/        # Chroma management
│   ├── generation/         # GPT-4 integration
│   ├── evaluation/         # RAGAS evaluation
│   ├── utils/             # Utilities
│   └── config.py          # Configuration
├── data/
│   ├── raw/               # Original PDFs
│   ├── processed/         # Processed chunks
│   └── evaluation/        # RAGAS datasets
├── tests/                 # Test suite
└── requirements.txt       # Dependencies
```

## RAGAS Metrics

- **Faithfulness**: Measures response accuracy (threshold: 0.90)
- **Context Precision**: Measures retrieval relevance (threshold: 0.85)
- **Answer Relevancy**: Measures response applicability

## Query Types

1. Drug Interactions
2. Treatment Protocols
3. Diagnosis Guidelines
4. General Medical Information

## Safety Measures

1. RAGAS threshold validation
2. Safety prompt verification
3. Source citation requirements
4. Medical disclaimer inclusion

## Performance

- Response latency target: p95 < 3 seconds
- RAGAS evaluation overhead: ~1-2 seconds
- Retrieval optimization with metadata filtering

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License 