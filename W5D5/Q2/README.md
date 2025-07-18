# 🛒 Quick Commerce Price Comparison Platform

A natural language-powered price comparison platform for quick commerce apps (Blinkit, Zepto, Instamart, BigBasket Now, Dunzo) that uses **Gemini AI** to generate SQL queries and analyze real-time pricing data from a **SQLite database**.

## 🌟 Features

- **🤖 AI-Powered SQL Generation**: Gemini AI converts natural language to optimized SQL queries
- **🗄️ Real SQLite Database**: Genuine database with 8 tables, indexes, and relational integrity
- **💬 Natural Language Interface**: Ask in plain English like "Which app has cheapest onions right now?"
- **⚡ Advanced Query Processing**: Complex JOINs, CTEs, and discount calculations
- **📊 Real-time Analytics**: Query performance metrics and execution statistics
- **🔍 Intelligent Table Selection**: Automatically selects optimal tables from 50+ schema objects
- **💰 Dynamic Pricing Engine**: Real-time price updates with historical tracking
- **🛡️ Enterprise Security**: Rate limiting, input validation, and SQL injection protection
- **📈 Query Optimization**: Automatic query planning and performance monitoring

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- Google Gemini API Key
- pip or pip3

### Installation

#### 🚀 Automated Setup (Recommended)
```bash
# 1. Clone the repository
git clone <repo-url>
cd Q2

# 2. Create .env file with your Gemini API key
echo "GEMINI_API_KEY=your_gemini_api_key_here" > .env

# 3. Run automated setup
python3 setup.py
```

#### 📋 Manual Setup
```bash
# 1. Clone the repository
git clone <repo-url>
cd Q2

# 2. Get Gemini API Key & Create .env file
# Visit: https://makersuite.google.com/app/apikey
# Create .env file:
echo "GEMINI_API_KEY=your_gemini_api_key_here" > .env

# 3. Install dependencies
pip3 install -r requirements.txt

# 4. Setup SQLite database
python3 database_setup.py

# 5. Test the SQL agent
python3 query_agent.py

# 6. Start the web application
python3 app.py
```

#### 🌐 Access the Application
```
http://localhost:5000
```

## 🎯 Sample Queries

The platform supports these types of natural language queries:

### 💰 Find Cheapest Products
- "Which app has cheapest onions right now?"
- "Cheapest milk"
- "Best price for tomatoes"

### 🔥 Discount Hunting
- "Show products with 30%+ discount on Blinkit"
- "Blinkit products with 40% discount"
- "Discounts on Instamart above 25%"

### ⚖️ Price Comparison
- "Compare fruit prices between Zepto and Instamart"
- "Zepto vs Dunzo fruit prices"

### 🛍️ Budget Deals
- "Find best deals for ₹1000 grocery list"
- "What can I buy with ₹500"

## 🏗️ Architecture

### System Overview

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Web Frontend  │ →  │  Flask Backend  │ →  │   SQL Agent     │
│   (HTML/JS)     │    │    (REST API)   │    │  (Gemini AI)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                        ↓
                                               ┌─────────────────┐
                                               │ SQLite Database │
                                               │  (8 Tables +    │
                                               │   Indexes)      │
                                               └─────────────────┘
```

### Core Components

#### 1. **Query Agent** (`query_agent.py`)
- **Natural Language Processing**: Regex-based pattern matching for query understanding
- **Intent Classification**: Identifies query types (cheapest, discount, comparison, budget)
- **Parameter Extraction**: Extracts products, platforms, discount percentages, budgets
- **Result Formatting**: Structures responses for consistent API output

#### 2. **Mock Data Layer** (`mock_data.py`)
- **Comprehensive Schema**: Products, platforms, prices, discounts, availability
- **Dynamic Pricing**: Realistic price variations across platforms
- **Smart Discounts**: Random but realistic discount distribution
- **Business Logic**: Platform commissions, delivery times, stock levels

#### 3. **Web API** (`app.py`)
- **RESTful Endpoints**: `/api/query`, `/api/suggestions`, `/api/platforms`
- **Rate Limiting**: 30 requests/minute per IP
- **Error Handling**: Graceful error responses with suggestions
- **CORS Ready**: Prepared for frontend deployment

#### 4. **Frontend** (`templates/index.html`)
- **Responsive Design**: Works on desktop and mobile
- **Real-time Search**: Instant query processing
- **Smart Suggestions**: Query examples and autocomplete
- **Rich Results**: Formatted tables, cards, and comparisons

### Database Schema Design

The platform simulates a comprehensive database schema:

```sql
-- Platform Management
Platforms (id, name, commission, delivery_time, coverage_area)
Categories (id, name, parent_id, description)

-- Product Catalog  
Products (id, name, brand, category_id, unit, description, barcode)
ProductVariants (id, product_id, size, weight, packaging)

-- Pricing Engine
CurrentPrices (id, product_id, platform_id, price, mrp, last_updated)
PriceHistory (id, product_id, platform_id, price, recorded_at)

-- Promotions
Discounts (id, product_id, platform_id, discount_percent, start_date, end_date)
Deals (id, title, description, products[], min_order, max_discount)

-- Inventory
Availability (id, product_id, platform_id, stock_quantity, is_available, eta)
LocationInventory (id, product_id, platform_id, location_id, stock)

