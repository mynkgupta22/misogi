# 🚀 Quick Commerce SQL Agent Setup

## 📋 Prerequisites

1. **Python 3.7+** installed
2. **Google Gemini API Key** (required for AI-powered SQL generation)

## 🔑 Get Gemini API Key

1. Visit: https://makersuite.google.com/app/apikey
2. Create a new API key
3. Copy the API key for use below

## ⚡ Quick Setup (Recommended)

```bash
# 1. Copy example environment file and edit with your API key
cp env.example .env
# Then edit .env file with your actual Gemini API key

# 2. Run automated setup
python3 setup.py
```

## 📖 Manual Setup (If needed)

```bash
# 1. Copy and edit .env file with your API key
cp env.example .env
# Edit .env file and replace 'your_gemini_api_key_here' with actual key

# 2. Install dependencies
pip3 install -r requirements.txt

# 3. Setup database
python3 database_setup.py

# 4. Test SQL agent
python3 query_agent.py

# 5. Start web application
python3 app.py
```

## 🌐 Access Application

Open your browser to: **http://localhost:5000**

## 🧪 Test Queries

Try these natural language queries:

1. **"Which app has cheapest onions right now?"**
2. **"Show products with 30%+ discount on Blinkit"**
3. **"Compare fruit prices between Zepto and Instamart"**
4. **"Find best deals for ₹1000 grocery list"**

## 🔍 What You'll See

For each query, the system will:
- 🤖 **Generate SQL** using Gemini AI
- ⚡ **Execute queries** against SQLite database
- 📊 **Show performance** metrics (generation time, execution time)
- 📈 **Display results** with proper formatting

## 🛠️ Architecture Overview

```
User Query → Gemini AI → SQL Generation → SQLite Database → Formatted Results
```

## 📊 Database Schema

- **platforms**: 5 commerce apps (Blinkit, Zepto, etc.)
- **products**: 20 products across 7 categories  
- **current_prices**: Real-time pricing data
- **discounts**: Active discount information
- **availability**: Stock and delivery data
- **price_history**: Historical pricing trends
- **search_queries**: Query analytics
- **popular_products**: Usage statistics

## 🚨 Troubleshooting

### API Key Issues
```bash
# Check if .env file exists and contains API key
cat .env

# Create .env file with your API key
echo "GEMINI_API_KEY=your_actual_api_key_here" > .env

# Verify .env file content
cat .env
```

### Database Issues
```bash
# Recreate database if needed
rm commerce_data.db
python3 database_setup.py
```

### Testing Issues
```bash
# Test individual components
python3 sql_agent.py     # Test SQL agent
python3 query_agent.py   # Test query processing
python3 app.py           # Start web server
```

## 🎯 Success Indicators

✅ Database created with 3,000+ records  
✅ Gemini AI generates valid SQL queries  
✅ Natural language queries return accurate results  
✅ Web interface shows SQL generation process  
✅ Performance metrics displayed  

## 🔧 Advanced Configuration

### Custom Database Path
```python
# In your code, modify:
sql_agent = SQLAgent(db_path="custom_path.db")
```

### Rate Limiting
```python
# Modify in app.py:
RATE_LIMIT = 30  # requests per minute
```

## 📈 Next Steps

1. **Add more products** to database
2. **Implement real-time price updates**
3. **Add machine learning recommendations**
4. **Deploy to cloud platform**

---

🎉 **Your SQL Agent is ready! Experience AI-powered database querying with natural language.** 