# AI Coding Agent Recommendation System

A sophisticated web application that analyzes programming tasks and recommends the best AI coding agents based on task requirements, complexity, and domain-specific needs.

## 🚀 Features

- **Natural Language Task Analysis**: Accepts detailed task descriptions and analyzes requirements
- **Intelligent Agent Matching**: Sophisticated scoring algorithm that matches task needs with agent capabilities
- **Comprehensive Agent Database**: 8 popular AI coding agents with detailed capabilities and system prompts
- **Beautiful Modern UI**: Responsive design with smooth animations and intuitive user experience
- **Real-time Recommendations**: Get top 3 agent recommendations with detailed justifications
- **Agent Explorer**: Browse all available agents with search and filtering capabilities

## 🛠️ Technology Stack

- **Backend**: Python Flask
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Styling**: Custom CSS with modern design patterns
- **Icons**: Font Awesome
- **Fonts**: Inter (Google Fonts)

## 📋 Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

## 🚀 Installation

1. **Clone or navigate to the project directory**:
   ```bash
   cd W3D3/Q2
   ```

2. **Install required dependencies**:
   ```bash
   pip install flask
   ```

3. **Run the application**:
   ```bash
   python app.py
   ```

4. **Open your browser and navigate to**:
   ```
   http://localhost:5000
   ```

## 📖 Usage Guide

### Getting Recommendations

1. **Describe Your Task**: Enter a detailed description of your programming task in the text area
2. **Submit**: Click "Get Recommendations" or press Ctrl/Cmd + Enter
3. **Review Analysis**: View the system's analysis of your task requirements
4. **Explore Recommendations**: See the top 3 recommended agents with match percentages and justifications

### Example Task Descriptions

- *"I need to build a REST API with Python Flask that handles user authentication and connects to a PostgreSQL database. The API should include JWT tokens and input validation."*
- *"I want to create a React frontend with TypeScript for a real-time chat application that connects to a WebSocket backend."*
- *"I need help debugging a complex algorithm in C++ that's causing memory leaks and performance issues."*
- *"I want to build a machine learning model using Python with pandas and scikit-learn for data analysis."*

### Browsing All Agents

1. Click "View All Agents" in the footer
2. Use the search bar to find specific agents or capabilities
3. Filter agents by capabilities using the filter buttons
4. Explore detailed information about each agent's strengths, weaknesses, and system prompts

## 🏗️ System Architecture

### Core Components

1. **Flask Application (`app.py`)**:
   - Main web server with REST API endpoints
   - Handles task submission and recommendation requests
   - Serves HTML templates and static files

2. **Recommendation Engine (`recommendation_engine.py`)**:
   - Sophisticated scoring algorithm
   - Task analysis and requirement extraction
   - Agent capability matching
   - Justification generation

3. **Agent Database (`agents_db.json`)**:
   - Comprehensive knowledge base of 8 AI coding agents
   - Detailed capabilities, strengths, weaknesses
   - System prompts and scoring weights
   - Use case recommendations

4. **Web Interface**:
   - Modern, responsive design
   - Real-time search and filtering
   - Interactive animations and transitions
   - Mobile-friendly layout

### Scoring Algorithm

The recommendation engine uses a multi-factor scoring system:

1. **Requirement Matching**: Analyzes task keywords and matches them with agent capabilities
2. **Complexity Assessment**: Considers task complexity and matches with appropriate agent strengths
3. **Domain Specialization**: Provides bonuses for domain-specific agents (AWS, web development, etc.)
4. **Language Detection**: Identifies programming languages and provides language-specific bonuses
5. **Context Analysis**: Considers code snippets, word count, and other contextual factors

## 🎯 Supported AI Coding Agents

1. **GitHub Copilot**: Real-time code completion with IDE integration
2. **Cursor**: AI-first code editor with advanced capabilities
3. **Replit Ghost**: Cloud-based collaborative coding assistant
4. **AWS CodeWhisperer**: AWS-integrated coding companion with security focus
5. **Claude Sonnet**: Advanced reasoning and problem-solving capabilities
6. **GPT-4**: Broad knowledge base with strong coding abilities
7. **Tabnine**: Privacy-focused local code completion
8. **Kite**: Python/JavaScript specialized assistant

## 🔧 Customization

### Adding New Agents

1. Edit `agents_db.json` and add a new agent entry
2. Include all required fields: id, name, description, capabilities, strengths, weaknesses, best_for, system_prompt, and score_weights
3. Restart the application

### Modifying Scoring Weights

1. Update the `score_weights` object in `agents_db.json`
2. Adjust weights for different capabilities (0.0 to 1.0)
3. The system will automatically use the new weights

### Customizing Task Analysis

1. Modify the keyword lists in `recommendation_engine.py`
2. Add new task types or domain keywords
3. Adjust complexity indicators as needed

## 🎨 UI Features

- **Responsive Design**: Works perfectly on desktop, tablet, and mobile
- **Smooth Animations**: CSS transitions and JavaScript animations
- **Interactive Elements**: Hover effects, loading states, and feedback
- **Accessibility**: Keyboard shortcuts and screen reader support
- **Modern Aesthetics**: Gradient backgrounds, card-based layout, and clean typography

## ⌨️ Keyboard Shortcuts

- **Ctrl/Cmd + Enter**: Submit task for recommendations
- **Escape**: Clear form or search
- **Ctrl/Cmd + F**: Focus search (on agents page)

## 🐛 Troubleshooting

### Common Issues

1. **Port already in use**: Change the port in `app.py` or kill the existing process
2. **Missing dependencies**: Ensure Flask is installed with `pip install flask`
3. **JSON errors**: Check that `agents_db.json` is valid JSON format
4. **Static files not loading**: Ensure the `static` folder structure is correct

### Debug Mode

Run the application in debug mode for detailed error messages:
```bash
export FLASK_ENV=development
python app.py
```

## 📁 Project Structure

```
W3D3/Q2/
├── app.py                 # Main Flask application
├── recommendation_engine.py # Core recommendation logic
├── agents_db.json         # Agent knowledge base
├── README.md             # This file
├── templates/            # HTML templates
│   ├── index.html       # Main page
│   └── agents.html      # Agents browser page
├── static/              # Static assets
│   ├── css/
│   │   └── style.css    # Main stylesheet
│   └── js/
│       ├── app.js       # Main page JavaScript
│       └── agents.js    # Agents page JavaScript
└── demo/                # Screenshots and demo materials
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is created for educational purposes as part of the AI coding course.

## 🙏 Acknowledgments

- Font Awesome for icons
- Google Fonts for typography
- Flask community for the web framework
- All AI coding agent providers for their innovative tools

---

**Built with ❤️ for developers who want to choose the right AI coding assistant for their tasks.** 