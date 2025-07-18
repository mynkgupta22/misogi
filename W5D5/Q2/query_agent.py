import os
from typing import Dict, List, Any
from sql_agent import SQLAgent
import sqlite3
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class CommerceQueryAgent:
    def __init__(self):
        """Initialize the commerce query agent with SQL backend"""
        
        # Check if database exists
        if not os.path.exists('commerce_data.db'):
            print("❌ Database not found! Please run: python database_setup.py")
            raise FileNotFoundError("Database file 'commerce_data.db' not found. Run database_setup.py first.")
        
        # Initialize SQL agent
        try:
            self.sql_agent = SQLAgent()
            print("✅ Commerce Query Agent initialized with SQL backend")
        except Exception as e:
            print(f"❌ Failed to initialize SQL Agent: {e}")
            print("Make sure to:")
            print("1. Create a .env file with: GEMINI_API_KEY=your_api_key_here")
            print("2. Get API key from: https://makersuite.google.com/app/apikey")
            raise
        
        # Get platform and product data for legacy API compatibility
        self._load_metadata()
    
    def _load_metadata(self):
        """Load platform and product metadata for API compatibility"""
        
        try:
            conn = sqlite3.connect('commerce_data.db')
            cursor = conn.cursor()
            
            # Load platforms
            cursor.execute("SELECT id, name, commission, delivery_time FROM platforms")
            self.platforms = []
            for row in cursor.fetchall():
                self.platforms.append({
                    "id": row[0],
                    "name": row[1], 
                    "commission": row[2],
                    "delivery_time": row[3]
                })
            
            # Load categories
            cursor.execute("SELECT id, name, description FROM categories")
            self.categories = []
            for row in cursor.fetchall():
                self.categories.append({
                    "id": row[0],
                    "name": row[1],
                    "description": row[2] or ""
                })
            
            # Load products
            cursor.execute("SELECT id, name, category_id, brand, unit, description FROM products")
            self.products = []
            for row in cursor.fetchall():
                self.products.append({
                    "id": row[0],
                    "name": row[1],
                    "category_id": row[2],
                    "brand": row[3] or "",
                    "unit": row[4] or "",
                    "description": row[5] or ""
                })
            
            conn.close()
            
        except Exception as e:
            print(f"Warning: Could not load metadata: {e}")
            self.platforms = []
            self.categories = []
            self.products = []
    
    def process_query(self, query: str) -> Dict[str, Any]:
        """Process natural language query using SQL Agent"""
        
        try:
            # Use SQL agent to process the query
            result = self.sql_agent.process_natural_language_query(query)
            
            if result["status"] == "success":
                # Convert SQL agent result to expected format
                formatted_result = self._convert_sql_result_to_api_format(result)
                return formatted_result
            else:
                return {
                    "status": "error",
                    "message": result.get("message", "Failed to process query"),
                    "suggestions": [
                        "Which app has cheapest onions right now?",
                        "Show products with 30%+ discount on Blinkit",
                        "Compare fruit prices between Zepto and Instamart",
                        "Find best deals for ₹1000 grocery list"
                    ]
                }
        
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error processing query: {str(e)}",
                "suggestions": [
                    "Which app has cheapest onions right now?",
                    "Show products with 30%+ discount on Blinkit", 
                    "Compare fruit prices between Zepto and Instamart",
                    "Find best deals for ₹1000 grocery list"
                ]
            }
    
    def _convert_sql_result_to_api_format(self, sql_result: Dict[str, Any]) -> Dict[str, Any]:
        """Convert SQL agent result to the expected API format"""
        
        formatted_results = sql_result["formatted_results"]
        query_type = formatted_results.get("type", "general_results")
        
        # Base response structure
        response = {
            "status": "success",
            "query": sql_result["query"],
            "generated_sql": sql_result["generated_sql"],
            "performance": sql_result["performance"],
            "timestamp": sql_result.get("timestamp", ""),
            "query_type": query_type,
            "message": formatted_results.get("message", "Query executed successfully")
        }
        
        # Add query-specific result formatting
        if query_type == "cheapest_product":
            response["result"] = {
                "product_name": formatted_results["product_name"],
                "platform": formatted_results["platform"],
                "original_price": formatted_results["original_price"],
                "discounted_price": formatted_results["discounted_price"],
                "discount_percent": formatted_results["discount_percent"],
                "savings": formatted_results["savings"],
                "delivery_time": formatted_results["delivery_time"]
            }
        
        elif query_type == "discount_products":
            response["result"] = {
                "platform": formatted_results["platform"],
                "min_discount": formatted_results["min_discount"],
                "total_products": formatted_results["total_products"],
                "products": formatted_results["products"]
            }
        
        elif query_type == "compare_prices":
            response["result"] = {
                "category": "Products",  # Default since SQL results might not have category
                "platform1": formatted_results["platform1"],
                "platform2": formatted_results["platform2"],
                "total_products_compared": formatted_results["total_products_compared"],
                "comparison": formatted_results["comparison"]
            }
        
        elif query_type == "budget_deals":
            response["result"] = {
                "budget": "₹" + str(self._extract_budget_from_query(sql_result["query"])),
                "total_cost": formatted_results["total_cost"],
                "total_savings": formatted_results["total_savings"],
                "remaining_budget": "₹0.00",  # Calculate if needed
                "total_items": formatted_results["total_items"],
                "deals": formatted_results["deals"]
            }
        
        else:
            # Generic results
            response["result"] = {
                "results": formatted_results.get("results", sql_result["raw_results"][:10])
            }
        
        return response
    
    def _extract_budget_from_query(self, query: str) -> float:
        """Extract budget amount from query string"""
        import re
        
        # Look for ₹ followed by numbers
        match = re.search(r'₹(\d+)', query)
        if match:
            return float(match.group(1))
        
        # Look for numbers followed by budget-related words
        match = re.search(r'(\d+)\s*(?:rupees?|rs\.?|budget|money)', query.lower())
        if match:
            return float(match.group(1))
        
        return 1000.0  # Default budget
    
    def get_available_products(self) -> List[str]:
        """Return list of available products"""
        return [product["name"] for product in self.products]
    
    def get_available_platforms(self) -> List[str]:
        """Return list of available platforms"""
        return [platform["name"] for platform in self.platforms]
    
    def get_categories(self) -> List[str]:
        """Return list of available categories"""
        return [category["name"] for category in self.categories]
    
    def get_database_stats(self) -> Dict[str, Any]:
        """Get database statistics"""
        return self.sql_agent.get_database_stats()

