price1 = int(input("Enter price of item 1: "))
quantity1 = int(input("Enter quantity of item 1: "))
price2 = int(input("Enter price of item 2: "))
quantity2 = int(input("Enter quantity of item 2: "))
price3 = int(input("Enter price of item 3: "))
quantity3 = int(input("Enter quantity of item 3: "))



print(f"Item 1: {price1} x {quantity1} = {price1 * quantity1}")
print(f"Item 2: {price2} x {quantity2} = {price2 * quantity2}")
print(f"Item 3: {price3} x {quantity3} = {price3 * quantity3}")

subTotal = price1 * quantity1 + price2 * quantity2 + price3 * quantity3

print(f"subtotal: {subTotal}")
print(f"tax (8.5%): {subTotal * 8.5 /100}")
print(f"total: {subTotal + subTotal * 8.5/100}")





