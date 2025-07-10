import os
import json
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask, render_template_string, request, jsonify
from services.openai_service import OpenAIService
from services.file_service import FileService
from services.medium_service import MediumService

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Initialize services
try:
    openai_service = OpenAIService()
    file_service = FileService()
    medium_service = MediumService()
except Exception as e:
    print(f"Error initializing services: {str(e)}")
    exit(1)

# HTML template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Content Creation Tool</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            display: flex;
            height: 100vh;
        }
        
        .file-browser {
            width: 300px;
            padding: 10px;
            border-right: 1px solid #ccc;
            overflow-y: auto;
        }
        
        .chat-interface {
            flex: 1;
            padding: 10px;
            display: flex;
            flex-direction: column;
        }
        
        .chat-history {
            flex: 1;
            border: 1px solid #ccc;
            padding: 10px;
            margin-bottom: 10px;
            overflow-y: auto;
        }
        
        .input-area {
            display: flex;
            gap: 10px;
        }
        
        input[type="text"] {
            flex: 1;
            padding: 5px;
        }
        
        button {
            padding: 5px 15px;
        }
        
        .file-item {
            cursor: pointer;
            padding: 5px;
            margin: 2px 0;
        }
        
        .file-item:hover {
            background-color: #f0f0f0;
        }
        
        .directory {
            font-weight: bold;
        }
    </style>
    <script>
        function sendMessage() {
            const input = document.getElementById('message-input');
            const message = input.value.trim();
            
            if (message) {
                fetch('/send_message', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ message: message })
                })
                .then(response => response.json())
                .then(data => {
                    appendMessage('You: ' + message);
                    appendMessage('Assistant: ' + data.response);
                    input.value = '';
                    refreshFileBrowser();
                });
            }
        }
        
        function appendMessage(message) {
            const chatHistory = document.getElementById('chat-history');
            const messageDiv = document.createElement('div');
            messageDiv.textContent = message;
            chatHistory.appendChild(messageDiv);
            chatHistory.scrollTop = chatHistory.scrollHeight;
        }
        
        function refreshFileBrowser() {
            fetch('/get_files')
            .then(response => response.json())
            .then(data => {
                const fileBrowser = document.getElementById('file-browser');
                fileBrowser.innerHTML = '';
                
                Object.entries(data).forEach(([dir, files]) => {
                    const dirDiv = document.createElement('div');
                    dirDiv.className = 'directory';
                    dirDiv.textContent = dir;
                    fileBrowser.appendChild(dirDiv);
                    
                    files.forEach(file => {
                        const fileDiv = document.createElement('div');
                        fileDiv.className = 'file-item';
                        fileDiv.textContent = file;
                        fileDiv.onclick = () => viewFile(dir + '/' + file);
                        fileBrowser.appendChild(fileDiv);
                    });
                });
            });
        }
        
        function viewFile(path) {
            fetch('/view_file', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ path: path })
            })
            .then(response => response.json())
            .then(data => {
                alert(data.content);
            });
        }
        
        // Initialize
        document.addEventListener('DOMContentLoaded', () => {
            refreshFileBrowser();
            appendMessage(`Welcome to Content Creation Tool! 🚀

Available commands:
1. Create new idea:
   "Create idea: [title] | [description] | [target audience] | [keyword1, keyword2, ...]"

2. Generate content:
   "Generate content from: [idea-file-name]"

3. Publish to Medium:
   "Publish to Medium: [generated-file-name]"

4. Show status:
   "Show content status"

Example:
Create idea: Writing Python GUIs | Best practices for creating web apps with Flask | Python developers | Flask, GUI, web apps, Python

Type your command to get started!`);
        });
    </script>
</head>
<body>
    <div class="file-browser" id="file-browser">
    </div>
    <div class="chat-interface">
        <div class="chat-history" id="chat-history">
        </div>
        <div class="input-area">
            <input type="text" id="message-input" placeholder="Type your message here..." onkeypress="if(event.key === 'Enter') sendMessage()">
            <button onclick="sendMessage()">Send</button>
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/send_message', methods=['POST'])
def send_message():
    message = request.json.get('message', '').strip()
    response = process_message(message)
    return jsonify({'response': response})

