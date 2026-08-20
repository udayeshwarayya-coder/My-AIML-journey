# Day 2 Practice — Student Record System (Part 2)
# Topic: Instance vars, Class vars, @classmethod, @staticmethod, lambda
# Goal: Write 3 logic functions for the Student Record System project

# ============================================================
# SETUP — The Student class (build on this)
# ============================================================

class Student:
    school = "Tech Academy"
    total_students = 0          # Class variable — tracks count

    def __init__(self, name, marks, section="A"):
        self.name = name
        self.marks = marks          # list of marks e.g. [85, 90, 78]
        self.section = section
        Student.total_students += 1

    def __repr__(self):
        return f"Student({self.name}, avg={self.get_avg():.1f})"

    # Helper — you can use this inside other methods
    def get_avg(self):
        return sum(self.marks) / len(self.marks)


# ============================================================
# FUNCTION 1: count_students()
# ============================================================
# Returns the total number of Student objects created.
# Hint: Use the class variable Student.total_students
# Should work as both a @classmethod on Student AND as
# a standalone call.
#
# Expected output:
#   s1 = Student("Uday", [85, 90, 78])
#   s2 = Student("Ravi", [70, 65, 80])
#   s3 = Student("Sneha", [95, 88, 92])
#   print(Student.count_students())   # 3

# Write your solution here:
def count_students():

    return Student.total_students

# ============================================================
# FUNCTION 2: get_topper(students)
# ============================================================
# Takes a list of Student objects.
# Returns the Student with the HIGHEST average marks.
# Hint: Use max() with a lambda key.
#
# Expected output:
#   students = [s1, s2, s3]
#   topper = get_topper(students)
#   print(topper.name)    # Sneha  (avg = 91.67)

# Write your solution here:
def get_topper(students):
    topper=max(students,key=lambda x:x.get_avg())
    return topper

# ============================================================
# FUNCTION 3: calculate_avg(student)
# ============================================================
# Takes a single Student object.
# Returns their average marks rounded to 2 decimal places.
# Bonus: Also return their grade (A/B/C/F based on avg)
#
# Grade scale:
#   A  → avg >= 85
#   B  → avg >= 70
#   C  → avg >= 55
#   F  → below 55
#
# Expected output:
#   result = calculate_avg(s1)
#   print(result)   # {"name": "Uday", "avg": 84.33, "grade": "B"}

# Write your solution here:
def calculate_avg(student):
    avg=round(sum(student.marks)/len(student.marks),2)
    grade=""    
    if avg>=85: 
        grade="A"
    elif avg>=70:
        grade="B"
    elif avg>=55:
        grade="C"
    else:
        grade="F"
    return {"name":student.name,"avg":avg,"grade":grade}
# ============================================================
# TEST YOUR FUNCTIONS
# ============================================================

s1 = Student("Uday", [85, 90, 78])
s2 = Student("Ravi", [70, 65, 80])
s3 = Student("Sneha", [95, 88, 92])
s4 = Student("Priya", [50, 45, 55], section="B")

students = [s1, s2, s3, s4]

# Test 1: count_students
print(Student.total_students)    # Expected: 4

# Test 2: get_topper
topper = get_topper(students)
print(f"Topper: {topper.name}")    # Expected: Sneha

# Test 3: calculate_avg
print(calculate_avg(s1))           # Expected: {"name": "Uday", "avg": 84.33, "grade": "B"}
print(calculate_avg(s4))           # Expected: {"name": "Priya", "avg": 50.0, "grade": "F"}


# ============================================================
# BONUS CHALLENGE (optional, 10 min extra)
# ============================================================
# Add an @staticmethod called `letter_grade(avg)` to the
# Student class that returns "A", "B", "C", or "F" based on avg.
# Refactor calculate_avg() to use it.
#
# Also fix the Day 1 Library bug:
#   is_read should be a boolean (False), not a string ('false')
#   so that `not book.is_read` works correctly.
