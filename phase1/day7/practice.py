# Day 7 Practice — Employee Payroll System (Part 3)
# Topic: Dunder Methods & Operator Overloading
# Goal: Make your Employee objects behave like built-in Python types

# ============================================================
# SETUP — Corrected classes from Day 6 (your base today)
# ============================================================

class Employee:
    company = "Tikota group of companies"
    total_employees = 0

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

    def get_details(self):
        return f"Name: {self.name} | ID: {self.emp_id} | Dept: {self.department} | Salary: Rs.{self.base_salary:,}"

    def __eq__(self, other):
        return self.emp_id==other.emp_id
    def __lt__(self, other):
        return self.calculate_pay < other.calculate_pay
    def __gt__(self, other):
        return self.calculate_pay > other.calculate_pay
    def __add__(self, other):
        return self.calculate_pay + other.calculate_pay
    def __len__(self):
        return self.calculate_pay//10000
    def __bool__(self):
        return self.base_salary > 0
    def __ne__(self, value):
        return self.emp_id != value.emp_id
    @property
    def calculate_pay(self):
        return self.base_salary


class Manager(Employee):
    def __init__(self, name, emp_id, base_salary, department="General", team_size=0):
        super().__init__(name, emp_id, base_salary, department)
        self.team_size = team_size

    def get_team_info(self):
        return f"{self.name} manages a team of {self.team_size} people."

    @property
    def total_pay(self):
        return self.base_salary + self.team_size * 5000

    @property
    def calculate_pay(self):
        return self.base_salary + self.team_size * 5000


class Intern(Employee):
    def __init__(self, name, emp_id, base_salary, department, stipend=0.0, college="xyz"):
        super().__init__(name, emp_id, base_salary, department)
        self.stipend = stipend
        self.college = college

    def get_intern_info(self):
        return f"{self.name} from {self.college} interning in {self.department}"

    @property
    def calculate_pay(self):
        return self.stipend


# ============================================================
# TASK 1: Add __eq__ to Employee
# ============================================================
# Two employees are EQUAL if they have the same emp_id.
# Add __eq__(self, other) to the Employee class above.
#
# Rule: return True if self.emp_id == other.emp_id
#
# Example:
#   e1 = Employee("Uday", "E001", 50000, "Engineering")
#   e2 = Employee("Uday", "E001", 60000, "Marketing")   # same ID!
#   e1 == e2   ->  True   (same person even if salary differs)
#   e1 == m1   ->  False  (different IDs)
#
# HINT: Add it directly inside the Employee class above.
# Write "pass" below as a placeholder reminder:

# def __eq__(self, other):
#     ...


# ============================================================
# TASK 2: Add __lt__ and __gt__ to Employee
# ============================================================
# Compare employees by their calculate_pay.
# Add both methods to the Employee class above.
#
# Rule:
#   __lt__: return True if self.calculate_pay < other.calculate_pay
#   __gt__: return True if self.calculate_pay > other.calculate_pay
#
# Example:
#   e1 = Employee("Uday", "E001", 50000, "Engineering")  # pay = 50000
#   m1 = Manager("Arjun", "M001", 80000, "Engineering", team_size=8) # pay = 120000
#   e1 < m1   ->  True
#   m1 > e1   ->  True
#
# HINT: remember calculate_pay is a @property — no parentheses!


# ============================================================
# TASK 3: Add __add__ to Employee
# ============================================================
# e1 + e2 should return the COMBINED pay of both employees (a number).
# Add __add__(self, other) to the Employee class above.
#
# Rule: return self.calculate_pay + other.calculate_pay
#
# Example:
#   e1 + i1   ->  65000   (50000 + 15000)
#   e1 + m1   ->  170000  (50000 + 120000)


