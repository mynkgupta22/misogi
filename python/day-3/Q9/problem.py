# Course class: represents a university course
class Course:
    total_enrollments = 0  # class variable for tracking all enrollments

    def __init__(self, course_code, name, instructor, credit_hours, max_students):
        self.course_code = course_code
        self.name = name
        self.instructor = instructor
        self.credit_hours = credit_hours
        self.max_students = max_students
        self.enrolled_students = []  # list of student IDs
        self.grades = {}  # mapping student_id -> grade
        self.waitlist = []  # students waiting for seat

    def __str__(self):
        return f"{self.name} ({self.course_code}) by {self.instructor}"

    def get_available_spots(self):
        return self.max_students - len(self.enrolled_students)

    def get_enrollment_count(self):
        return len(self.enrolled_students)

    def is_full(self):
        return len(self.enrolled_students) >= self.max_students

    def enroll_student(self, student_id):
        if student_id in self.enrolled_students:
            return "Student already enrolled."

        if self.is_full():
            self.waitlist.append(student_id)
            return "Course full. Student added to waitlist."

        self.enrolled_students.append(student_id)
        Course.total_enrollments += 1
        return "Enrollment successful."

    def add_grade(self, student_id, grade):
        self.grades[student_id] = grade

    def get_course_statistics(self):
        if not self.grades:
            return {"average": None, "min": None, "max": None}

        scores = list(self.grades.values())
        return {
            "average": round(sum(scores) / len(scores), 2),
            "min": min(scores),
            "max": max(scores)
        }

    @classmethod
    def get_total_enrollments(cls):
        return cls.total_enrollments


# Student class: represents a student enrolled in a university program
class Student:
    all_students = []  # list of all student objects

    def __init__(self, student_id, name, email, program):
        self.student_id = student_id
        self.name = name
        self.email = email
        self.program = program
        self.courses = []  # enrolled course codes
        self.grades = {}  # course_code -> grade

        Student.all_students.append(self)

    def __str__(self):
        return f"{self.name} ({self.program})"

    def enroll_in_course(self, course: Course):
        result = course.enroll_student(self.student_id)
        if "successful" in result:
            self.courses.append(course.course_code)
        return result

    def add_grade(self, course_code, grade):
        self.grades[course_code] = grade

    def calculate_gpa(self):
        if not self.grades:
            return 0.0

        total = sum(self.grades.values())
        gpa = total / len(self.grades)
        return round(gpa, 2)

    def get_transcript(self):
        return self.grades.copy()

    @classmethod
    def get_total_students(cls):
        return len(cls.all_students)

    @classmethod
    def get_average_gpa(cls):
        if not cls.all_students:
            return 0.0
        total_gpa = sum(st.calculate_gpa() for st in cls.all_students)
        return round(total_gpa / len(cls.all_students), 2)

    @classmethod
    def get_top_students(cls, top_n=1):
        sorted_students = sorted(cls.all_students, key=lambda s: s.calculate_gpa(), reverse=True)
        return [(s.name, s.calculate_gpa()) for s in sorted_students[:top_n]]


# ----------------------------
# Test Cases with Expected Output
# ----------------------------

# Test Case 1: Creating courses
math_course = Course("MATH101", "Calculus I", "Dr. Smith", 3, 30)
physics_course = Course("PHYS101", "Physics I", "Dr. Johnson", 4, 25)
cs_course = Course("CS101", "Programming Basics", "Prof. Brown", 3, 20)

print(f"Course: {math_course}")
print(f"Available spots in Math: {math_course.get_available_spots()}")

# Test Case 2: Creating students
student1 = Student("S001", "Alice Wilson", "alice@university.edu", "Computer Science")
student2 = Student("S002", "Bob Davis", "bob@university.edu", "Mathematics")
student3 = Student("S003", "Carol Lee", "carol@university.edu", "Physics")

print(f"Student: {student1}")
print(f"Total students: {Student.get_total_students()}")

# Test Case 3: Course enrollment
enrollment1 = student1.enroll_in_course(math_course)
enrollment2 = student1.enroll_in_course(cs_course)
enrollment3 = student2.enroll_in_course(math_course)

print(f"Alice's enrollment in Math: {enrollment1}")
print(f"Math course enrollment count: {math_course.get_enrollment_count()}")

# Test Case 4: GPA Calculation
student1.add_grade("MATH101", 85.5)
student1.add_grade("CS101", 92.0)
student2.add_grade("MATH101", 78.3)

print(f"Alice's GPA: {student1.calculate_gpa()}")
print(f"Alice's transcript: {student1.get_transcript()}")

# Test Case 5: Course statistics
math_course.add_grade("S001", 85.5)
math_course.add_grade("S002", 78.3)

course_stats = math_course.get_course_statistics()
print(f"Math course statistics: {course_stats}")

# Test Case 6: University-wide analytics
total_enrollments = Course.get_total_enrollments()
print(f"Total enrollments across all courses: {total_enrollments}")

average_gpa = Student.get_average_gpa()
print(f"University average GPA: {average_gpa}")

top_students = Student.get_top_students(2)
print(f"Top 2 students: {top_students}")

# Test Case 7: Waitlist management
# Enroll many students to exceed course limit
for i in range(25):  # math_course has 30 seats
    temp_student = Student(f"S100{i}", f"Student {i}", f"student{i}@uni.edu", "General")
    result = temp_student.enroll_in_course(math_course)

print(f"Course full status: {math_course.is_full()}")
print(f"Waitlist size: {len(math_course.waitlist)}")
