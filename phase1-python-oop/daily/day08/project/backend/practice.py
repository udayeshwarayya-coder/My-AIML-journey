# Day 8 Practice — Employee Payroll System (Build Day)
# Topic: Putting it all together — 3 final logic functions
# These become API endpoints in your Flask backend

# ============================================================
# SETUP — Full class hierarchy from Days 5-7
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

    def __eq__(self, other):
        return self.emp_id == other.emp_id

    def __lt__(self, other):
        return self.calculate_pay < other.calculate_pay

    def __gt__(self, other):
        return self.calculate_pay > other.calculate_pay

    def __add__(self, other):
        return self.calculate_pay + other.calculate_pay

    def __len__(self):
        return self.base_salary // 10000

    def __bool__(self):
        return self.calculate_pay > 0

    @property
    def calculate_pay(self):
        return self.base_salary

    def get_details(self):
        return {
            "name": self.name,
            "emp_id": self.emp_id,
            "department": self.department,
            "type": type(self).__name__,
            "base_salary": self.base_salary,
            "total_pay": self.calculate_pay
        }


class Manager(Employee):
    def __init__(self, name, emp_id, base_salary, department="General", team_size=0):
        super().__init__(name, emp_id, base_salary, department)
        self.team_size = team_size

    def __str__(self):
        return f"{self.name} [{self.emp_id}] — {self.department} | Team: {self.team_size}"

    @property
    def calculate_pay(self):
        return self.base_salary + self.team_size * 5000

    def get_details(self):
        details = super().get_details()
        details["team_size"] = self.team_size
        details["team_bonus"] = self.team_size * 5000
        return details


class Intern(Employee):
    def __init__(self, name, emp_id, base_salary, department, stipend=0.0, college="xyz"):
        super().__init__(name, emp_id, base_salary, department)
        self.stipend = stipend
        self.college = college

    def __str__(self):
        return f"{self.name} [{self.emp_id}] — {self.department} | College: {self.college}"

    @property
    def calculate_pay(self):
        return self.stipend

    def get_details(self):
        details = super().get_details()
        details["college"] = self.college
        details["stipend"] = self.stipend
        return details


# ============================================================
# TASK 1: department_summary(employees) -> dict
# ============================================================
# Groups employees by department and returns stats.
#
# Input: a list of Employee / Manager / Intern objects
# Output: a dict like:
# {
#     "Engineering": {
#         "count": 2,
#         "total_payroll": 170000,
#         "avg_salary": 85000,
#         "members": ["Uday", "Arjun"]
#     },
#     ...
# }
#
# Steps:
#   1. Loop through employees
#   2. Group by emp.department
#   3. For each dept: count, sum of calculate_pay, member names
#   4. Calculate avg = total / count
#
# HINT: Use the dict grouping pattern from concepts.md

def department_summary(employees):
    # YOUR CODE HERE
    summary={}
    for emp in employees:
        dept=emp.department
        if dept not in summary:
            summary[dept]={"count":0,"total_payroll":0,"members":[]}
        summary[dept]["count"]+=1
        summary[dept]["total_payroll"]+=emp.calculate_pay
        
        summary[dept]["members"].append(emp.name)
        summary[dept]["avg_salary"]=summary[dept]["total_payroll"]/ summary[dept]["count"]
    return summary




# ============================================================
# TASK 2: highest_earner(employees) -> Employee object
# ============================================================
# Returns the employee with the highest calculate_pay.
#
# Input: list of employees
# Output: the Employee/Manager/Intern object with max pay
#
# Option A (simple): use max() with a key
#   return max(employees, key=lambda emp: emp.calculate_pay)
#
# Option B (manual loop): iterate and track the highest
#
# HINT: Since you have __gt__ from Day 7, sorted() and max()
#       already work on your objects without a key!

def highest_earner(employees):
    # YOUR CODE HERE
    return max(employees)


