items = ["apple", "banana", "orange"]
cart = []

def add_item_to_cart(cart, item):
    if item in items:
        cart.append(item)
        print( f"{item} has been added to the cart.")
    else:
        print( f"{item} is not available.")

def remove_item_from_cart(cart, item):
    if item in cart:
        cart.remove(item)
        print( f"{item} has been removed from the cart.")
    else:
        print( f"{item} is not in the cart.")

def remove_last_item_from_cart(cart):
    if cart:
        item = cart.pop()
        print( f"{item} has been removed from the cart.")
    else:
        print("The cart is empty.")   

def view_item_in_alphabetical_order(cart):
    if cart:
        sorted_cart = sorted(cart)
        print("Items in the cart in alphabetical order:")
        for item in sorted_cart:
            print(item)
    else:
        print("The cart is empty.")

def view_cart(cart):
    if cart:
        for item in cart:
            print(f"{cart.index(item)}: {item}")
    else:
        print("The cart is empty.")           
        