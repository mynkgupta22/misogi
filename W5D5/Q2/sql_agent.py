import sqlite3
import google.generativeai as genai
import os
import json
import time
from datetime import datetime
from typing import Dict, List, Any, Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class SQLAgent:
    def __init__(self, api_key: str = None, db_path: str = "commerce_data.db"):
        """Initialize SQL Agent with Gemini AI"""
        
        # Configure Gemini API
        if api_key:
            genai.configure(api_key=api_key)
        else:
            # Try to get from .env file or environment variable
            api_key = os.getenv('GEMINI_API_KEY')
            if not api_key:
                raise ValueError(
                    "Gemini API key is required. Please:\n"
                    "1. Create a .env file with: GEMINI_API_KEY=your_api_key_here\n"
                    "2. Or set GEMINI_API_KEY environment variable\n"
                    "3. Or pass api_key parameter to constructor"
                )
            genai.configure(api_key=api_key)
        
        # Initialize Gemini model
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Database connection
        self.db_path = db_path
        
        # Get database schema
        self.schema = self._get_database_schema()
        
        print("🤖 SQL Agent initialized with Gemini AI")
    
    def _get_database_schema(self) -> str:
        """Get complete database schema for context"""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get all table names
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        schema_info = []
        schema_info.append("=== COMMERCE DATABASE SCHEMA ===\n")
        
        for table in tables:
            table_name = table[0]
            
            # Get table schema
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            
            schema_info.append(f"Table: {table_name}")
            for col in columns:
                col_name, col_type, not_null, default_val, pk = col[1], col[2], col[3], col[4], col[5]
                pk_info = " (PRIMARY KEY)" if pk else ""
                null_info = " NOT NULL" if not_null else ""
                default_info = f" DEFAULT {default_val}" if default_val else ""
                schema_info.append(f"  - {col_name}: {col_type}{pk_info}{null_info}{default_info}")
            
            # Get sample data
            cursor.execute(f"SELECT * FROM {table_name} LIMIT 3")
            sample_rows = cursor.fetchall()
            if sample_rows:
                schema_info.append(f"  Sample data: {sample_rows[0] if sample_rows else 'No data'}")
            
            schema_info.append("")
        
        conn.close()
        return "\n".join(schema_info)
    
    def generate_sql_query(self, natural_language_query: str) -> Dict[str, Any]:
        """Generate SQL query from natural language using Gemini"""
        
        start_time = time.time()
        
        prompt = f"""
You are an expert SQL query generator for a quick commerce price comparison platform.

DATABASE SCHEMA:
{self.schema}

BUSINESS CONTEXT:
- This is a multi-platform grocery price comparison system
- Platforms: Blinkit, Zepto, Instamart, BigBasket Now, Dunzo
- Products include vegetables, fruits, dairy, snacks, beverages
- Prices vary by platform and may have discounts
- Availability varies by platform

USER QUERY: "{natural_language_query}"

INSTRUCTIONS:
1. Generate a SINGLE, optimized SQLite query to answer the user's question
2. Use proper JOINs to get related data (product names, platform names, categories)
3. Apply discounts by calculating: price * (1 - discount_percent/100) when discount exists
4. For "cheapest" queries, find the minimum price after applying discounts
5. Use CASE statements for complex calculations
6. Include LIMIT clauses for top results
7. Use proper WHERE clauses for filtering
8. Return only valid SQLite syntax

QUERY TYPES TO HANDLE:
- Cheapest product queries: Find lowest price across platforms
- Discount queries: Find products with specific discount percentages
- Platform comparison: Compare prices between specific platforms
- Budget queries: Find products within price range
- Category queries: Filter by product categories

RETURN ONLY THE SQL QUERY - NO EXPLANATIONS OR MARKDOWN:
"""

        try:
            response = self.model.generate_content(prompt)
            sql_query = response.text.strip()
            
            # Clean up the SQL query
            sql_query = self._clean_sql_query(sql_query)
            
            generation_time = (time.time() - start_time) * 1000
            
            return {
                "status": "success",
                "sql_query": sql_query,
                "generation_time_ms": round(generation_time, 2),
                "model_used": "gemini-1.5-flash"
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "generation_time_ms": (time.time() - start_time) * 1000
            }
    
    def _clean_sql_query(self, sql_query: str) -> str:
        """Clean and validate SQL query"""
        
        # Remove markdown code blocks if present
        if "```sql" in sql_query:
            sql_query = sql_query.split("```sql")[1].split("```")[0]
        elif "```" in sql_query:
            sql_query = sql_query.split("```")[1].split("```")[0]
        
        # Remove extra whitespace and comments
        lines = sql_query.split('\n')
        cleaned_lines = []
        for line in lines:
            line = line.strip()
            if line and not line.startswith('--'):
                cleaned_lines.append(line)
        
        sql_query = ' '.join(cleaned_lines)
        
        # Basic validation
        if not sql_query.upper().startswith('SELECT'):
            raise ValueError("Generated query must be a SELECT statement")
        
        return sql_query
    
    def execute_query(self, sql_query: str) -> Dict[str, Any]:
        """Execute SQL query against the database"""
        
        start_time = time.time()
        
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row  # Enable column access by name
            cursor = conn.cursor()
            
            # Execute the query
            cursor.execute(sql_query)
            
            # Fetch results
            rows = cursor.fetchall()
            
            # Convert to list of dictionaries
            results = []
            for row in rows:
                results.append(dict(row))
            
            conn.close()
            
            execution_time = (time.time() - start_time) * 1000
            
            return {
                "status": "success",
                "results": results,
                "row_count": len(results),
                "execution_time_ms": round(execution_time, 2),
                "sql_executed": sql_query
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "execution_time_ms": (time.time() - start_time) * 1000,
                "sql_attempted": sql_query
            }
    
    def process_natural_language_query(self, user_query: str) -> Dict[str, Any]:
        """Complete pipeline: Generate SQL from natural language and execute"""
        
        start_time = time.time()
        
        # Log the query
        self._log_search_query(user_query)
        
        # Generate SQL
        sql_result = self.generate_sql_query(user_query)
        if sql_result["status"] != "success":
            return {
                "status": "error",
                "message": f"Failed to generate SQL: {sql_result['error']}",
                "query": user_query
            }
        
        sql_query = sql_result["sql_query"]
        
        # Execute SQL
        exec_result = self.execute_query(sql_query)
        if exec_result["status"] != "success":
            return {
                "status": "error",
                "message": f"Failed to execute SQL: {exec_result['error']}",
                "query": user_query,
                "generated_sql": sql_query
            }
        
        # Format results based on query type
        formatted_results = self._format_results(user_query, exec_result["results"])
        
        total_time = (time.time() - start_time) * 1000
        
        return {
            "status": "success",
            "query": user_query,
            "generated_sql": sql_query,
            "raw_results": exec_result["results"],
            "formatted_results": formatted_results,
            "performance": {
                "total_time_ms": round(total_time, 2),
                "sql_generation_ms": sql_result["generation_time_ms"],
                "sql_execution_ms": exec_result["execution_time_ms"],
                "rows_returned": exec_result["row_count"]
            }
        }
    
    def _format_results(self, query: str, raw_results: List[Dict]) -> Dict[str, Any]:
        """Format results based on query type for better presentation"""
        
        if not raw_results:
            return {
                "message": "No results found for your query.",
                "type": "empty_result"
            }
        
        query_lower = query.lower()
        
        # Detect query type and format accordingly
        if "cheapest" in query_lower or "best price" in query_lower:
            return self._format_cheapest_result(raw_results[0])
        
        elif "discount" in query_lower and "%" in query:
            return self._format_discount_results(raw_results)
        
        elif "compare" in query_lower:
            return self._format_comparison_results(raw_results)
        
        elif "budget" in query_lower or "₹" in query:
            return self._format_budget_results(raw_results)
        
        else:
            # Generic formatting
            return {
                "message": f"Found {len(raw_results)} results",
                "type": "general_results",
                "results": raw_results[:10]  # Limit to 10 results
            }
    
    def _format_cheapest_result(self, result: Dict) -> Dict[str, Any]:
        """Format cheapest product result"""
        
        # Calculate savings if discount info is available
        original_price = result.get('price', result.get('original_price', 0))
        final_price = result.get('final_price', result.get('discounted_price', original_price))
        discount_percent = result.get('discount_percent', 0)
        savings = original_price - final_price
        
        return {
            "type": "cheapest_product",
            "product_name": result.get('name', result.get('product_name', 'Unknown')),
            "platform": result.get('platform_name', result.get('platform', 'Unknown')),
            "original_price": f"₹{original_price:.2f}",
            "discounted_price": f"₹{final_price:.2f}",
            "discount_percent": f"{discount_percent:.0f}%",
            "savings": f"₹{savings:.2f}",
            "delivery_time": result.get('delivery_time', result.get('estimated_delivery', 'Unknown')),
            "message": f"The cheapest {result.get('name', 'product')} is available on {result.get('platform_name', 'platform')} for ₹{final_price:.2f}"
        }
    
    def _format_discount_results(self, results: List[Dict]) -> Dict[str, Any]:
        """Format discount products results"""
        
        formatted_products = []
        for result in results:
            original_price = result.get('price', result.get('original_price', 0))
            discount_percent = result.get('discount_percent', 0)
            final_price = original_price * (1 - discount_percent / 100)
            savings = original_price - final_price
            
            formatted_products.append({
                "product_name": result.get('name', result.get('product_name', 'Unknown')),
                "category": result.get('category_name', result.get('category', 'Unknown')),
                "original_price": f"₹{original_price:.2f}",
                "discounted_price": f"₹{final_price:.2f}",
                "discount_percent": f"{discount_percent:.0f}%",
                "savings": f"₹{savings:.2f}"
            })
        
        platform_name = results[0].get('platform_name', 'Platform') if results else 'Platform'
        min_discount = min([r.get('discount_percent', 0) for r in results]) if results else 0
        
        return {
            "type": "discount_products",
            "platform": platform_name,
            "min_discount": f"{min_discount:.0f}%",
            "total_products": len(formatted_products),
            "products": formatted_products,
            "message": f"Found {len(formatted_products)} products with discounts on {platform_name}"
        }
    
    def _format_comparison_results(self, results: List[Dict]) -> Dict[str, Any]:
        """Format price comparison results"""
        
        comparison_data = []
        for result in results:
            comparison_data.append({
                "product_name": result.get('name', result.get('product_name', 'Unknown')),
                "platform1": {
                    "name": result.get('platform1_name', 'Platform 1'),
                    "price": f"₹{result.get('platform1_price', 0):.2f}",
                    "discount": f"{result.get('platform1_discount', 0):.0f}%" if result.get('platform1_discount', 0) > 0 else "No discount"
                },
                "platform2": {
                    "name": result.get('platform2_name', 'Platform 2'),
                    "price": f"₹{result.get('platform2_price', 0):.2f}",
                    "discount": f"{result.get('platform2_discount', 0):.0f}%" if result.get('platform2_discount', 0) > 0 else "No discount"
                },
                "cheaper_platform": result.get('cheaper_platform', 'Unknown'),
                "price_difference": f"₹{result.get('price_difference', 0):.2f}"
            })
        
        platform1 = results[0].get('platform1_name', 'Platform 1') if results else 'Platform 1'
        platform2 = results[0].get('platform2_name', 'Platform 2') if results else 'Platform 2'
        
        return {
            "type": "compare_prices",
            "platform1": platform1,
            "platform2": platform2,
            "total_products_compared": len(comparison_data),
            "comparison": comparison_data,
            "message": f"Compared {len(comparison_data)} products between {platform1} and {platform2}"
        }
    
    def _format_budget_results(self, results: List[Dict]) -> Dict[str, Any]:
        """Format budget-based results"""
        
        deals = []
        total_cost = 0
        total_savings = 0
        
        for result in results:
            original_price = result.get('price', result.get('original_price', 0))
            final_price = result.get('final_price', result.get('discounted_price', original_price))
            discount_percent = result.get('discount_percent', 0)
            savings = original_price - final_price
            
            deals.append({
                "product_name": result.get('name', result.get('product_name', 'Unknown')),
                "platform": result.get('platform_name', result.get('platform', 'Unknown')),
                "original_price": f"₹{original_price:.2f}",
                "discounted_price": f"₹{final_price:.2f}",
                "discount_percent": f"{discount_percent:.0f}%",
                "savings": f"₹{savings:.2f}",
                "value_score": f"{(savings/final_price*100) if final_price > 0 else 0:.1f}%"
            })
            
            total_cost += final_price
            total_savings += savings
        
        return {
            "type": "budget_deals",
            "total_cost": f"₹{total_cost:.2f}",
            "total_savings": f"₹{total_savings:.2f}",
            "total_items": len(deals),
            "deals": deals,
            "message": f"Found {len(deals)} deals with total savings of ₹{total_savings:.2f}"
        }
    
    def _log_search_query(self, query: str) -> None:
        """Log search query for analytics"""
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO search_queries (query_text, user_session, created_at) 
                VALUES (?, ?, ?)
            ''', (query, "web_session", datetime.now()))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"Warning: Could not log search query: {e}")
    
    def get_database_stats(self) -> Dict[str, Any]:
        """Get database statistics"""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        stats = {}
        
        # Table counts
        tables = ['platforms', 'categories', 'products', 'current_prices', 'discounts', 'availability']
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            stats[table] = cursor.fetchone()[0]
        
        # Recent queries
        cursor.execute("SELECT COUNT(*) FROM search_queries WHERE created_at > datetime('now', '-1 day')")
        stats['queries_today'] = cursor.fetchone()[0]
        
        conn.close()
        return stats

# Example usage and testing
if __name__ == "__main__":
    # Test the SQL agent
    try:
        agent = SQLAgent()
        
        test_queries = [
            "Which app has cheapest onions right now?",
            "Show products with 30% discount on Blinkit",
            "Compare fruit prices between Zepto and Instamart",
            "Find best deals for ₹500 budget"
        ]
        
        for query in test_queries:
            print(f"\n🔍 Testing: {query}")
            result = agent.process_natural_language_query(query)
            print(f"Status: {result['status']}")
            if result['status'] == 'success':
                print(f"Generated SQL: {result['generated_sql']}")
                print(f"Results: {len(result['raw_results'])} rows")
            else:
                print(f"Error: {result['message']}")
    
    except Exception as e:
        print(f"Error testing SQL agent: {e}")
        print("Make sure to:")
        print("1. Create .env file with: GEMINI_API_KEY=your_api_key_here")
        print("2. Get API key from: https://makersuite.google.com/app/apikey")
        print("3. Run database_setup.py first") 