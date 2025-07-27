grades = [85, 92, 78, 90, 88, 76, 94, 89, 87, 91]

from typing import Dict, Any
# Given the list grades = [85, 92, 78, 90, 88, 76, 94, 89, 87, 91], perform the following operations:

# Slice grades from index 2 to 7
# Use list comprehension to find grades above 85
# Replace the grade at index 3 with 95
# Append three new grades
# Sort in descending order and display the top 5 grades

def grade_operations(grades: list):

    print(grades[2:8])
    print([grade for grade in grades if grade > 85])
    print(grades[:3] +[95] + grades[4:])
    print(grades + [93, 90, 88])
    print(sorted(grades,reverse = True)[:5])

grade_operations(grades)
