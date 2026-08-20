# Day 3 Practice — Student Record System (Part 3)
# Topic: sorted(), list comprehensions, string search, object comparison
# Goal: Write 3 logic functions for the Student Record System project

# ============================================================
# SETUP — Same Student class as Day 2 (copy-pasted for you)
# ============================================================

class Student:
    school = "Tech Academy"
    total_students = 0          # Class variable — tracks count

    def __init__(self, name, marks, section="A"):
        self.name = name
        self.marks = marks          # list of marks e.g. [85, 90, 78]
        self.section = section
        Student.total_students += 1

    def __repr__(self):#what it is explain and after explaination remove this comment
        return f"Student({self.name}, avg={self.get_avg():.1f})"

    # Helper — use this inside your functions
    def get_avg(self):
        return sum(self.marks) / len(self.marks)


# ============================================================
# FUNCTION 1: compare_students(s1, s2)
# ============================================================
# Takes two Student objects.
# Compares their averages and returns a string like:
#   "Sneha (91.67) > Uday (84.33)"   ← if s2 wins
#   "Uday (84.33) > Ravi (71.67)"    ← if s1 wins
#   "Uday and Ravi are equal (71.67)" ← if tied
#
# Hint: use .get_avg() and round() for both students

# Write your solution here:
def compare_students(s1, s2):
    avg1 = round(s1.get_avg(),2)
    avg2= round(s2.get_avg(),2)
    if avg1 > avg2:
        return f"{s1.name}({avg1}) > {s2.name}({avg2})"
    elif avg1<avg2:
        return f"{s2.name}({avg2}) > {s1.name}({avg1})"
    else:
        return f"{s1.name} and {s2.name} are equal ({avg1})"


# ============================================================
# FUNCTION 2: find_by_name(students, name)
# ============================================================
# Takes a list of Student objects and a name string.
# Searches case-insensitively (e.g. "sneha" should find "Sneha").
# Returns the Student object if found, None if not found.
#
# Hint: use .lower() and .strip() for safe comparison

# Write your solution here:
def find_by_name(students, name):
    for s in students:
        if s.name.lower()==name.lower():
            return s
    return None



# ============================================================
# FUNCTION 3: sort_by_grade(students)
# ============================================================
# Takes a list of Student objects.
# Returns a NEW list sorted by average marks — HIGHEST first.
# Do NOT modify the original list.
#
# Hint: use sorted() with key=lambda and reverse=True

# Write your solution here:
def sort_by_grade(students):
    re = sorted(students, key=lambda x: x.get_avg(), reverse=True)
    return re


# ============================================================
# TEST YOUR FUNCTIONS
# ============================================================

s1 = Student("Uday", [85, 90, 78])
s2 = Student("Ravi", [70, 65, 80])
s3 = Student("Sneha", [95, 88, 92])
s4 = Student("Priya", [50, 45, 55], section="B")

students = [s1, s2, s3, s4]

# Test 1: compare_students
print(compare_students(s1, s2))   # Uday (84.33) > Ravi (71.67)
print(compare_students(s1, s3))   # Sneha (91.67) > Uday (84.33)

# Test 2: find_by_name
result = find_by_name(students, "sneha")
print(result.name if result else "Not found")   # Sneha

result = find_by_name(students, "ghost")
print(result.name if result else "Not found")   # Not found

# Test 3: sort_by_grade
ranked = sort_by_grade(students)
for i, s in enumerate(ranked, start=1):
    print(f"{i}. {s.name} — {s.get_avg():.2f}")
# Expected:
# 1. Sneha — 91.67
# 2. Uday  — 84.33
# 3. Ravi  — 71.67
# 4. Priya — 50.00


# ============================================================
# BONUS CHALLENGE (optional, ~10 min)
# ============================================================
# 1. Add a list comprehension inside sort_by_grade() to also
#    print each student's grade (A/B/C/F) alongside their name.
#
# 2. Write a function get_section(students, section) that returns
#    only the students from a given section using a list comprehension.
#    Example: get_section(students, "B")  →  [Student(Priya, avg=50.0)]
