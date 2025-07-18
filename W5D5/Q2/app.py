from flask import Flask, render_template, request, jsonify
from query_agent import CommerceQueryAgent
import time
from datetime import datetime
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Initialize the query agent
try:
    query_agent = CommerceQueryAgent()
    print("✅ Query agent initialized successfully")
except Exception as e:
    print(f"❌ Failed to initialize query agent: {e}")
    print("Please ensure:")
    print("1. Create .env file with: GEMINI_API_KEY=your_api_key_here")
    print("2. Get API key from: https://makersuite.google.com/app/apikey")
    print("3. Database exists (run: python database_setup.py)")
    query_agent = None

# Simple rate limiting (in-memory store)
request_times = {}
RATE_LIMIT = 30  # requests per minute
RATE_WINDOW = 60  # seconds

def check_rate_limit(client_ip):
    """Simple rate limiting implementation."""
    current_time = time.time()
    
    if client_ip not in request_times:
        request_times[client_ip] = []
    
    # Clean old requests
    request_times[client_ip] = [
        req_time for req_time in request_times[client_ip] 
        if current_time - req_time < RATE_WINDOW
    ]
    
    # Check if limit exceeded
    if len(request_times[client_ip]) >= RATE_LIMIT:
        return False
    
    # Add current request
    request_times[client_ip].append(current_time)
    return True

@app.route('/')
def index():
    """Main page with query interface."""
    return render_template('index.html')

@app.route('/api/query', methods=['POST'])
def api_query():
    """API endpoint to process natural language queries."""
    client_ip = request.remote_addr
    
    # Check if query agent is available
    if query_agent is None:
        return jsonify({
            'status': 'error',
            'message': 'SQL Agent not initialized. Please check server configuration.',
            'details': 'Ensure GEMINI_API_KEY is set and database exists.'
        }), 503
    
    # Check rate limiting
    if not check_rate_limit(client_ip):
        return jsonify({
            'status': 'error',
            'message': 'Rate limit exceeded. Please wait before making more requests.'
        }), 429
    
    try:
        data = request.get_json()
        if not data or 'query' not in data:
            return jsonify({
                'status': 'error',
                'message': 'Query parameter is required'
            }), 400
        
        query = data['query'].strip()
        if not query:
            return jsonify({
                'status': 'error',
                'message': 'Query cannot be empty'
            }), 400
        
        # Process the query using SQL agent
        result = query_agent.process_query(query)
        
        # Add timestamp and additional metadata
        result['timestamp'] = datetime.now().isoformat()
        result['server_info'] = {
            'sql_backend': 'SQLite with Gemini AI',
            'query_processed_at': datetime.now().isoformat(),
            'api_version': '2.0'
        }
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Internal server error: {str(e)}',
            'error_type': 'SQL_PROCESSING_ERROR'
        }), 500

@app.route('/api/suggestions', methods=['GET'])
def api_suggestions():
    """API endpoint to get query suggestions."""
    try:
        suggestions = {
            'sample_queries': [
                "Which app has cheapest onions right now?",
                "Show products with 30%+ discount on Blinkit",
                "Compare fruit prices between Zepto and Instamart",
                "Find best deals for ₹1000 grocery list",
                "Cheapest milk",
                "Best price for tomatoes",
                "Blinkit products with 40% discount",
                "What can I buy with ₹500"
            ],
            'products': query_agent.get_available_products(),
            'platforms': query_agent.get_available_platforms(),
            'categories': query_agent.get_categories()
        }
        return jsonify(suggestions)
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error getting suggestions: {str(e)}'
        }), 500

@app.route('/api/platforms', methods=['GET'])
def api_platforms():
    """API endpoint to get platform information."""
    
    if query_agent is None:
        return jsonify({
            'status': 'error',
            'message': 'SQL Agent not initialized'
        }), 503
        
    try:
        platforms_info = []
        for platform in query_agent.platforms:
            platforms_info.append({
                'name': platform['name'],
                'commission': f"{platform['commission']}%",
                'delivery_time': platform['delivery_time']
            })
        
        return jsonify({
            'status': 'success',
            'platforms': platforms_info,
            'data_source': 'SQLite Database'
        })
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error getting platforms: {str(e)}'
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    
    health_status = {
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '2.0',
        'backend': 'SQLite + Gemini AI'
    }
    
    if query_agent is None:
        health_status.update({
            'status': 'unhealthy',
            'error': 'SQL Agent not initialized',
            'database_connected': False,
            'gemini_api_available': False
        })
        return jsonify(health_status), 503
    
    try:
        # Get database statistics
        db_stats = query_agent.get_database_stats()
        health_status.update({
            'database_connected': True,
            'database_stats': db_stats,
            'gemini_api_available': True,
            'total_products': db_stats.get('products', 0),
            'total_platforms': db_stats.get('platforms', 0),
            'total_categories': db_stats.get('categories', 0),
            'queries_today': db_stats.get('queries_today', 0)
        })
        
    except Exception as e:
        health_status.update({
            'status': 'degraded',
            'database_connected': False,
            'error': str(e)
        })
        return jsonify(health_status), 503
    
    return jsonify(health_status)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001) 