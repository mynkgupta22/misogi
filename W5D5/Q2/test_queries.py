#!/usr/bin/env python3
"""
Test script to verify all sample queries work correctly.
"""

from query_agent import CommerceQueryAgent
import json

def test_sample_queries():
    """Test all the sample queries mentioned in the requirements."""
    
    agent = CommerceQueryAgent()
    
    sample_queries = [
        "Which app has cheapest onions right now?",
        "Show products with 30%+ discount on Blinkit",
        "Compare fruit prices between Zepto and Instamart", 
        "Find best deals for ₹1000 grocery list"
    ]
    
    additional_test_queries = [
        "cheapest milk",
        "best price for tomatoes", 
        "Blinkit products with 40% discount",
        "what can i buy with ₹500",
        "zepto vs dunzo fruit prices",
        "cheapest apples",
        "discounts on Instamart above 25%"
    ]
    
    all_queries = sample_queries + additional_test_queries
    
    print("🧪 Testing Quick Commerce Price Comparison Queries")
    print("=" * 60)
    
    for i, query in enumerate(all_queries, 1):
        print(f"\n{i}. Testing: '{query}'")
        print("-" * 50)
        
        try:
            result = agent.process_query(query)
            
            if result['status'] == 'success':
                print(f"✅ SUCCESS: {result['message']}")
                
                # Print summary based on query type
                if result['query_type'] == 'cheapest_product':
                    r = result['result']
                    print(f"   📦 Product: {r['product_name']}")
                    print(f"   🏪 Platform: {r['platform']}")
                    print(f"   💰 Price: {r['discounted_price']} (was {r['original_price']})")
                    print(f"   🏷️ Discount: {r['discount_percent']}")
                    
                elif result['query_type'] == 'discount_products':
                    r = result['result']
                    print(f"   🔥 Found {r['total_products']} products on {r['platform']}")
                    print(f"   💸 Best discount: {max([int(p['discount_percent'].replace('%', '')) for p in r['products']])}%")
                    
                elif result['query_type'] == 'compare_prices':
                    r = result['result']
                    print(f"   ⚖️ Compared {r['total_products_compared']} products")
                    print(f"   📊 Between {r['platform1']} and {r['platform2']}")
                    
                elif result['query_type'] == 'budget_deals':
                    r = result['result']
                    print(f"   💰 Budget: {r['budget']}")
                    print(f"   🛍️ Items: {r['total_items']}")
                    print(f"   💸 Savings: {r['total_savings']}")
                    
            else:
                print(f"❌ ERROR: {result['message']}")
                if 'suggestions' in result:
                    print(f"   💡 Suggestions: {result['suggestions']}")
                
        except Exception as e:
            print(f"💥 EXCEPTION: {str(e)}")
    
    print("\n" + "=" * 60)
    print("🎯 Testing Summary")
    print("=" * 60)
    
    # Test data statistics
    print(f"📊 Data Statistics:")
    print(f"   • Products: {len(agent.data.products)}")
    print(f"   • Platforms: {len(agent.data.platforms)}")
    print(f"   • Categories: {len(agent.data.categories)}")
    print(f"   • Active Discounts: {len([d for d in agent.data.discounts if d['is_active']])}")
    print(f"   • Current Prices: {len(agent.data.current_prices)}")
    
    # Platform details
    print(f"\n🏪 Available Platforms:")
    for platform in agent.data.platforms:
        print(f"   • {platform['name']}: {platform['delivery_time']}, {platform['commission']}% commission")
    
    # Product categories
    print(f"\n📁 Product Categories:")
    for category in agent.data.categories:
        count = len([p for p in agent.data.products if p['category_id'] == category['id']])
        print(f"   • {category['name']}: {count} products")

def test_edge_cases():
    """Test edge cases and error handling."""
    
    agent = CommerceQueryAgent()
    
    print("\n🧪 Testing Edge Cases")
    print("=" * 60)
    
    edge_cases = [
        "",  # Empty query
        "xyz unknown product",  # Unknown product
        "cheapest xyz",  # Unknown product with pattern
        "show products with 99% discount on NonExistentApp",  # Unknown platform
        "compare prices between UnknownApp1 and UnknownApp2",  # Unknown platforms
        "find best deals for ₹0.50 grocery list",  # Very low budget
        "random gibberish query that makes no sense"  # Random text
    ]
    
    for i, query in enumerate(edge_cases, 1):
        print(f"\n{i}. Testing edge case: '{query}'")
        print("-" * 50)
        
        try:
            result = agent.process_query(query)
            
            if result['status'] == 'error':
                print(f"✅ Properly handled error: {result['message']}")
            else:
                print(f"⚠️ Unexpected success: {result['message']}")
                
        except Exception as e:
            print(f"💥 EXCEPTION: {str(e)}")

if __name__ == "__main__":
    test_sample_queries()
    test_edge_cases()
    
    print("\n🎉 All tests completed!")
    print("Ready to run the web application with: python app.py") 