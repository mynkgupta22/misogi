import random
from datetime import datetime, timedelta
import json

class MockCommerceData:
    def __init__(self):
        self.platforms = [
            {"id": 1, "name": "Blinkit", "commission": 15.0, "delivery_time": "10-15 min"},
            {"id": 2, "name": "Zepto", "commission": 12.0, "delivery_time": "10-15 min"},
            {"id": 3, "name": "Instamart", "commission": 18.0, "delivery_time": "15-30 min"},
            {"id": 4, "name": "BigBasket Now", "commission": 20.0, "delivery_time": "15-45 min"},
            {"id": 5, "name": "Dunzo", "commission": 22.0, "delivery_time": "20-45 min"}
        ]
        
        self.categories = [
            {"id": 1, "name": "Vegetables", "parent_id": None},
            {"id": 2, "name": "Fruits", "parent_id": None},
            {"id": 3, "name": "Dairy", "parent_id": None},
            {"id": 4, "name": "Snacks", "parent_id": None},
            {"id": 5, "name": "Beverages", "parent_id": None},
            {"id": 6, "name": "Household", "parent_id": None},
            {"id": 7, "name": "Personal Care", "parent_id": None}
        ]
        
        self.products = [
            # Vegetables
            {"id": 1, "name": "Onions", "category_id": 1, "brand": "Local", "unit": "kg", "description": "Fresh red onions"},
            {"id": 2, "name": "Tomatoes", "category_id": 1, "brand": "Local", "unit": "kg", "description": "Fresh tomatoes"},
            {"id": 3, "name": "Potatoes", "category_id": 1, "brand": "Local", "unit": "kg", "description": "Fresh potatoes"},
            {"id": 4, "name": "Carrots", "category_id": 1, "brand": "Local", "unit": "kg", "description": "Fresh carrots"},
            
            # Fruits
            {"id": 5, "name": "Bananas", "category_id": 2, "brand": "Local", "unit": "dozen", "description": "Fresh bananas"},
            {"id": 6, "name": "Apples", "category_id": 2, "brand": "Kashmir", "unit": "kg", "description": "Kashmir apples"},
            {"id": 7, "name": "Oranges", "category_id": 2, "brand": "Nagpur", "unit": "kg", "description": "Nagpur oranges"},
            {"id": 8, "name": "Mangoes", "category_id": 2, "brand": "Alphonso", "unit": "kg", "description": "Alphonso mangoes"},
            
            # Dairy
            {"id": 9, "name": "Milk", "category_id": 3, "brand": "Amul", "unit": "1L", "description": "Fresh toned milk"},
            {"id": 10, "name": "Curd", "category_id": 3, "brand": "Amul", "unit": "500g", "description": "Fresh curd"},
            {"id": 11, "name": "Paneer", "category_id": 3, "brand": "Amul", "unit": "200g", "description": "Fresh paneer"},
            
            # Snacks
            {"id": 12, "name": "Chips", "category_id": 4, "brand": "Lays", "unit": "pack", "description": "Classic salted chips"},
            {"id": 13, "name": "Biscuits", "category_id": 4, "brand": "Parle G", "unit": "pack", "description": "Glucose biscuits"},
            
            # Beverages
            {"id": 14, "name": "Coca Cola", "category_id": 5, "brand": "Coca Cola", "unit": "500ml", "description": "Soft drink"},
            {"id": 15, "name": "Water Bottle", "category_id": 5, "brand": "Bisleri", "unit": "1L", "description": "Mineral water"},
        ]
        
        self.current_prices = self._generate_current_prices()
        self.price_history = self._generate_price_history()
        self.discounts = self._generate_discounts()
        self.availability = self._generate_availability()
        
    def _generate_current_prices(self):
        prices = []
        base_prices = {
            1: 45,   # Onions
            2: 50,   # Tomatoes
            3: 30,   # Potatoes
            4: 60,   # Carrots
            5: 40,   # Bananas
            6: 150,  # Apples
            7: 80,   # Oranges
            8: 200,  # Mangoes
            9: 60,   # Milk
            10: 45,  # Curd
            11: 80,  # Paneer
            12: 20,  # Chips
            13: 10,  # Biscuits
            14: 40,  # Coca Cola
            15: 20,  # Water
        }
        
        for product_id, base_price in base_prices.items():
            for platform in self.platforms:
                # Add some variation between platforms
                price_variation = random.uniform(0.8, 1.3)
                current_price = round(base_price * price_variation, 2)
                
                prices.append({
                    "id": len(prices) + 1,
                    "product_id": product_id,
                    "platform_id": platform["id"],
                    "price": current_price,
                    "mrp": round(current_price * 1.2, 2),
                    "last_updated": datetime.now() - timedelta(minutes=random.randint(1, 60))
                })
        
        return prices
    
    def _generate_price_history(self):
        history = []
        for price in self.current_prices:
            # Generate some historical prices
            for i in range(5):
                historical_price = price["price"] * random.uniform(0.9, 1.1)
                history.append({
                    "id": len(history) + 1,
                    "product_id": price["product_id"],
                    "platform_id": price["platform_id"],
                    "price": round(historical_price, 2),
                    "recorded_at": datetime.now() - timedelta(days=i+1)
                })
        return history
    
    def _generate_discounts(self):
        discounts = []
        
        # Add some random discounts
        discount_products = random.sample(range(1, 16), 8)
        
        for i, product_id in enumerate(discount_products):
            platform_id = random.choice([p["id"] for p in self.platforms])
            discount_percent = random.choice([10, 15, 20, 25, 30, 35, 40, 50])
            
            discounts.append({
                "id": i + 1,
                "product_id": product_id,
                "platform_id": platform_id,
                "discount_percent": discount_percent,
                "discount_type": "percentage",
                "start_date": datetime.now() - timedelta(days=1),
                "end_date": datetime.now() + timedelta(days=7),
                "is_active": True
            })
        
        return discounts
    
    def _generate_availability(self):
        availability = []
        
        for price in self.current_prices:
            # Most products are in stock, some are out of stock randomly
            is_available = random.choice([True, True, True, True, False])  # 80% availability
            stock_quantity = random.randint(0 if not is_available else 10, 100)
            
            availability.append({
                "id": len(availability) + 1,
                "product_id": price["product_id"],
                "platform_id": price["platform_id"],
                "is_available": is_available,
                "stock_quantity": stock_quantity,
                "estimated_delivery": random.choice(["10-15 min", "15-30 min", "30-45 min"]),
                "last_updated": datetime.now() - timedelta(minutes=random.randint(1, 30))
            })
        
        return availability
    
    def get_product_by_name(self, name):
        for product in self.products:
            if name.lower() in product["name"].lower():
                return product
        return None
    
    def get_platform_by_name(self, name):
        for platform in self.platforms:
            if name.lower() in platform["name"].lower():
                return platform
        return None
    
    def get_cheapest_product(self, product_name):
        product = self.get_product_by_name(product_name)
        if not product:
            return None
        
        product_prices = [p for p in self.current_prices if p["product_id"] == product["id"]]
        if not product_prices:
            return None
        
        # Apply discounts
        for price in product_prices:
            discount = next((d for d in self.discounts 
                           if d["product_id"] == product["id"] 
                           and d["platform_id"] == price["platform_id"] 
                           and d["is_active"]), None)
            if discount:
                price["discounted_price"] = price["price"] * (1 - discount["discount_percent"] / 100)
                price["discount_percent"] = discount["discount_percent"]
            else:
                price["discounted_price"] = price["price"]
                price["discount_percent"] = 0
        
        cheapest = min(product_prices, key=lambda x: x["discounted_price"])
        platform = next(p for p in self.platforms if p["id"] == cheapest["platform_id"])
        
        return {
            "product": product,
            "platform": platform,
            "original_price": cheapest["price"],
            "discounted_price": cheapest["discounted_price"],
            "discount_percent": cheapest["discount_percent"],
            "savings": cheapest["price"] - cheapest["discounted_price"]
        }
    
    def get_products_with_discount(self, platform_name, min_discount_percent):
        platform = self.get_platform_by_name(platform_name)
        if not platform:
            return []
        
        results = []
        for discount in self.discounts:
            if (discount["platform_id"] == platform["id"] 
                and discount["discount_percent"] >= min_discount_percent 
                and discount["is_active"]):
                
                product = next(p for p in self.products if p["id"] == discount["product_id"])
                price = next(p for p in self.current_prices 
                           if p["product_id"] == discount["product_id"] 
                           and p["platform_id"] == platform["id"])
                
                discounted_price = price["price"] * (1 - discount["discount_percent"] / 100)
                
                results.append({
                    "product": product,
                    "platform": platform,
                    "original_price": price["price"],
                    "discounted_price": discounted_price,
                    "discount_percent": discount["discount_percent"],
                    "savings": price["price"] - discounted_price
                })
        
        return sorted(results, key=lambda x: x["discount_percent"], reverse=True)
    
    def compare_prices(self, category, platform1_name, platform2_name):
        platform1 = self.get_platform_by_name(platform1_name)
        platform2 = self.get_platform_by_name(platform2_name)
        
        if not platform1 or not platform2:
            return []
        
        category_products = [p for p in self.products if p["category_id"] == 2]  # Fruits
        results = []
        
        for product in category_products:
            price1 = next((p for p in self.current_prices 
                          if p["product_id"] == product["id"] 
                          and p["platform_id"] == platform1["id"]), None)
            price2 = next((p for p in self.current_prices 
                          if p["product_id"] == product["id"] 
                          and p["platform_id"] == platform2["id"]), None)
            
            if price1 and price2:
                # Apply discounts
                discount1 = next((d for d in self.discounts 
                               if d["product_id"] == product["id"] 
                               and d["platform_id"] == platform1["id"] 
                               and d["is_active"]), None)
                discount2 = next((d for d in self.discounts 
                               if d["product_id"] == product["id"] 
                               and d["platform_id"] == platform2["id"] 
                               and d["is_active"]), None)
                
                final_price1 = price1["price"] * (1 - (discount1["discount_percent"] if discount1 else 0) / 100)
                final_price2 = price2["price"] * (1 - (discount2["discount_percent"] if discount2 else 0) / 100)
                
                cheaper_platform = platform1["name"] if final_price1 < final_price2 else platform2["name"]
                price_difference = abs(final_price1 - final_price2)
                
                results.append({
                    "product": product,
                    "platform1": {
                        "name": platform1["name"],
                        "price": final_price1,
                        "discount": discount1["discount_percent"] if discount1 else 0
                    },
                    "platform2": {
                        "name": platform2["name"],
                        "price": final_price2,
                        "discount": discount2["discount_percent"] if discount2 else 0
                    },
                    "cheaper_platform": cheaper_platform,
                    "price_difference": price_difference
                })
        
        return results
    
    def find_best_deals_for_budget(self, budget):
        all_deals = []
        
        for product in self.products:
            cheapest = self.get_cheapest_product(product["name"])
            if cheapest and cheapest["discounted_price"] <= budget:
                all_deals.append({
                    **cheapest,
                    "value_score": cheapest["savings"] / cheapest["discounted_price"] if cheapest["discounted_price"] > 0 else 0
                })
        
        # Sort by value score (highest savings percentage first)
        all_deals.sort(key=lambda x: x["value_score"], reverse=True)
        
        # Select deals that fit within budget
        selected_deals = []
        total_cost = 0
        
        for deal in all_deals:
            if total_cost + deal["discounted_price"] <= budget:
                selected_deals.append(deal)
                total_cost += deal["discounted_price"]
        
        return {
            "deals": selected_deals,
            "total_cost": total_cost,
            "total_savings": sum(deal["savings"] for deal in selected_deals),
            "remaining_budget": budget - total_cost
        } 