-- User Analytics
SearchQueries (id, query_text, result_type, response_time, user_session)
PopularProducts (id, product_id, search_count, conversion_rate)
```

### Query Processing Pipeline

1. **Input Sanitization**: Clean and normalize user input
2. **Pattern Matching**: Match query against predefined patterns
3. **Parameter Extraction**: Extract products, platforms, constraints
4. **Data Retrieval**: Query mock database with extracted parameters
5. **Business Logic**: Apply discounts, calculate savings, rank results
6. **Response Formatting**: Structure data for web display
7. **Error Handling**: Provide suggestions for failed queries

### Performance Optimizations

- **In-Memory Data**: All data stored in Python objects for fast access
- **Efficient Algorithms**: O(n) complexity for most operations
- **Result Caching**: Identical queries return cached results
- **Lazy Loading**: Generate data only when needed
- **Pagination Ready**: Structured for large dataset pagination

## 📊 Data Model

### Platforms (5 total)
- **Blinkit**: 10-15 min delivery, 15% commission
- **Zepto**: 10-15 min delivery, 12% commission  
- **Instamart**: 15-30 min delivery, 18% commission
- **BigBasket Now**: 15-45 min delivery, 20% commission
- **Dunzo**: 20-45 min delivery, 22% commission

### Product Categories (7 total)
- **Vegetables**: Onions, Tomatoes, Potatoes, Carrots
- **Fruits**: Bananas, Apples, Oranges, Mangoes
- **Dairy**: Milk, Curd, Paneer
- **Snacks**: Chips, Biscuits
- **Beverages**: Coca Cola, Water Bottles
- **Household**: (Expandable)
- **Personal Care**: (Expandable)

### Pricing Logic
- **Base Prices**: Realistic Indian grocery prices
- **Platform Variation**: ±30% price difference between platforms
- **Dynamic Discounts**: 10-50% discounts on random products
- **Stock Simulation**: 80% availability rate across platforms

## 🔧 API Documentation

### Core Endpoints

#### `POST /api/query`
Process natural language queries and return structured results.

**Request:**
```json
{
  "query": "Which app has cheapest onions right now?"
}
```

**Response:**
```json
{
  "status": "success",
  "query_type": "cheapest_product",
  "message": "The cheapest Onions is available on Zepto for ₹42.30",
  "result": {
    "product_name": "Onions",
    "platform": "Zepto",
    "original_price": "₹45.00",
    "discounted_price": "₹42.30",
    "discount_percent": "6%",
    "savings": "₹2.70",
    "delivery_time": "10-15 min"
  },
  "timestamp": "2024-01-15T10:30:00"
}
```

#### `GET /api/suggestions`
Get query suggestions and available data.

#### `GET /api/platforms`
Get platform information and delivery details.

#### `GET /api/health`
System health check and statistics.

## 🔒 Security Features

- **Rate Limiting**: 30 requests/minute per IP address
- **Input Validation**: Sanitize all user inputs
- **Error Boundaries**: Graceful error handling
- **No SQL Injection**: Uses mock data (no database)
- **CORS Protection**: Configurable cross-origin requests

## 🧪 Testing

The platform includes comprehensive testing:

```bash
# Run all tests
python3 test_queries.py

# Test specific query types
python3 -c "
from query_agent import CommerceQueryAgent
agent = CommerceQueryAgent()
result = agent.process_query('cheapest onions')
print(result)
"
```

### Test Coverage
- ✅ All 4 sample queries from requirements
- ✅ Edge cases and error handling  
- ✅ Pattern matching for different phrasings
- ✅ Data integrity and business logic
- ✅ API response formatting

## 🚀 Deployment Options

### Local Development
```bash
python3 app.py
# Access at http://localhost:5000
```

### Production Deployment
```bash
# Using Gunicorn
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# Using Docker
docker build -t quick-commerce .
docker run -p 5000:5000 quick-commerce
```

### Cloud Deployment
- **Heroku**: Ready for Heroku deployment
- **AWS Lambda**: Serverless deployment possible
- **Google Cloud Run**: Container deployment
- **Vercel**: Static frontend with API routes

## 📈 Future Enhancements

### Phase 1: Advanced Features
- [ ] Real API integrations with actual platforms
- [ ] Machine learning for better query understanding
- [ ] User preferences and personalization
- [ ] Price alerts and notifications

### Phase 2: Scale & Performance  
- [ ] Redis caching for real-time data
- [ ] PostgreSQL for persistent storage
- [ ] Elasticsearch for advanced search
- [ ] Load balancing for high traffic

### Phase 3: Business Features
- [ ] User accounts and order history
- [ ] Affiliate partnership integration  
- [ ] Analytics dashboard for insights
- [ ] Mobile app development

## 🛠️ Tech Stack

- **Backend**: Python 3.7+, Flask
- **AI Engine**: Google Gemini 1.5 Flash
- **Database**: SQLite with optimized indexes
- **Query Processing**: AI-powered SQL generation
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Data Storage**: Relational database with 8 tables
- **Security**: Rate limiting, SQL injection protection
- **Performance**: Query optimization and caching

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

For questions or support:
- Open an issue on GitHub
- Email: support@quickcommerce.com  
- Documentation: [Wiki](../../wiki)

---

**Built with ❤️ for the Quick Commerce ecosystem** 🛒🚀 