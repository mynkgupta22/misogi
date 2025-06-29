from flask import Flask, render_template, request, jsonify
import json
import os
from recommendation_engine import RecommendationEngine

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'

# Initialize recommendation engine
recommendation_engine = RecommendationEngine()

@app.route('/')
def index():
    """Main page with task input interface"""
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    """API endpoint to get agent recommendations"""
    try:
        data = request.get_json()
        task_description = data.get('task_description', '')
        
        if not task_description.strip():
            return jsonify({'error': 'Task description is required'}), 400
        
        # Get recommendations from the engine
        recommendations = recommendation_engine.get_recommendations(task_description)
        
        return jsonify({
            'success': True,
            'recommendations': recommendations,
            'task_analysis': recommendation_engine.analyze_task(task_description)
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/agents')
def agents():
    """Page to view all available agents"""
    agents_data = recommendation_engine.get_all_agents()
    return render_template('agents.html', agents=agents_data)

@app.route('/api/agents')
def api_agents():
    """API endpoint to get all agents"""
    agents_data = recommendation_engine.get_all_agents()
    return jsonify(agents_data)

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    
    print("🚀 Starting AI Coding Agent Recommendation System...")
    print("📱 Frontend will be available at: http://localhost:8080")
    print("🔧 API endpoints:")
    print("   - POST http://localhost:8080/recommend")
    print("   - GET  http://localhost:8080/api/agents")
    print("   - GET  http://localhost:8080/agents")
    print("⏹️  Press Ctrl+C to stop the server")
    print("-" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=8080) 