# For backward compatibility, keep the mock functions but with database backend
def get_cheapest_product(product_name: str) -> Dict[str, Any]:
    """Legacy function for getting cheapest product"""
    agent = CommerceQueryAgent()
    result = agent.process_query(f"cheapest {product_name}")
    return result

def get_products_with_discount(platform_name: str, min_discount_percent: int) -> List[Dict[str, Any]]:
    """Legacy function for getting discounted products"""
    agent = CommerceQueryAgent()
    result = agent.process_query(f"show products with {min_discount_percent}% discount on {platform_name}")
    if result["status"] == "success" and "products" in result.get("result", {}):
        return result["result"]["products"]
    return []

def compare_prices(category: str, platform1_name: str, platform2_name: str) -> List[Dict[str, Any]]:
    """Legacy function for price comparison"""
    agent = CommerceQueryAgent()
    result = agent.process_query(f"compare {category} prices between {platform1_name} and {platform2_name}")
    if result["status"] == "success" and "comparison" in result.get("result", {}):
        return result["result"]["comparison"]
    return []

def find_best_deals_for_budget(budget: float) -> Dict[str, Any]:
    """Legacy function for budget deals"""
    agent = CommerceQueryAgent()
    result = agent.process_query(f"find best deals for ₹{budget} budget")
    if result["status"] == "success":
        return result["result"]
    return {"deals": [], "total_cost": 0, "total_savings": 0, "remaining_budget": budget}

if __name__ == "__main__":
    # Test the query agent
    try:
        agent = CommerceQueryAgent()
        
        test_queries = [
            "Which app has cheapest onions right now?",
            "Show products with 30%+ discount on Blinkit",
            "Compare fruit prices between Zepto and Instamart",
            "Find best deals for ₹1000 grocery list"
        ]
        
        print("🧪 Testing Commerce Query Agent with SQL Backend")
        print("=" * 60)
        
        for i, query in enumerate(test_queries, 1):
            print(f"\n{i}. Testing: '{query}'")
            print("-" * 50)
            
            result = agent.process_query(query)
            
            if result["status"] == "success":
                print(f"✅ SUCCESS: {result['message']}")
                print(f"🔍 Generated SQL: {result.get('generated_sql', 'N/A')[:100]}...")
                print(f"⚡ Performance: {result.get('performance', {}).get('total_time_ms', 0):.2f}ms")
            else:
                print(f"❌ ERROR: {result['message']}")
        
        # Show database stats
        print(f"\n📊 Database Statistics:")
        stats = agent.get_database_stats()
        for key, value in stats.items():
            print(f"   • {key}: {value:,}")
        
        print("\n🎉 All tests completed!")
        
    except Exception as e:
        print(f"💥 Error: {e}")
        print("\nSetup Instructions:")
        print("1. Create .env file with: GEMINI_API_KEY=your_api_key_here")
        print("2. Get API key from: https://makersuite.google.com/app/apikey")
        print("3. Run: python database_setup.py")
        print("4. Then run: python query_agent.py") 