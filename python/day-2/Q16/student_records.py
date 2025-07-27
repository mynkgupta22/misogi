# (student_id, name, grade, age)

students = [
    (101, "Alice", 85, 20),
    (102, "Bob", 92, 19),
    (103, "Carol", 78, 21),
    (104, "David", 88, 20)
]
from typing import Dict, Any



# Find the Student with the Highest Grade
# Identify and print the student who has the highest grade from the list.
def find_top_student(students: list):
    top_student = max(students, key = lambda x :x[2])
    print(f"Top student: {top_student[1]} with grade {top_student[2]}")

find_top_student(students)

# Create a Name-Grade List
# Generate a new list containing only the name and grade of each student in the format: ("Alice", 85).
def create_names_grades_list(students: list):
    names_grades = [(student[1],student[2]) for student in students]
    print("Names and Grades List:", names_grades)
create_names_grades_list(students)

# Demonstrate Tuple Immutability
# Attempt to change the grade of a student in the original list and show why this is not allowed with tuples. Explain briefly why tuples are preferred for immutable records like student data.

def demonstrate_tuple_immutability(students: list):
    try:
        students[0][2] = 90
    except TypeError as e:
        print("Error:", e)
        print("Tuples are immutable, meaning their elements cannot be changed after creation. This is why tuples are preferred for records like student data, as it ensures the integrity of the data.")

demonstrate_tuple_immutability(students)