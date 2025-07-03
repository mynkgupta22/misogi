from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

# MCP Knowledge Base
mcp_knowledge = {
    "general": {
        "what is mcp": "Model Context Protocol (MCP) is a standardized protocol for communication between AI models and development environments. It enables seamless integration of AI capabilities into applications while maintaining context and state.",
        "benefits of mcp": "MCP offers several benefits: 1) Standardized communication between AI and applications, 2) Maintains context across interactions, 3) Enables stateful conversations, 4) Supports multiple model providers, 5) Improves development workflow.",
        "when to use mcp": "Use MCP when you need: 1) AI-powered features in your application, 2) Consistent model interactions, 3) Context preservation across calls, 4) Integration with multiple AI providers."
    },
    "implementation": {
        "how to implement mcp": "To implement MCP: 1) Set up an MCP server, 2) Configure model providers, 3) Define context handlers, 4) Implement API endpoints, 5) Handle state management.",
        "mcp server setup": "Basic MCP server setup involves: 1) Installing dependencies, 2) Configuring server settings, 3) Setting up authentication, 4) Implementing required endpoints.",
        "best practices": "MCP best practices: 1) Use secure connections, 2) Implement proper error handling, 3) Manage context efficiently, 4) Monitor performance, 5) Regular maintenance."
    },
    "troubleshooting": {
        "common issues": "Common MCP issues: 1) Connection problems, 2) Authentication errors, 3) Context loss, 4) Performance bottlenecks, 5) Integration conflicts.",
        "debugging tips": "Debug MCP by: 1) Checking logs, 2) Verifying configurations, 3) Testing connections, 4) Monitoring resource usage, 5) Validating context flow."
    }
}

def find_best_match(query):
    query = query.lower()
    best_score = 0
    best_answer = "I'm sorry, I don't have specific information about that. Could you try rephrasing your question?"
    
    for category in mcp_knowledge:
        for q, a in mcp_knowledge[category].items():
            # Simple word matching score
            score = sum(word in query for word in q.split())
            if score > best_score:
                best_score = score
                best_answer = a
    
    return best_answer

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '').lower()
    
    response = find_best_match(user_message)
    
    return jsonify({
        'response': response
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000) 