# Adaptive Prompt Optimizer

An intelligent tool that analyzes and optimizes prompts for specific AI coding tools, providing tailored recommendations based on each tool's capabilities and best practices.

## 🚀 Features

### Core Functionality
- **Natural Language Task Input**: Accept prompts in plain English
- **Task Analysis**: Analyze prompt intent, complexity, and requirements
- **Tool-Specific Optimization**: Generate optimized prompts for 6+ AI coding tools
- **Before/After Comparison**: Visual comparison with detailed explanations
- **Web Interface**: Modern, responsive web application

### Supported AI Coding Tools
1. **GitHub Copilot** - AI-powered code completion
2. **Cursor** - AI-first code editor
3. **Replit Ghost** - Online AI coding assistant
4. **AWS CodeWhisperer** - AWS-integrated coding companion
5. **Claude Sonnet** - Advanced reasoning AI assistant
6. **GPT-4** - Comprehensive language model

### Optimization Strategies
Each tool has specialized optimization strategies:
- **Context Enhancement**: Add relevant context and environment details
- **Specificity Improvement**: Make requirements more specific and detailed
- **Tool-Specific Techniques**: Leverage each tool's unique capabilities
- **Best Practices Integration**: Apply industry-standard practices

## 📁 Project Structure

```
W3D3/Q3/
├── app.py                      # Main Flask application
├── tool_analysis.json          # Tool capabilities database
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── optimizers/                 # Tool-specific optimization modules
│   ├── prompt_optimizer.py     # Main optimization engine
│   └── tool_optimizers.py      # Individual tool optimizers
├── templates/                  # HTML templates
│   ├── index.html             # Main interface
│   └── tools.html             # Tools overview page
└── static/                    # Static assets
    ├── css/
    │   └── style.css          # Modern styling
    └── js/
        ├── app.js             # Main application logic
        └── tools.js           # Tools page functionality
```

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Installation Steps

1. **Clone or navigate to the project directory**
   ```bash
   cd W3D3/Q3
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Access the web interface**
   - Open your browser and go to: `http://localhost:8081`
   - The API endpoints will be available at the same host

## 🎯 Usage

### Web Interface

1. **Enter Your Prompt**
   - Describe what you want to build or accomplish
   - Be as specific as possible about your requirements

2. **Select Target Tool**
   - Choose from the dropdown of supported AI coding tools
   - Each tool has different optimization strategies

3. **Optimize Prompt**
   - Click "Optimize Prompt" to get tool-specific optimization
   - Or click "Analyze Only" to see prompt analysis without optimization

4. **Review Results**
   - View the before/after comparison
   - Read explanations of applied optimizations
   - Check the improvement score
   - Copy the optimized prompt

### API Endpoints

#### Optimize Prompt
```http
POST /optimize
Content-Type: application/json

{
    "base_prompt": "Create a function to sort a list",
    "target_tool": "github_copilot"
}
```

#### Analyze Prompt
```http
POST /api/analyze
Content-Type: application/json

{
    "base_prompt": "Create a function to sort a list"
}
```

#### Get All Tools
```http
GET /api/tools
```

#### View Tools Page
```http
GET /tools
```

## 🔧 How It Works

### 1. Prompt Analysis
The system analyzes prompts using keyword-based detection:
- **Complexity**: Simple, Medium, Complex
- **Intent**: Code generation, completion, debugging, refactoring, etc.
- **Languages**: Python, JavaScript, Java, C++, Go, Rust
- **Domains**: Web development, mobile, data science, cloud computing, etc.

### 2. Tool-Specific Optimization
Each tool has specialized optimization strategies:

#### GitHub Copilot
- Adds language specification if missing
- Improves function/class naming
- Includes type hints and context

#### Cursor
- Breaks down complex tasks into steps
- Adds comprehensive requirements
- Includes architecture context

#### AWS CodeWhisperer
- Emphasizes AWS services and security
- Adds cloud-native patterns
- Includes monitoring and logging

#### Claude Sonnet
- Adds reasoning requirements
- Includes step-by-step breakdown
- Emphasizes documentation

#### GPT-4
- Leverages broad knowledge base
- Provides multiple approaches
- Includes best practices

#### Replit Ghost
- Adds educational context
- Includes deployment considerations
- Emphasizes collaboration

### 3. Improvement Scoring
The system calculates improvement scores based on:
- Length optimization
- Clarity enhancement
- Specificity improvement
- Context addition

## 📊 Example Optimizations

### Before (Original Prompt)
```
"write a function to sort a list"
```

### After (GitHub Copilot Optimized)
```
"Create a Python function called `sort_list` that takes a list of integers as input and returns a sorted list in ascending order. Include type hints and handle edge cases like empty lists."
```

### Before (Original Prompt)
```
"build a todo app"
```

### After (Cursor Optimized)
```
"Create a full-stack todo application with React frontend and Node.js backend. Include user authentication, CRUD operations for todos, real-time updates, and MongoDB database. The app should have a modern UI with drag-and-drop functionality and support for todo categories and priorities."
```

## 🎨 Features

### Modern UI/UX
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Beautiful Interface**: Modern gradient design with smooth animations
- **Interactive Elements**: Hover effects, loading states, and transitions
- **Accessibility**: Proper contrast, keyboard navigation, and screen reader support

### Real-time Analysis
- **Instant Feedback**: See analysis results immediately
- **Live Validation**: Form validation with helpful error messages
- **Progress Indicators**: Loading spinners and status updates

### Copy & Export
- **One-Click Copy**: Copy optimized prompts to clipboard
- **Visual Feedback**: Success indicators for copy operations
- **Format Preservation**: Maintains formatting and structure

## 🔍 Tool Capabilities Database

The system includes a comprehensive database (`tool_analysis.json`) with:
- **Tool Descriptions**: Detailed explanations of each tool
- **Capabilities**: List of supported features
- **Optimization Strategies**: Tool-specific techniques
- **Best Practices**: Recommended approaches
- **Limitations**: Known constraints and considerations
- **Example Optimizations**: Before/after examples

## 🚀 Performance

- **Fast Response**: Optimizations complete in milliseconds
- **Scalable Architecture**: Easy to add new tools and strategies
- **Efficient Processing**: Minimal resource usage
- **Caching Ready**: Designed for future caching implementation

## 🔧 Customization

### Adding New Tools
1. Add tool information to `tool_analysis.json`
2. Create optimizer class in `tool_optimizers.py`
3. Update the main optimizer in `prompt_optimizer.py`
4. Add tool to the web interface dropdown

### Modifying Optimization Strategies
- Edit strategy definitions in `tool_analysis.json`
- Update optimization logic in `tool_optimizers.py`
- Adjust scoring algorithms in `prompt_optimizer.py`

## 🐛 Troubleshooting

### Common Issues

**Port Already in Use**
```bash
# Change port in app.py
app.run(debug=True, host='0.0.0.0', port=8082)
```

**Module Import Errors**
```bash
# Ensure you're in the correct directory
cd W3D3/Q3
python app.py
```

**Dependencies Issues**
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

## 📈 Future Enhancements

- **Machine Learning Integration**: Use ML for better prompt analysis
- **User Feedback System**: Learn from user preferences
- **Batch Processing**: Optimize multiple prompts at once
- **Export Options**: Save results in various formats
- **Collaboration Features**: Share and rate optimizations
- **More Tools**: Support for additional AI coding assistants

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is part of the Misogi course materials.

## 🙏 Acknowledgments

- Built for educational purposes
- Inspired by the need for better AI tool utilization
- Uses modern web technologies and best practices

---

**Happy Prompt Optimizing! 🚀** 