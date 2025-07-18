import re
from mock_data import MockCommerceData
from typing import Dict, List, Any
import json

class CommerceQueryAgent:
    def __init__(self):
        self.data = MockCommerceData()
        self.query_patterns = {
            'cheapest_product': [
                r'which app has cheapest (.+?) right now',
                r'cheapest (.+?) on which platform',
                r'where to find cheapest (.+)',
                r'best price for (.+)',
                r'cheapest (.+)'
            ],
            'discount_products': [
                r'show products with (\d+)%?\+ discount on (.+)',
                r'(.+) products with (\d+)%? or more discount',
                r'discounts on (.+) above (\d+)%?',
                r'(.+) deals above (\d+)%?',
                r'(.+) products with (\d+)%? discount',
                r'(\d+)%? discount on (.+)'
            ],
            'compare_prices': [
                r'compare (.+) prices between (.+) and (.+)',
                r'price comparison of (.+) on (.+) vs (.+)',
                r'(.+) price difference between (.+) and (.+)'
            ],
            'budget_deals': [
                r'find best deals for ₹(\d+) grocery list',
                r'what can i buy with ₹(\d+)',
                r'best value for ₹(\d+) budget',
                r'grocery list for ₹(\d+)'
            ]
        }
    
    def process_query(self, query: str) -> Dict[str, Any]:
        """Process natural language query and return structured results."""
        query = query.lower().strip()
        
        # Try to match query patterns
        for query_type, patterns in self.query_patterns.items():
            for pattern in patterns:
                match = re.search(pattern, query)
                if match:
                    return self._execute_query(query_type, match.groups(), query)
        
        # If no pattern matches, try keyword-based approach
        return self._handle_fallback_query(query)
    
    def _execute_query(self, query_type: str, groups: tuple, original_query: str) -> Dict[str, Any]:
        """Execute the matched query type with extracted parameters."""
        
        try:
            if query_type == 'cheapest_product':
                product_name = groups[0]
                result = self.data.get_cheapest_product(product_name)
                
                if result:
                    return {
                        'status': 'success',
                        'query_type': 'cheapest_product',
                        'query': original_query,
                        'result': {
                            'product_name': result['product']['name'],
                            'platform': result['platform']['name'],
                            'original_price': f"₹{result['original_price']:.2f}",
                            'discounted_price': f"₹{result['discounted_price']:.2f}",
                            'discount_percent': f"{result['discount_percent']:.0f}%",
                            'savings': f"₹{result['savings']:.2f}",
                            'delivery_time': result['platform']['delivery_time']
                        },
                        'message': f"The cheapest {result['product']['name']} is available on {result['platform']['name']} for ₹{result['discounted_price']:.2f}"
                    }
                else:
                    return {
                        'status': 'error',
                        'message': f"Product '{product_name}' not found in our database"
                    }
            
            elif query_type == 'discount_products':
                if len(groups) == 2:
                    platform_name = groups[1] if groups[1].replace('%', '').replace('+', '').isdigit() == False else groups[0]
                    discount_percent = int(re.sub(r'[^\d]', '', groups[0] if groups[0].replace('%', '').replace('+', '').isdigit() else groups[1]))
                else:
                    platform_name = groups[0]
                    discount_percent = int(re.sub(r'[^\d]', '', groups[1]))
                
                results = self.data.get_products_with_discount(platform_name, discount_percent)
                
                if results:
                    formatted_results = []
                    for item in results:
                        formatted_results.append({
                            'product_name': item['product']['name'],
                            'original_price': f"₹{item['original_price']:.2f}",
                            'discounted_price': f"₹{item['discounted_price']:.2f}",
                            'discount_percent': f"{item['discount_percent']:.0f}%",
                            'savings': f"₹{item['savings']:.2f}",
                            'category': next(c['name'] for c in self.data.categories if c['id'] == item['product']['category_id'])
                        })
                    
                    return {
                        'status': 'success',
                        'query_type': 'discount_products',
                        'query': original_query,
                        'result': {
                            'platform': platform_name.title(),
                            'min_discount': f"{discount_percent}%",
                            'total_products': len(formatted_results),
                            'products': formatted_results
                        },
                        'message': f"Found {len(formatted_results)} products with {discount_percent}%+ discount on {platform_name.title()}"
                    }
                else:
                    return {
                        'status': 'error',
                        'message': f"No products found with {discount_percent}%+ discount on {platform_name}"
                    }
            
            elif query_type == 'compare_prices':
                category = groups[0]
                platform1 = groups[1]
                platform2 = groups[2]
                
                results = self.data.compare_prices(category, platform1, platform2)
                
                if results:
                    formatted_results = []
                    for item in results:
                        formatted_results.append({
                            'product_name': item['product']['name'],
                            'platform1': {
                                'name': item['platform1']['name'],
                                'price': f"₹{item['platform1']['price']:.2f}",
                                'discount': f"{item['platform1']['discount']:.0f}%" if item['platform1']['discount'] > 0 else "No discount"
                            },
                            'platform2': {
                                'name': item['platform2']['name'],
                                'price': f"₹{item['platform2']['price']:.2f}",
                                'discount': f"{item['platform2']['discount']:.0f}%" if item['platform2']['discount'] > 0 else "No discount"
                            },
                            'cheaper_platform': item['cheaper_platform'],
                            'price_difference': f"₹{item['price_difference']:.2f}"
                        })
                    
                    return {
                        'status': 'success',
                        'query_type': 'compare_prices',
                        'query': original_query,
                        'result': {
                            'category': category.title(),
                            'platform1': platform1.title(),
                            'platform2': platform2.title(),
                            'total_products_compared': len(formatted_results),
                            'comparison': formatted_results
                        },
                        'message': f"Compared {len(formatted_results)} {category} products between {platform1.title()} and {platform2.title()}"
                    }
                else:
                    return {
                        'status': 'error',
                        'message': f"No {category} products found for comparison between {platform1} and {platform2}"
                    }
            
            elif query_type == 'budget_deals':
                budget = float(groups[0])
                
                results = self.data.find_best_deals_for_budget(budget)
                
                if results['deals']:
                    formatted_deals = []
                    for deal in results['deals']:
                        formatted_deals.append({
                            'product_name': deal['product']['name'],
                            'platform': deal['platform']['name'],
                            'original_price': f"₹{deal['original_price']:.2f}",
                            'discounted_price': f"₹{deal['discounted_price']:.2f}",
                            'discount_percent': f"{deal['discount_percent']:.0f}%",
                            'savings': f"₹{deal['savings']:.2f}",
                            'value_score': f"{deal['value_score']:.2f}"
                        })
                    
                    return {
                        'status': 'success',
                        'query_type': 'budget_deals',
                        'query': original_query,
                        'result': {
                            'budget': f"₹{budget:.2f}",
                            'total_cost': f"₹{results['total_cost']:.2f}",
                            'total_savings': f"₹{results['total_savings']:.2f}",
                            'remaining_budget': f"₹{results['remaining_budget']:.2f}",
                            'total_items': len(formatted_deals),
                            'deals': formatted_deals
                        },
                        'message': f"Found {len(formatted_deals)} best deals within ₹{budget:.2f} budget, saving you ₹{results['total_savings']:.2f}"
                    }
                else:
                    return {
                        'status': 'error',
                        'message': f"No suitable deals found within ₹{budget:.2f} budget"
                    }
        
        except Exception as e:
            return {
                'status': 'error',
                'message': f"Error processing query: {str(e)}"
            }
    
    def _handle_fallback_query(self, query: str) -> Dict[str, Any]:
        """Handle queries that don't match specific patterns using keywords."""
        
        # Look for product names
        for product in self.data.products:
            if product['name'].lower() in query:
                if 'cheap' in query or 'best price' in query:
                    result = self.data.get_cheapest_product(product['name'])
                    if result:
                        return {
                            'status': 'success',
                            'query_type': 'cheapest_product',
                            'query': query,
                            'result': {
                                'product_name': result['product']['name'],
                                'platform': result['platform']['name'],
                                'original_price': f"₹{result['original_price']:.2f}",
                                'discounted_price': f"₹{result['discounted_price']:.2f}",
                                'discount_percent': f"{result['discount_percent']:.0f}%",
                                'savings': f"₹{result['savings']:.2f}",
                                'delivery_time': result['platform']['delivery_time']
                            },
                            'message': f"The cheapest {result['product']['name']} is available on {result['platform']['name']} for ₹{result['discounted_price']:.2f}"
                        }
        
                 # Look for platform names
        platform_names = [p['name'].lower() for p in self.data.platforms]
        found_platforms = [p for p in platform_names if p in query]
        
        if len(found_platforms) >= 2 and ('compare' in query or 'vs' in query):
            results = self.data.compare_prices('fruits', found_platforms[0], found_platforms[1])
            if results:
                formatted_results = []
                for item in results:
                    formatted_results.append({
                        'product_name': item['product']['name'],
                        'platform1': {
                            'name': item['platform1']['name'],
                            'price': f"₹{item['platform1']['price']:.2f}",
                            'discount': f"{item['platform1']['discount']:.0f}%" if item['platform1']['discount'] > 0 else "No discount"
                        },
                        'platform2': {
                            'name': item['platform2']['name'],
                            'price': f"₹{item['platform2']['price']:.2f}",
                            'discount': f"{item['platform2']['discount']:.0f}%" if item['platform2']['discount'] > 0 else "No discount"
                        },
                        'cheaper_platform': item['cheaper_platform'],
                        'price_difference': f"₹{item['price_difference']:.2f}"
                    })
                
                return {
                    'status': 'success',
                    'query_type': 'compare_prices',
                    'query': query,
                    'result': {
                        'category': 'Fruits',
                        'platform1': found_platforms[0].title(),
                        'platform2': found_platforms[1].title(),
                        'total_products_compared': len(formatted_results),
                        'comparison': formatted_results
                    },
                    'message': f"Compared {len(formatted_results)} fruit products between {found_platforms[0].title()} and {found_platforms[1].title()}"
                }
        
        # Look for discount mentions
        if 'discount' in query or '%' in query:
            discount_match = re.search(r'(\d+)%?', query)
            platform_match = None
            for platform in self.data.platforms:
                if platform['name'].lower() in query:
                    platform_match = platform['name']
                    break
            
            if discount_match and platform_match:
                discount_percent = int(discount_match.group(1))
                results = self.data.get_products_with_discount(platform_match, discount_percent)
                if results:
                    return {
                        'status': 'success',
                        'query_type': 'discount_products',
                        'query': query,
                        'result': results,
                        'message': f"Found {len(results)} products with {discount_percent}%+ discount on {platform_match}"
                    }
        
        return {
            'status': 'error',
            'message': "I couldn't understand your query. Try asking about: cheapest products, discounts, price comparisons, or budget deals.",
            'suggestions': [
                "Which app has cheapest onions right now?",
                "Show products with 30%+ discount on Blinkit",
                "Compare fruit prices between Zepto and Instamart",
                "Find best deals for ₹1000 grocery list"
            ]
        }
    
    def get_available_products(self) -> List[str]:
        """Return list of available products."""
        return [product['name'] for product in self.data.products]
    
    def get_available_platforms(self) -> List[str]:
        """Return list of available platforms."""
        return [platform['name'] for platform in self.data.platforms]
    
    def get_categories(self) -> List[str]:
        """Return list of available categories."""
        return [category['name'] for category in self.data.categories] 