@app.route('/get_files', methods=['GET'])
def get_files():
    files = {
        'ideas': [f.name for f in Path('content/ideas').glob('*') if f.is_file()],
        'generated': [f.name for f in Path('content/generated').glob('*') if f.is_file()],
        'published': [f.name for f in Path('content/published').glob('*') if f.is_file()],
        'templates': [f.name for f in Path('content/templates').glob('*') if f.is_file()]
    }
    return jsonify(files)

@app.route('/view_file', methods=['POST'])
def view_file():
    path = request.json.get('path', '')
    try:
        with open(Path('content') / path, 'r') as f:
            content = f.read()
        return jsonify({'content': content})
    except Exception as e:
        return jsonify({'content': f"Error reading file: {str(e)}"})

def process_message(message: str) -> str:
    """Process the user's message and generate appropriate response"""
    try:
        if message.lower().startswith("create idea:"):
            return handle_create_idea(message[12:].strip())
        elif message.lower().startswith("generate content from:"):
            return handle_generate_content(message[20:].strip())
        elif message.lower().startswith("publish to medium:"):
            return handle_publish_medium(message[17:].strip())
        elif message.lower() == "show content status":
            return handle_show_status()
        else:
            return "I don't understand that command. Please use one of the available commands shown in the welcome message."
    except Exception as e:
        return f"Error processing command: {str(e)}"

def handle_create_idea(idea_str: str) -> str:
    """Handle idea creation command"""
    try:
        # Parse idea components
        parts = [p.strip() for p in idea_str.split("|")]
        if len(parts) != 4:
            raise ValueError("Please provide title, description, target audience, and keywords separated by |")
            
        title, description, target_audience, keywords = parts
        keywords = [k.strip() for k in keywords.split(",")]
        
        # Save idea
        idea_file = file_service.save_idea(title, description, keywords, target_audience)
        
        return f"Idea saved successfully! File: {idea_file}"
        
    except Exception as e:
        return f"Error creating idea: {str(e)}"

def handle_generate_content(idea_file: str) -> str:
    """Handle content generation command"""
    try:
        # Load idea file
        with open(Path("content/ideas") / idea_file, 'r') as f:
            idea_data = json.load(f)
            
        # Generate content
        content = openai_service.generate_content(idea_data)
        if not content:
            raise Exception("Failed to generate content")
            
        # Save generated content
        generated_file = file_service.save_generated_content(
            str(Path("content/ideas") / idea_file),
            content
        )
        
        return f"Content generated successfully! File: {generated_file}"
        
    except Exception as e:
        return f"Error generating content: {str(e)}"

def handle_publish_medium(generated_file: str) -> str:
    """Handle Medium publishing command"""
    try:
        file_path = Path("content/generated") / generated_file
        
        # Read the generated content
        with open(file_path, 'r') as f:
            content = f.read()
            
        # Get the title from the filename
        title = file_path.stem.split("-", 3)[-1].replace("-", " ").title()
        
        # Publish to Medium
        medium_url = medium_service.publish_post(title, content)
        if not medium_url:
            raise Exception("Failed to publish to Medium")
            
        # Move to published directory
        published_file = file_service.move_to_published(str(file_path), medium_url)
        
        return f"Content published successfully!\nMedium URL: {medium_url}\nLocal file: {published_file}"
        
    except Exception as e:
        return f"Error publishing to Medium: {str(e)}"

def handle_show_status() -> str:
    """Handle showing content status"""
    try:
        status = file_service.get_content_status()
        
        status_msg = "Content Status:\n\n"
        
        status_msg += "Ideas:\n"
        for idea in status["ideas"]:
            status_msg += f"- {idea['data']['title']} ({idea['file']})\n"
            
        status_msg += "\nGenerated Content:\n"
        for content in status["generated"]:
            status_msg += f"- {content['title']} ({content['file']})\n"
            
        status_msg += "\nPublished Content:\n"
        for content in status["published"]:
            url = content['metadata'].get('medium_url', 'Not available')
            status_msg += f"- {content['title']} ({content['file']})\n  Medium URL: {url}\n"
            
        return status_msg
        
    except Exception as e:
        return f"Error getting content status: {str(e)}"

def main():
    # Initialize content directories
    base_path = Path("content")
    dirs = ["ideas", "generated", "published", "templates"]
    for dir_name in dirs:
        (base_path / dir_name).mkdir(parents=True, exist_ok=True)
        
    # Run the Flask app
    app.run(debug=True)

if __name__ == "__main__":
    main() 