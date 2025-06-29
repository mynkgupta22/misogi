from flask import Flask, render_template, request, jsonify
import json
import os
from optimizers.prompt_optimizer import PromptOptimizer

app = Flask(__name__)
app.config['SECRET_KEY'] = 'adaptive-prompt-optimizer-secret-key'

# Initialize the prompt optimizer
optimizer = PromptOptimizer()

@app.route('/')
def index():
    """Main page with prompt input interface"""
    return render_template('index.html')

@app.route('/optimize', methods=['POST'])
def optimize():
    """API endpoint to optimize prompts"""
    try:
        data = request.get_json()
        base_prompt = data.get('base_prompt', '')
        target_tool = data.get('target_tool', '')
        
        if not base_prompt.strip():
            return jsonify({'error': 'Base prompt is required'}), 400
        
        if not target_tool:
            return jsonify({'error': 'Target tool selection is required'}), 400
        
        # Get optimization results
        optimization_result = optimizer.optimize_prompt(base_prompt, target_tool)
        
        return jsonify({
            'success': True,
            'optimization': optimization_result
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/tools')
def tools():
    """Page to view all available tools and their capabilities"""
    tools_data = optimizer.get_all_tools()
    return render_template('tools.html', tools=tools_data)

@app.route('/api/tools')
def api_tools():
    """API endpoint to get all tools"""
    tools_data = optimizer.get_all_tools()
    return jsonify(tools_data)

@app.route('/api/analyze', methods=['POST'])
def analyze():
    """API endpoint to analyze prompt without optimization"""
    try:
        data = request.get_json()
        base_prompt = data.get('base_prompt', '')
        
        if not base_prompt.strip():
            return jsonify({'error': 'Base prompt is required'}), 400
        
        # Analyze the prompt
        analysis = optimizer.analyze_prompt(base_prompt)
        
        return jsonify({
            'success': True,
            'analysis': analysis
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Create necessary directories
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    os.makedirs('optimizers', exist_ok=True)
    
    print("🚀 Starting Adaptive Prompt Optimizer...")
    print("📱 Frontend will be available at: http://localhost:8081")
    print("🔧 API endpoints:")
    print("   - POST http://localhost:8081/optimize")
    print("   - POST http://localhost:8081/api/analyze")
    print("   - GET  http://localhost:8081/api/tools")
    print("   - GET  http://localhost:8081/tools")
    print("⏹️  Press Ctrl+C to stop the server")
    print("-" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=8081) 