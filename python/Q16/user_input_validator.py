flag = True
while flag:
    try:
     age = int(input("Enter your age(1-120): "))
     if age < 1 or age > 120:
        raise ValueError("Out of Range.Age must be between 1 and 120.")
     flag = False    
     print(f"You entered a valid age: {age}")
    except ValueError:
     print("Invalid input. Please enter a valid number.")
