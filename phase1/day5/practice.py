# Day 5 Practice — Employee Payroll System (Part 1)
# Topic: Single Inheritance, super()
# Goal: Write 3 logic functions for Project 2

# ============================================================
# SETUP — Employee base class + Manager child class
# ============================================================
# Read concepts.md first (10 min), then come back here.

# The Employee class is provided — study it carefully.
# You'll be building on top of this for Days 5-8.

class Employee:
    company = "Tikota group of companies"              # class variable (shared by all employees)
    total_employees = 0               # tracks headcount

    def __init__(self, name, emp_id, base_salary, department="General"):
        self.name = name
        self.emp_id = emp_id
        self.base_salary = base_salary
        self.department = department
        Employee.total_employees += 1

    def __str__(self):
        return f"{self.name} [{self.emp_id}] — {self.department}"

    def __repr__(self):
        return f"Employee(name={self.name!r}, emp_id={self.emp_id!r}, salary={self.base_salary})"


# ============================================================
# FUNCTION 1: calculate_base_pay(employee)
# ============================================================
# Takes ONE Employee object (or a Manager — which is also an Employee).
# Returns the employee's base_salary as a float.
# Simple today! The complexity comes in Day 6 (bonuses).
#
# Example:
#   e = Employee("Uday", "E001", 50000)
#   calculate_base_pay(e)  →  50000
#
# Hint: just access the right attribute

# Write your solution here:
def calculate_base_pay(employee):
    return employee.base_salary


# ============================================================
# FUNCTION 2: get_details(employee)
# ============================================================
# Takes ONE Employee object.
# Returns a neatly formatted string with:
#   - Name
#   - Employee ID
#   - Department
#   - Base salary (formatted with ₹ and commas, e.g. ₹50,000)
#
# Example output:
#   "Name: Uday | ID: E001 | Dept: Engineering | Salary: ₹50,000"
#
# Hint: f-string with :, for number formatting → f"{50000:,}" → "50,000"

# Write your solution here:
def get_details(employee):
    return f"{"Name":} {employee.name}| {"ID":} {employee.emp_id}| {"Department":} {employee.department}| {"Salary":}{employee.base_salary}"


# ============================================================
# FUNCTION 3: build Manager class (it IS the function today!)
# ============================================================
# Write a Manager class that inherits from Employee.
# Manager has everything Employee has, PLUS:
#   - team_size (int) — how many people they manage
#
# Manager's __init__ must:
#   1. Accept: name, emp_id, base_salary, department, team_size
#   2. Call super().__init__() for the first 4 params
#   3. Set self.team_size
#
# Manager must also have a method:
#   get_team_info(self) → returns a string like:
#   "Arjun manages a team of 8 people."
#
# Example:
#   m = Manager("Arjun", "M001", 80000, "Engineering", team_size=8)
#   m.name         →  "Arjun"          (inherited from Employee)
#   m.team_size    →  8                (Manager's own)
#   m.get_team_info() → "Arjun manages a team of 8 people."
#   get_details(m) →  should work too! (inherited method behavior)

# Write your Manager class here:
class Manager(Employee):
    def __init__(self, name, emp_id, base_salary, department="General",team_size=0):
        super().__init__(name, emp_id, base_salary, department)
        self.team_size = team_size
    def get_team_info(self):
        return f"{self.name} manages a team of {self.team_size} people."


# ============================================================
# TEST YOUR CODE
# ============================================================

print("=" * 50)
print("TEST 1 — calculate_base_pay()")
print("=" * 50)

e1 = Employee("Uday", "E001", 50000, "Engineering")
e2 = Employee("Sneha", "E002", 42000, "Marketing")

print(calculate_base_pay(e1))   # Expected: 50000
print(calculate_base_pay(e2))   # Expected: 42000


print()
print("=" * 50)
print("TEST 2 — get_details()")
print("=" * 50)

print(get_details(e1))
# Expected: "Name: Uday | ID: E001 | Dept: Engineering | Salary: ₹50,000"
print(get_details(e2))
# Expected: "Name: Sneha | ID: E002 | Dept: Marketing | Salary: ₹42,000"


print()
print("=" * 50)
print("TEST 3 — Manager class")
print("=" * 50)

m = Manager("Arjun", "M001", 80000, "Engineering", team_size=8)

# Inherited attributes (from Employee)
print(m.name)         # Expected: Arjun
print(m.emp_id)       # Expected: M001
print(m.base_salary)  # Expected: 80000
print(m.department)   # Expected: Engineering

# Manager's own attribute
print(m.team_size)    # Expected: 8

# Manager's own method
print(m.get_team_info())
# Expected: "Arjun manages a team of 8 people."

# Inherited method works on Manager too!
print(get_details(m))
# Expected: "Name: Arjun | ID: M001 | Dept: Engineering | Salary: ₹80,000"

# isinstance checks
print(isinstance(m, Manager))    # Expected: True
print(isinstance(m, Employee))   # Expected: True  ← Manager IS also an Employee

# class variable is shared
print(Employee.total_employees)  # Expected: 3 (e1, e2, m all created Employee objects)


# ============================================================
# BONUS CHALLENGE (optional — ~10 min)
# ============================================================
# 1. Add an Intern class that also inherits from Employee.
#    Intern has:
#    - stipend (float) — their monthly stipend (separate from base_salary)
#    - college (str) — which college they're from
#    - A method: get_intern_info() → "Ravi from IIT interning in Marketing."
class Intern(Employee):
    def __init__(self,name,emp_id,base_salary,department,stipend=0.0,college="xyz"):
        super().__init__(name,emp_id,base_salary,department)
        self.stipend = stipend
        self.college = college
    def get_intern_info(self):
        return f"{self.name} from {self.college} interning from {self.department}"
# 2. Write a function employee_summary(employees) that takes a LIST
#    of Employee/Manager/Intern objects and prints:
#    - Total number of employees
#    - Total payroll (sum of all base salaries)
#    - Names of all Managers (use isinstance check!)
def employees_summary(employees_list):
    sum_salary=0
    managers_name=[]
    for m in employees_list:
        sum_salary+=m.base_salary
        if isinstance(m,Manager):
            managers_name.append(m.name)
    return f"Total number of employees:{Employee.total_employees},{managers_name} {sum_salary}"
