from flask import Flask, render_template, request, jsonify
from query_agent import CommerceQueryAgent
import time
from datetime import datetime
import json

app = Flask(__name__)

# Initialize the query agent
query_agent = CommerceQueryAgent()

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
        
        # Process the query
        result = query_agent.process_query(query)
        
        # Add timestamp
        result['timestamp'] = datetime.now().isoformat()
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Internal server error: {str(e)}'
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
    try:
        platforms_info = []
        for platform in query_agent.data.platforms:
            platforms_info.append({
                'name': platform['name'],
                'commission': f"{platform['commission']}%",
                'delivery_time': platform['delivery_time']
            })
        
        return jsonify({
            'status': 'success',
            'platforms': platforms_info
        })
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error getting platforms: {str(e)}'
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'total_products': len(query_agent.data.products),
        'total_platforms': len(query_agent.data.platforms),
        'total_categories': len(query_agent.data.categories)
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001) 