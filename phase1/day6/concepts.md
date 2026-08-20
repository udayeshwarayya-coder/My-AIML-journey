# Day 6 — Method Overriding, Polymorphism & `@property`
## Project 2: Employee Payroll System (continued)

> **Builds on Day 5:** Inheritance, `super()`, `isinstance()`

---

## Quick Recap — What You Built Yesterday

```
Employee (base)
├── name, emp_id, base_salary, department
├── get_details() → formatted string

Manager (child of Employee)
├── team_size
└── get_team_info() → "X manages a team of N people."

Intern (child of Employee)
├── stipend, college
└── get_intern_info() → "X from Y interning in Z."
```

Today you will teach each class to **calculate pay differently** — without changing the function that calls them.

---

## Concept 1: Method Overriding

When a child class defines a method with the **same name** as the parent, the child's version **wins**.

```python
class Employee:
    def calculate_pay(self):
        return self.base_salary          # just the base

class Manager(Employee):
    def calculate_pay(self):             # same name = override
        bonus = self.team_size * 5000
        return self.base_salary + bonus

class Intern(Employee):
    def calculate_pay(self):             # override again
        return self.stipend              # paid via stipend only
```

**Which version runs?** Python always looks at the actual object type:

```python
e = Employee("Uday", "E001", 50000)
m = Manager("Arjun", "M001", 80000, "Eng", team_size=8)
i = Intern("Ravi", "I001", 0, "Marketing", stipend=15000, college="IIT")

e.calculate_pay()   # 50000   (Employee's version)
m.calculate_pay()   # 120000  (Manager's: 80000 + 8x5000)
i.calculate_pay()   # 15000   (Intern's version)
```

---

## Concept 2: Polymorphism — One Function, Many Types

Write **one function** that works on any employee type:

```python
def print_payslip(emp):
    print(f"{emp.name}: Rs.{emp.calculate_pay():,}")
```

Call it with ANY employee type:

```python
print_payslip(e)    # Uday: Rs.50,000
print_payslip(m)    # Arjun: Rs.1,20,000
print_payslip(i)    # Ravi: Rs.15,000
```

Python automatically calls the **right version** of `calculate_pay()`.
This is **polymorphism** — same function name, different behavior per class.

**Classic pattern — process a mixed list:**

```python
employees = [e, m, i]

for emp in employees:
    print_payslip(emp)    # each calls its own calculate_pay()
```

---

## Concept 3: @property — Smart Attributes

A computed "attribute" that recalculates whenever you access it.

**Without @property (the bad way):**
```python
m.total_pay = m.base_salary + m.team_size * 5000
# Problem: stale if team_size changes later!
```

**With @property (the right way):**
```python
class Manager(Employee):
    @property
    def total_pay(self):
        return self.base_salary + self.team_size * 5000

m = Manager("Arjun", "M001", 80000, "Eng", team_size=8)
print(m.total_pay)        # 120000  (no parentheses!)
m.team_size = 12
print(m.total_pay)        # 140000  (auto-recalculated!)
```

**Key rules:**
- Accessed with `obj.property_name` — NO parentheses — looks like attribute
- Always returns fresh computed value — never stale
- Cannot be assigned directly (raises AttributeError by default)

---

## Visual: Method Resolution Order (MRO)

When you call `m.calculate_pay()`, Python searches:
```
1. Manager class  -> found! Use Manager's calculate_pay()
2. Employee class -> (would check here if not found in Manager)
3. object class   -> (Python's ultimate base class)
```

Check it yourself:
```python
print(Manager.__mro__)
# (<class 'Manager'>, <class 'Employee'>, <class 'object'>)
```

---

## What You Are Building Today

**Day 6 additions to the Payroll System:**

| Task | Description |
|------|-------------|
| Override `calculate_pay()` | Each class calculates pay differently |
| `run_payroll(employees)` | Loops over a mixed list, prints payslips |
| `@property total_pay` in Manager | Computed from base + team bonus |
| `get_highest_paid(employees)` | Returns employee object with highest pay |

**Pay rules:**
- Employee: pay = base_salary
- Manager:  pay = base_salary + (team_size x 5000)
- Intern:   pay = stipend (not base_salary)

---

## Common Mistakes Today

| Mistake | Fix |
|---------|-----|
| Calling `obj.total_pay()` with `()` | It's a @property — use `obj.total_pay` (no parens) |
| Forgetting to override in each child | If not overridden, Python uses parent's version |
| Storing computed values as regular attributes | Use @property for values that depend on other attributes |

---

## 10-Minute Read Check

You now understand:
- [ ] What method overriding is and how it works
- [ ] How polymorphism lets one function handle multiple types
- [ ] What @property does and when to use it
- [ ] Python's Method Resolution Order (child -> parent -> object)
- [ ] The pay rules for Employee, Manager, and Intern

**Now open practice.py and build Day 6!**
