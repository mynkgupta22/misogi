# Content Creation Tool

A GUI-based content creation tool that helps content teams automate blog writing from idea capture to Medium publishing using local filesystem operations.

## Features

1. **Chat-Based Idea Capture**
   - Natural language interface for capturing content ideas
   - Structured storage of ideas with metadata
   - Local filesystem organization

2. **AI Content Generation**
   - OpenAI-powered content generation
   - Markdown formatting support
   - Local draft storage and management

3. **Content Review Dashboard**
   - File browser for content workspace
   - Preview and edit capabilities
   - Content status tracking

4. **Medium Publishing**
   - One-click publishing to Medium
   - Automatic metadata handling
   - Publication status tracking

## Setup

1. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file with your API keys:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   MEDIUM_API_KEY=your_medium_api_key_here
   MEDIUM_USER_ID=your_medium_user_id_here
   ```

4. Run the application:
   ```bash
   python src/main.py
   ```

## Usage

### Available Commands

1. Create new idea:
   ```
   Create idea: [title] | [description] | [target audience] | [keyword1, keyword2, ...]
   ```

2. Generate content:
   ```
   Generate content from: [idea-file-name]
   ```

3. Publish to Medium:
   ```
   Publish to Medium: [generated-file-name]
   ```

4. Show status:
   ```
   Show content status
   ```

### Example Workflow

1. Create a new content idea:
   ```
   Create idea: Writing Python GUIs | Best practices for creating desktop apps with PyQt6 | Python developers | PyQt6, GUI, desktop apps, Python
   ```

2. Generate content from the idea:
   ```
   Generate content from: 2024-03-19-writing-python-guis.json
   ```

3. Review the generated content in the file browser

4. Publish to Medium:
   ```
   Publish to Medium: 2024-03-19-writing-python-guis.md
   ```

## Directory Structure

```
content-workspace/
├── ideas/         # Stored content ideas
├── generated/     # AI-generated content
├── published/     # Published content with metadata
└── templates/     # Content templates
```

## Requirements

- Python 3.11+
- OpenAI API key
- Medium API key and user ID
- PyQt6 for GUI

## Development

The project is structured as follows:

```
src/
├── main.py              # Main application
├── gui/                 # GUI components
├── services/            # Core services
│   ├── openai_service.py
│   ├── file_service.py
│   └── medium_service.py
└── utils/              # Utility functions
```

## License

MIT License 