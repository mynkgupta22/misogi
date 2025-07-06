# HR Knowledge Assistant

An AI-powered assistant that helps employees quickly find information about company policies, benefits, and procedures from HR documents.

## Features

- Upload and process HR documents (PDF, DOCX)
- Natural language querying of HR policies
- Source citations for answers
- User-friendly web interface
- Fast and accurate responses

## Setup

1. Clone the repository
2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory and add your OpenAI API key:
```
OPENAI_API_KEY=your-api-key-here
```

## Running the Application

1. Start the FastAPI backend:
```bash
cd src
uvicorn main:app --reload
```

2. In a new terminal, start the Streamlit frontend:
```bash
cd src
streamlit run streamlit_app.py
```

3. Open your browser and navigate to:
- Frontend: http://localhost:8501
- API docs: http://localhost:8000/docs

## Usage

1. Upload HR documents using the file uploader in the sidebar
2. Ask questions about company policies in the main panel
3. Get instant answers with source citations

## Sample Questions

- How many vacation days do I get?
- What's the process for requesting parental leave?
- Can I work remotely and what are the guidelines?
- How do I enroll in health insurance?

## Project Structure

```
.
├── README.md
├── requirements.txt
├── .env
├── src/
│   ├── main.py              # FastAPI backend
│   ├── document_processor.py # Document processing logic
│   ├── query_handler.py     # Query handling logic
│   └── streamlit_app.py     # Streamlit frontend
├── db/                      # Vector store database
└── temp/                    # Temporary file storage
``` 