# Day 4 Practice — Student Record System (Part 4 — FINAL)
# Topic: Merging sections, report generation, CSV export
# Goal: Write the last 3 logic functions — then the website launches!

# ============================================================
# SETUP — Same Student class (with __str__ added today)
# ============================================================

class Student:
    school = "Tech Academy"
    total_students = 0

    def __init__(self, name, marks, section="A"):
        self.name = name
        self.marks = marks
        self.section = section
        Student.total_students += 1

    def __repr__(self):
        # Used by Python in console and when inside a list — for developers
        return f"Student({self.name}, avg={self.get_avg():.1f})"

    def __str__(self):
        # Used by print() and f-strings — for users
        return f"{self.name} [{self.get_avg():.1f}]"

    def get_avg(self):
        return sum(self.marks) / len(self.marks)


# ============================================================
# HELPER — get_grade(avg)
# ============================================================
# Returns letter grade based on average.
# You'll use this inside generate_report() and export_data().

def get_grade(avg):
    if avg >= 90: return "A"
    elif avg >= 75: return "B"
    elif avg >= 60: return "C"
    elif avg >= 40: return "D"
    else:          return "F"


# ============================================================
# FUNCTION 1: merge_sections(section_a, section_b)
# ============================================================
# Takes two lists of Student objects.
# Combines them into ONE new list (don't modify the originals!).
# Remove duplicates by name (case-insensitive).
# Return the merged list sorted by average — HIGHEST first.
#
# Hint: use a set() to track names already seen
# Hint: use sorted() with reverse=True at the end

# Write your solution here:
def merge_sections(section_a, section_b):
    merged=section_a + section_b
    unique_names =set()
    names=[]
    for s in merged:
        if s.name not in unique_names:
            names.append(s)
            unique_names.add(s.name.lower())
    sorted_obj=sorted(names, key=lambda s: s.get_avg(), reverse=True)
    return sorted_obj
        


# ============================================================
# FUNCTION 2: generate_report(students)
# ============================================================
# Takes a list of Student objects.
# Returns a list of dicts, one per student, sorted highest avg first.
# Each dict must have these keys:
#   "name"    -> student name (str)
#   "avg"     -> rounded to 2 decimal places (float)
#   "grade"   -> letter grade from get_grade() (str)
#   "status"  -> "Pass" if avg >= 40, else "Fail" (str)
#   "section" -> student's section (str)
#
# Example output:
# [
#   {"name": "Sneha", "avg": 91.67, "grade": "A", "status": "Pass", "section": "A"},
#   {"name": "Uday",  "avg": 84.33, "grade": "B", "status": "Pass", "section": "A"},
# ]

# Write your solution here:
def get_status(avg):
    status= True if avg > 40 else False
    return "pass" if status else "fail"

def generate_report(students):
    sorted_obj=sorted(students,key=lambda s:s.get_avg(),reverse=True)
    return_dict=[]
    for s in sorted_obj:
        return_dict.append({"name":s.name,"avg":round(s.get_avg(),2),"grade":get_grade(s.get_avg()),"status":get_status(s.get_avg()), "section":s.section})
    return return_dict

# ============================================================
# FUNCTION 3: export_data(students)
# ============================================================
# Takes a list of Student objects.
# Returns a single CSV-formatted string.
# First line must be the header: Name,Average,Grade,Status,Section
# Each following line: one student's data separated by commas.
#
# Example output (as a string):
# "Name,Average,Grade,Status,Section\nSneha,91.67,A,Pass,A\nUday,84.33,B,Pass,A"
#
# Hint: build a list of strings, then "\n".join(lines)
# Hint: use get_grade() and the same avg/status logic as generate_report

# Write your solution here:
def export_data(students):
    return_list=["Name,Average,Grade,Status,Section"]
    for s in students:
        return_list.append(f"{s.name},{round(s.get_avg(),2)},{get_grade(s.get_avg())},{get_status(s.get_avg())},{s.section}")
    return "\n".join(return_list)


# ============================================================
# TEST YOUR FUNCTIONS
# ============================================================

# Two separate sections
section_a = [
    Student("Uday",  [85, 90, 78]),
    Student("Sneha", [95, 88, 92]),
]
section_b = [
    Student("Ravi",  [70, 65, 80]),
    Student("Priya", [50, 45, 55], section="B"),
    Student("Uday",  [85, 90, 78]),   # duplicate — should be removed!
]

# Test 1: merge_sections
merged = merge_sections(section_a, section_b)
print("=== Merged (no duplicates, sorted) ===")
for s in merged:
    print(s)   # uses __str__
# Expected (highest avg first, Uday appears only once):
# Sneha [91.7]
# Uday [84.3]
# Ravi [71.7]
# Priya [50.0]

print()

# Test 2: generate_report
all_students = [
    Student("Uday",  [85, 90, 78]),
    Student("Ravi",  [70, 65, 80]),
    Student("Sneha", [95, 88, 92]),
    Student("Priya", [50, 45, 55], section="B"),
]
report = generate_report(all_students)
print("=== Report ===")
for row in report:
    print(row)
# Expected (each row is a dict):
# {'name': 'Sneha', 'avg': 91.67, 'grade': 'A', 'status': 'Pass', 'section': 'A'}
# {'name': 'Uday',  'avg': 84.33, 'grade': 'B', 'status': 'Pass', 'section': 'A'}
# {'name': 'Ravi',  'avg': 71.67, 'grade': 'C', 'status': 'Pass', 'section': 'A'}
# {'name': 'Priya', 'avg': 50.0,  'grade': 'D', 'status': 'Pass', 'section': 'B'}

print()

# Test 3: export_data
csv_output = export_data(all_students)
print("=== CSV Export ===")
print(csv_output)
# Expected:
# Name,Average,Grade,Status,Section
# Sneha,91.67,A,Pass,A
# Uday,84.33,B,Pass,A
# Ravi,71.67,C,Pass,A
# Priya,50.0,D,Pass,B


# ============================================================
# BONUS CHALLENGE (optional, ~10 min)
# ============================================================
# 1. Add a "rank" key to each dict in generate_report()
#    so the first student gets rank=1, second gets rank=2, etc.
#
# 2. In export_data(), sort students highest avg first
#    (same order as generate_report).
#
# 3. Write a function top_students(students, n=3) that
#    returns the top N students as a list of dicts (same format
#    as generate_report). Default N is 3.