# ============================================================
# TASK 4: Add __len__ to Employee
# ============================================================
# len(emp) should return salary expressed in units of 10,000.
# Add __len__(self) to the Employee class above.
#
# Rule: return self.base_salary // 10000
#
# Example:
#   len(e1)  ->  5    (50000 // 10000)
#   len(m1)  ->  8    (80000 // 10000  — uses base_salary, not bonus)


# ============================================================
# TASK 5: Add __bool__ to Employee
# ============================================================
# bool(emp) should return True only if the employee's calculate_pay > 0.
# Add __bool__(self) to the Employee class above.
#
# Rule: return self.calculate_pay > 0
#
# Example:
#   bool(e1)   ->  True   (paid 50000)
#   unpaid = Intern("Ghost", "I999", 0, "HR", stipend=0)
#   bool(unpaid)  ->  False


# ============================================================
# TEST YOUR CODE
# ============================================================

print("=" * 55)
print("TEST 1 — __eq__")
print("=" * 55)

e1 = Employee("Uday", "E001", 50000, "Engineering")
e2 = Employee("Uday", "E001", 60000, "Marketing")   # same ID, different salary
m1 = Manager("Arjun", "M001", 80000, "Engineering", team_size=8)
i1 = Intern("Ravi", "I001", 0, "Marketing", stipend=15000, college="IIT")

print(e1 == e2)   # Expected: True  (same emp_id)
print(e1 == m1)   # Expected: False (different emp_id)


print()
print("=" * 55)
print("TEST 2 — __lt__ and __gt__")
print("=" * 55)

print(e1 < m1)    # Expected: True  (50000 < 120000)
print(m1 > e1)    # Expected: True
print(i1 < e1)    # Expected: True  (15000 < 50000)


print()
print("=" * 55)
print("TEST 3 — __add__")
print("=" * 55)

print(e1 + i1)    # Expected: 65000  (50000 + 15000)
print(e1 + m1)    # Expected: 170000 (50000 + 120000)
print(m1 + i1)    # Expected: 135000 (120000 + 15000)


print()
print("=" * 55)
print("TEST 4 — __len__")
print("=" * 55)

print(len(e1))    # Expected: 5  (50000 // 10000)
print(len(m1))    # Expected: 8  (80000 // 10000)


print()
print("=" * 55)
print("TEST 5 — __bool__")
print("=" * 55)

unpaid = Intern("Ghost", "I999", 0, "HR", stipend=0)
print(bool(e1))       # Expected: True
print(bool(unpaid))   # Expected: False

if e1:
    print(f"{e1.name} is an active employee")   # should print
if not unpaid:
    print(f"{unpaid.name} is unpaid!")           # should print


print()
print("=" * 55)
print("TEST 6 — sorted() and max() using your dunders")
print("=" * 55)

team = [m1, e1, i1]
sorted_team = sorted(team)              # uses __lt__ automatically
print([emp.name for emp in sorted_team])  # Expected: ['Ravi', 'Uday', 'Arjun']

highest = max(team)                     # uses __gt__ automatically
print(highest.name)                     # Expected: Arjun


# ============================================================
# BONUS CHALLENGE (optional — ~10 min)
# ============================================================
# 1. Add __ne__ to Employee:
#    e1 != e2  ->  True if emp_ids differ
#    (Hint: return not self.__eq__(other))
#
# 2. Add __contains__ to Manager:
#    "Uday" in m1  ->  True if "Uday" is in m1's team name list
#    (You'll need to add a team_members list to Manager)
#
# 3. Overload __str__ in Manager and Intern so they show
#    extra info beyond the base Employee __str__:
#    Manager → "Arjun [M001] — Engineering | Team: 8"
#    Intern  → "Ravi [I001] — Marketing | College: IIT"

# Write bonus code below:
# in manager
def __str__(self,value):
    return f"{self.name} {self.emp_id}, {self.calculate_pay}, {self.department},{self.team_size}"


#in intern
def __str__(self, value):
    return f"{self.name} {self.emp_id},{self.stipend},{self.college}"