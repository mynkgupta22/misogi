# Plagiarism Detector - Semantic Similarity Analyzer

A web-based tool that detects plagiarism and analyzes semantic similarity between multiple text inputs using both sentence-transformers and OpenAI embeddings.

## Features

- Multiple text input support (up to 5 texts)
- Two embedding models:
  - Sentence Transformers (offline, free)
  - OpenAI Embeddings (requires API key)
- Interactive similarity matrix visualization
- Highlights high-similarity pairs (>80%)
- Real-time analysis

## Setup

1. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. For OpenAI embeddings (optional):
   - Create a `.env` file in the project root
   - Add your OpenAI API key: `OPENAI_API_KEY=your_api_key_here`

## Running the Application

1. Start the FastAPI server:
```bash
uvicorn app.main:app --reload
```

2. Open your browser and navigate to:
```
http://localhost:8000
```

## Usage

1. Enter at least two texts in the input boxes
2. Add more text boxes using the "Add Text Input" button
3. Select the embedding model:
   - Sentence Transformers (default, works offline)
   - OpenAI Embeddings (requires API key)
4. Click "Analyze" to compare texts
5. View results in the similarity matrix and plagiarism detection section

## Notes

- The similarity threshold for plagiarism detection is set to 80%
- OpenAI embeddings require an API key and may incur costs
- Sentence Transformers work offline and are free to use 