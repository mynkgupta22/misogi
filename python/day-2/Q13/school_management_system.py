school = {
    "Math": {
        "teacher": "Mr. Smith",
        "students": [("Alice", 85), ("Bob", 92), ("Carol", 78)]
    },
    "Science": {
        "teacher": "Ms. Johnson",
        "students": [("David", 88), ("Eve", 94), ("Frank", 82)]
    }
}
from typing import Dict, Any

# Print Teacher Names
# Iterate through all classes and print the name of each teacher.
def print_teachers(school: Dict[str, Dict[str, Any]]):
    for subject, details in school.items():
        print(f"Teacher for {subject}: {details["teacher"]}")

print_teachers(school)

# Calculate Class Average Grades
# For each class, calculate and display the average grade of the students.
def calculate_subject_average(school: Dict[str, Dict[str, Any]]):
    for subject, details in school.items():
        grades = [grade for _, grade in details["students"]]
        average = sum(grades) / len(grades)
        print(f"Average grade for {subject}: {average:.2f}")

calculate_subject_average(school)

# Find Top Student Across All Classes
# Identify the student with the highest grade among all students across every class.
def find_top_student(school: Dict[str, Dict[str, Any]]):
    top_student = None 
    top_grade = -1
    for details in school.values():
        for student,grade in details["students"]:
            if grade > top_grade:
                top_grade = grade
                top_student = student
    print(f"Top student: {top_student} with grade {top_grade}")

find_top_student(school)

# Use Unpacking
# Use tuple unpacking to extract and work with student names and grades separately.
def unpack_students(school: Dict[str, Dict[str, Any]]):
    for subject, details in school.items():
        for student, grade in details["students"]:
            print(f"Student: {student}, Grade: {grade}")

unpack_students(school)

