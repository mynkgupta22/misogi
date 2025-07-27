from collections import defaultdict

class Product:
    _total_products = 0
    _category_count = defaultdict(int)

    def __init__(self, product_id, name, price, category, stock_quantity):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.category = category
        self.stock_quantity = stock_quantity

        Product._total_products += 1
        Product._category_count[category] += 1

    def get_product_info(self):
        return f"{self.name} ({self.category}) - ${self.price:.2f}, Stock: {self.stock_quantity}"

    @classmethod
    def get_total_products(cls):
        return cls._total_products

    @classmethod
    def get_most_popular_category(cls):
        if not cls._category_count:
            return None
        return max(cls._category_count, key=cls._category_count.get)

    def reduce_stock(self, quantity):
        if self.stock_quantity >= quantity:
            self.stock_quantity -= quantity
            return True
        return False

class Customer:
    _total_revenue = 0.0

    def __init__(self, customer_id, name, email, membership_type='regular'):
        self.customer_id = customer_id
        self.name = name
        self.email = email
        self.membership_type = membership_type

    def __str__(self):
        return f"{self.name} ({self.membership_type})"

    def get_discount_rate(self):
        if self.membership_type == 'premium':
            return 10
        elif self.membership_type == 'gold':
            return 5
        else:
            return 0

    @classmethod
    def add_revenue(cls, amount):
        cls._total_revenue += amount

    @classmethod
    def get_total_revenue(cls):
        return round(cls._total_revenue, 2)

class ShoppingCart:
    def __init__(self, customer):
        self.customer = customer
        self.items = {}  # product_id -> (product, quantity)

    def add_item(self, product, quantity):
        if product.product_id in self.items:
            self.items[product.product_id][1] += quantity
        else:
            self.items[product.product_id] = [product, quantity]

    def remove_item(self, product_id):
        if product_id in self.items:
            del self.items[product_id]

    def clear_cart(self):
        self.items.clear()

    def get_total_items(self):
        return sum(quantity for _, quantity in self.items.values())

    def get_cart_items(self):
        return {pid: (prod.name, qty) for pid, (prod, qty) in self.items.items()}

    def get_subtotal(self):
        return round(sum(prod.price * qty for prod, qty in self.items.values()), 2)

    def calculate_total(self):
        subtotal = self.get_subtotal()
        discount_rate = self.customer.get_discount_rate()
        discount_amount = subtotal * (discount_rate / 100)
        return round(subtotal - discount_amount, 2)

    def place_order(self):
        # Check stock
        for product, quantity in self.items.values():
            if product.stock_quantity < quantity:
                return "Order failed: Insufficient stock for some items."

        # Deduct stock
        for product, quantity in self.items.values():
            product.reduce_stock(quantity)

        # Add revenue
        total_price = self.calculate_total()
        Customer.add_revenue(total_price)

        self.clear_cart()
        return f"Order placed successfully! Total: ${total_price}"


# ----------------------------
# Test Cases
# ----------------------------

# Test Case 1
laptop = Product("P001", "Gaming Laptop", 1299.99, "Electronics", 10)
book = Product("P002", "Python Programming", 49.99, "Books", 25)
shirt = Product("P003", "Cotton T-Shirt", 19.99, "Clothing", 50)

print(f"Product info: {laptop.get_product_info()}")
print(f"Total products in system: {Product.get_total_products()}")

# Test Case 2
customer = Customer("C001", "John Doe", "john@email.com", "premium")
cart = ShoppingCart(customer)

print(f"Customer: {customer}")
print(f"Customer discount: {customer.get_discount_rate()}%")

# Test Case 3
cart.add_item(laptop, 1)
cart.add_item(book, 2)
cart.add_item(shirt, 3)

print(f"Cart total items: {cart.get_total_items()}")
print(f"Cart subtotal: ${cart.get_subtotal()}")

# Test Case 4
final_total = cart.calculate_total()
print(f"Final total with {customer.get_discount_rate()}% discount: ${final_total}")

# Test Case 5
print(f"Laptop stock before order: {laptop.stock_quantity}")
order_result = cart.place_order()
print(f"Order result: {order_result}")
print(f"Laptop stock after order: {laptop.stock_quantity}")

# Test Case 6
popular_category = Product.get_most_popular_category()
print(f"Most popular category: {popular_category}")

total_revenue = Customer.get_total_revenue()
print(f"Total revenue: ${total_revenue}")

# Test Case 7
cart.remove_item("P002")  # Remove book
print(f"Items after removal: {cart.get_cart_items()}")

cart.clear_cart()
print(f"Items after clearing: {cart.get_total_items()}")
