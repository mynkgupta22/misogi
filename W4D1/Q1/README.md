# MCP Expert Chatbot

A Q&A chatbot that specializes in answering questions about Model Context Protocol (MCP). The chatbot provides information about MCP concepts, implementation patterns, best practices, and troubleshooting.

## Features

- Interactive chat interface
- Comprehensive MCP knowledge base
- Real-time responses
- Modern and responsive UI
- Easy to use and extend

## Setup

1. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

1. Start the Flask server:
```bash
python app.py
```

2. Open your web browser and navigate to:
```
http://localhost:5000
```

## Example Questions

You can ask the chatbot questions like:
- What is MCP?
- What are the benefits of using MCP?
- How do I implement MCP in my project?
- What are some common MCP issues?
- What are the best practices for MCP?

## Project Structure

```
.
├── app.py              # Flask backend application
├── requirements.txt    # Python dependencies
├── static/
│   └── styles.css     # CSS styles for the frontend
├── templates/
│   └── index.html     # HTML template for the chat interface
└── README.md          # This file
```

## Technologies Used

- Backend: Python with Flask
- Frontend: HTML, CSS, JavaScript
- Communication: REST API
- Styling: Custom CSS with modern design 