# Data Processing with enumerate()

students = ["Alice", "Bob", "Carol", "David", "Eve"]
scores = [85, 92, 78, 88, 95]



# Create a Numbered List of Students
# Print each student’s name with a number starting from 1 (e.g., 1. Alice).
def numbered_students(students: list):
    for index, student in enumerate(students, start=1):
        print(f"{index}. {student}")
numbered_students(students)

# Pair Students with Their Scores Using enumerate()
# Combine both lists to display each student's name alongside their score.
def pair_students_scores(students:list, scores: list):
    for index, (student, score) in enumerate(zip(students, scores), start=1):
        print(f"{index}. {student}: {score}")
pair_students_scores(students, scores)



# Find Positions of High Scorers
# Identify and print the positions (indices) of students who scored above 90.
def high_scorers_positions(students: list, scores: list):
    high_scores = [(index, student) for index, (student, score) in enumerate (zip(students, scores)) if score >90]
    print("High Scorers (above 90):")
    for index, student in high_scores:
        print(f"Position {index}: {student}")
high_scorers_positions(students, scores)



# Map Positions to Student Names
# Create a dictionary where keys are positions (starting from 0) and values are the student names.
def map_positions_to_students(students: list):
    position_map = {index: student for index, student in enumerate(students)}
    print("Position to Student Mapping:")
    for position, student in position_map.items():
        print(f"Position {position}: {student}")
map_positions_to_students(students)



