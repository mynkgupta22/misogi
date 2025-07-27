inventory = {
    "apples" : {"price": 1.50, "quantity" : 100},
    "bananas" : {"price": 0.75, "quantity" : 150},
    "oranges" : {"price": 1.00, "quantity": 80}
}

# Add a New Product

# Add a new product to the inventory with its price and quantity.

inventory["grapes"] = {"price": 2.00, "quantity" : 50}
print(inventory)

inventory["bananas"]["price"] = 1.00
print(inventory)

# Sell 25 Apples

# Simulate the sale of 25 apples by updating the quantity accordingly.

inventory["apples"]["quantity"] -=25
print(inventory)

# Calculate Total Inventory Value

# Compute the total value of the inventory using the formula:

# total = sum(price × quantity for all products)

total_inventory_value = sum(item["price"] * item["quantity"] for item in inventory.values())
print(total_inventory_value)

# Find Low Stock Products

# Identify and print all products whose quantity is below 100.

low_stock_products = [product for product, details in inventory.items() if details["quantity"] <100]
print(low_stock_products)
