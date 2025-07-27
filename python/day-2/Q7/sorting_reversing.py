# You are given a list of employees, where each employee is represented as a tuple containing their name, salary, and department:
employees = [
    ("Alice", 70000, "HR"), 
    ("Bob", 50000, "Engineering"),
    ("Charlie", 60000, "Marketing"),
    ("David", 80000, "Engineering")]

def sort_employee_by_salary(ascending=True):
    sorted_employees = sorted(employees, key = lambda x: x[1], reverse=not ascending)
    return sorted_employees

def sort_employee_by_department_salary() :
    sorted_employees = sorted(employee, key = lambda x: (x[2], x[1]))
    return sorted_employees

# Reverse the order of the original list of employees without modifying the original.

def reverse_employee_list():
    reversed_employees = employees[::1]
    return reversed_employees

# Sort employees based on the length of their names.
def sort_employee_by_length_of_their_name():
    sorted_employees = sorted(employees, key = lambda x: len(x[0]))
    return sorted_employees

# Use .sort() when modifying the original list and sorted() when creating a new sorted list. Demonstrate both methods.
def sort_employee_in_place():
    employees.sort(key = lambda x: x[1])
    return employees

def sort_employee_new_list():
    sorted_employees = sorted(employees, key = lambda x: x[1])
    return sorted_employees  

