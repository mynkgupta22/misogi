
products = ["Laptop", "Smartphone", "Tablet", "Smartwatch"]
prices= [1000.20, 800.50, 300.75, 250.00]
quantities = [5, 10, 15, 20]

# Create Product-Price Pairs

# Use zip() to pair each product with its corresponding price.
product_price_pairs = list(zip(products, prices))
print(product_price_pairs)

# Calculate Total Value for Each Product

# For each product, calculate the total inventory value using the formula: price × quantity.

total_values = [price * quantity for price, quantity in zip(prices,quantities)]

print(total_values)

# Build a Product Catalog Dictionary

#Create a dictionary where each product maps to another dictionary containing its price and quantity.
product_catalog = {
    product: {"price": price, "quantity" : quantity}
    for product, price, quantity in zip(products, prices, quantities)
}

print(product_catalog)

# Find Low Stock Products

# Identify and print the names of products with a quantity less than 10.

low_stock_products = [product for product,quantity in zip (products, quantities) if quantity <10]
print(low_stock_products)