# ============================================================
# TASK 3: payroll_report(employees) -> dict
# ============================================================
# Generates a full company-wide payroll report.
#
# Output:
# {
#     "company": "Tikota group of companies",
#     "total_employees": 5,
#     "total_payroll": 450000,
#     "by_type": {
#         "Employee": {"count": 2, "total": 100000},
#         "Manager":  {"count": 2, "total": 280000},
#         "Intern":   {"count": 1, "total": 15000}
#     },
#     "highest_earner": {"name": "Arjun", "pay": 120000},
#     "pay_slips": [
#         {"name": "Uday", "emp_id": "E001", "type": "Employee", "pay": 50000},
#         ...
#     ]
# }
#
# HINT: use type(emp).__name__ to get "Manager", "Employee", "Intern"
# HINT: reuse highest_earner() you just wrote above

def payroll_report(employees):
    # YOUR CODE HERE
    payroll={}
    payroll["company"]=Employee.company
    payroll["total_employees"]=len(employees)
    s=0
    for emp in employees:
        s+=emp.calculate_pay
    payroll["total_payroll"]=s
    by_type={}
    for emp in employees:
        dept=type(emp).__name__
        if dept not in by_type:
            by_type[dept]={"count":0,"total":0}
        by_type[dept]["count"]+=1
        by_type[dept]["total"]+=emp.calculate_pay
    payroll["by_type"]=by_type
    high=highest_earner(employees)
    payroll["highest_earner"]={"name":high.name,"pay":high.calculate_pay}
    li=[]
    for emp in employees:
        d={}
        d["name"]=emp.name
# {"name": "Uday", "emp_id": "E001", "type": "Employee", "pay": 50000}
        d["emp_id"]=emp.emp_id
        d["type"]=type(emp).__name__
        d["pay"]=emp.calculate_pay
        li.append(d)
    payroll["pay_slips"]=li
    return payroll


# ============================================================
# TEST YOUR CODE
# ============================================================

print("=" * 60)
print("SETUP — Creating company roster")
print("=" * 60)

all_employees = [
    Employee("Uday", "E001", 50000, "Engineering"),
    Employee("Priya", "E002", 55000, "Marketing"),
    Manager("Arjun", "M001", 80000, "Engineering", team_size=8),
    Manager("Sunita", "M002", 75000, "Marketing", team_size=5),
    Intern("Ravi", "I001", 0, "Engineering", stipend=15000, college="IIT"),
    Intern("Meena", "I002", 0, "Marketing", stipend=12000, college="NIT"),
]

for emp in all_employees:
    print(emp)


print()
print("=" * 60)
print("TEST 1 — department_summary()")
print("=" * 60)

summary = department_summary(all_employees)
if summary:
    for dept, info in summary.items():
        print(f"\n{dept}:")
        print(f"  Count: {info['count']}")
        print(f"  Total Payroll: Rs.{info['total_payroll']:,}")
        print(f"  Avg Salary: Rs.{info['avg_salary']:,}")
        print(f"  Members: {info['members']}")
else:
    print("Not implemented yet")


print()
print("=" * 60)
print("TEST 2 — highest_earner()")
print("=" * 60)

top = highest_earner(all_employees)
if top:
    print(f"Top earner: {top.name}")
    print(f"Pay: Rs.{top.calculate_pay:,}")
    print(f"Type: {type(top).__name__}")
else:
    print("Not implemented yet")


print()
print("=" * 60)
print("TEST 3 — payroll_report()")
print("=" * 60)

report = payroll_report(all_employees)
if report:
    print(f"Company: {report['company']}")
    print(f"Total Employees: {report['total_employees']}")
    print(f"Total Payroll: Rs.{report['total_payroll']:,}")
    print(f"\nBy Type:")
    for emp_type, data in report['by_type'].items():
        print(f"  {emp_type}: {data['count']} employees, Rs.{data['total']:,}")
    print(f"\nHighest Earner: {report['highest_earner']['name']} — Rs.{report['highest_earner']['pay']:,}")
    print(f"\nPay Slips:")
    for slip in report['pay_slips']:
        print(f"  {slip['name']} ({slip['type']}): Rs.{slip['pay']:,}")
else:
    print("Not implemented yet")
