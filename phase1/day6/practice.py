# Day 6 Practice — Employee Payroll System (Part 2)
# Topic: Method Overriding, Polymorphism, @property
# Goal: Teach each class to calculate pay differently

# ============================================================
# SETUP — Copy your corrected Day 5 classes here as a base
# ============================================================
# The Employee, Manager, and Intern classes below are the
# CORRECTED versions from Day 5. Study the fixes if any.
# Today you will ADD to these classes.

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

    # FIX from Day 5 — correct get_details
    def get_details(self):
        return f"Name: {self.name} | ID: {self.emp_id} | Dept: {self.department} | Salary: Rs.{self.base_salary:,}"
    @property
    def calculate_pay(self):
        return self.base_salary

# ============================================================
# TASK 1: Add calculate_pay to Employee
# ============================================================
# Add a method calculate_pay(self) to the Employee class above.
# Rule: Employee pay = base_salary (just return it as-is)
#
# Example:
#   e = Employee("Uday", "E001", 50000)
#   e.calculate_pay  ->  50000
#
# HINT: Add the method directly inside the Employee class above.
# Write "pass" here as a reminder and add it above:
#
# def calculate_pay(self):
#     ...


# ============================================================
# TASK 2: Manager class — override calculate_pay + @property
# ============================================================
# Write the Manager class that:
#   1. Inherits from Employee
#   2. Has team_size attribute (via __init__ + super())
#   3. Overrides calculate_pay:
#      Manager pay = base_salary + (team_size * 5000)
#   4. Has a @property called total_pay that returns calculate_pay
#   5. Still has get_team_info() from Day 5
#
# Example:
#   m = Manager("Arjun", "M001", 80000, "Engineering", team_size=8)
#   m.calculate_pay   ->  120000   (80000 + 8*5000)
#   m.total_pay         ->  120000   (same, via @property — no parens!)
#   m.team_size = 12
#   m.total_pay         ->  140000   (auto-recalculated!)

# Write your Manager class here:
class Manager(Employee):
   # replace this with your full implementation
    def __init__(self, name, emp_id, base_salary, department="General",team_size=0):
            super().__init__(name, emp_id, base_salary, department)
            self.team_size = team_size
    def get_team_info(self):
        return f"{self.name} manages a team of {self.team_size} people."
    @property
    def total_pay(self):
        return self.base_salary + self.team_size * 5000
    @property
    def calculate_pay(self):
        total=self.base_salary+self.team_size*5000
        return total

# ============================================================
# TASK 3: Intern class — override calculate_pay
# ============================================================
# Write the Intern class that:
#   1. Inherits from Employee
#   2. Has stipend (float) and college (str) attributes
#   3. Overrides calculate_pay:
#      Intern pay = stipend (NOT base_salary)
#   4. Still has get_intern_info() from Day 5
#
# Example:
#   i = Intern("Ravi", "I001", 0, "Marketing", stipend=15000, college="IIT")
#   i.calculate_pay   ->  15000

# Write your Intern class here:
class Intern(Employee):
       # replace this with your full implementation
    def __init__(self,name,emp_id,base_salary,department,stipend=0.0,college="xyz"):
        super().__init__(name,emp_id,base_salary,department)
        self.stipend = stipend
        self.college = college
    def get_intern_info(self):
        return f"{self.name} from {self.college} interning from {self.department}"    
    @property
    def calculate_pay(self):
        return self.stipend

# ============================================================
# TASK 4: run_payroll(employees)
# ============================================================
# Takes a LIST of Employee/Manager/Intern objects (mixed).
# Loops through and prints a payslip for each:
#   "Payslip -> Uday [E001]: Rs.50,000"
#
# Polymorphism in action: same function, each emp calls its
# own calculate_pay version automatically.
#
# Example:
#   run_payroll([e, m, i])
#   Payslip -> Uday [E001]: Rs.50,000
#   Payslip -> Arjun [M001]: Rs.1,20,000
#   Payslip -> Ravi [I001]: Rs.15,000

# Write your function here:

      # replace with your implementation
def run_payroll(employee):
    for emp in employee:
        print(f"payout is {emp.calculate_pay} for {emp.name}")

# ============================================================
# TASK 5: get_highest_paid(employees)
# ============================================================
# Takes a LIST of employee objects.
# Returns the employee OBJECT with the highest calculate_pay.
# (Not just the number — return the whole object!)
#
# Example:
#   winner = get_highest_paid([e, m, i])
#   print(winner.name)   ->  "Arjun"  (Manager earns most)
#
# Hint: use max() with a key= argument, OR a manual loop.

# Write your function here:
def get_highest_paid(employees):
       # replace with your implementation
    highest_paid=employees[0]
    for emp in employees:
        if highest_paid.calculate_pay < emp.calculate_pay:
            highest_paid=emp
    return highest_paid
# ============================================================
# TEST YOUR CODE
# ============================================================

print("=" * 55)
print("TEST 1 — calculate_pay per class")
print("=" * 55)

e1 = Employee("Uday", "E001", 50000, "Engineering")
m1 = Manager("Arjun", "M001", 80000, "Engineering", team_size=8)
i1 = Intern("Ravi", "I001", 0, "Marketing", stipend=15000, college="IIT")

print(e1.calculate_pay)    # Expected: 50000
print(m1.calculate_pay)    # Expected: 120000
print(i1.calculate_pay)    # Expected: 15000


print()
print("=" * 55)
print("TEST 2 — @property total_pay on Manager")
print("=" * 55)

print(m1.total_pay)          # Expected: 120000  (no parentheses!)
m1.team_size = 12
print(m1.total_pay)          # Expected: 140000  (auto-recalculated)


print()
print("=" * 55)
print("TEST 3 — run_payroll() (polymorphism)")
print("=" * 55)

run_payroll([e1, m1, i1])
# Expected:
# Payslip -> Uday [E001]: Rs.50,000
# Payslip -> Arjun [M001]: Rs.1,40,000   (team_size is now 12)
# Payslip -> Ravi [I001]: Rs.15,000


print()
print("=" * 55)
print("TEST 4 — get_highest_paid()")
print("=" * 55)

winner = get_highest_paid([e1, m1, i1])
print(winner.name)           # Expected: Arjun
print(winner.calculate_pay)# Expected: 140000


print()
print("=" * 55)
print("TEST 5 — isinstance still works correctly")
print("=" * 55)

print(isinstance(m1, Manager))    # True
print(isinstance(m1, Employee))   # True  <- Manager IS also an Employee
print(isinstance(i1, Intern))     # True
print(isinstance(i1, Manager))    # False


# ============================================================
# BONUS CHALLENGE (optional — ~10 min)
# ============================================================
# 1. Add a @property annual_pay to ALL three classes that
#    returns calculate_pay * 12
#    Usage: e1.annual_pay  ->  600000
#
# 2. Write a function department_payroll(employees, dept) that:
#    - Takes a list of employees and a department name (str)
#    - Returns the TOTAL payroll only for employees in that dept
#    Example:
#      department_payroll([e1, m1, i1], "Engineering")  ->  190000
#
# 3. Bonus brain teaser:
#    What happens if you call e1.total_pay?
#    (Employee has no total_pay property — what error do you get?)
#    Try it and note the error message.

# Write bonus code below:
