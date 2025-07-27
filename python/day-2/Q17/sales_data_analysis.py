sales_data = [
    ("Q1", [("Jan", 1000), ("Feb", 1200), ("Mar", 1100)]),
    ("Q2", [("Apr", 1300), ("May", 1250), ("Jun", 1400)]),
    ("Q3", [("Jul", 1350), ("Aug", 1450), ("Sep", 1300)])
]

# Calculate Total Sales per Quarter
# Use unpacking to compute and display the total sales for each quarter.
def total_sales_per_quarter(sales_data):
    for quarter, months in sales_data:
        total = sum(sale for _,sale in months)
        print(f"Total sales for {quarter}: {total}")

total_sales_per_quarter(sales_data)


# Find the Month with Highest Sales
# Identify the month with the highest individual sales across all quarters.
def highest_sales_month(sales_data):
    highest_month = None
    highest_sales = -1
    for _, months in sales_data:
        for month, sales in months:
            if sales > highest_sales:
                highest_sales = sales
                highest_month = month
    print(f"Month with highest sales: {highest_month} with sales {highest_sales}")

highest_sales_month(sales_data)

# Create a Flat List of Monthly Sales
# Generate a flat list of all monthly sales in the format: ("Jan", 1000), ("Feb", 1200), ....
def flat_monthly_sales(sales_data):
    flat_sales =[ (month, sales) for _, months in sales_data for month, sales in months]
    print("Flat list of monthly sales:", flat_sales)

flat_monthly_sales(sales_data)

# Use Unpacking in Loops
# Use tuple unpacking while iterating to clearly separate months, sales values, and quarters.
def unpack_sales_data(sales_data):
    for quarter, months in sales_data:
        print(f"Sales data for {quarter}:")
        for month, sales in months:
            print(f"Month: {month}, Sales: {sales}")

unpack_sales_data(sales_data)            



