# Day 5 — Single Inheritance & `super()`
## Project 2: Employee Payroll System

> **Revisits from Day 1-4:** Classes, `__init__`, `self`, instance vars, class vars, `__str__`, `__repr__`

---

## What You Already Know (Quick Recap)

```python
class Student:
    def __init__(self, name, marks):
        self.name = name      # instance variable
        self.marks = marks

    def get_avg(self):
        return sum(self.marks) / len(self.marks)
```

A class bundles **data** (attributes) and **behavior** (methods) together.  
Today: what if you need a *specialized version* of a class?

---

## The Problem Inheritance Solves

Imagine you have:
- `Employee` → has `name`, `emp_id`, `base_salary`
- `Manager` → has everything an Employee has, PLUS `team_size`, `bonus`
- `Intern` → has everything an Employee has, BUT paid differently

**Without inheritance:**  
You'd copy-paste all Employee code into Manager and Intern. If you fix a bug in Employee, you fix it in 3 places. Nightmare.

**With inheritance:**  
Manager and Intern *inherit* everything from Employee automatically.

---

## Single Inheritance — The Basics

```python
class Employee:                      # Parent class (also called Base class)
    def __init__(self, name, emp_id, base_salary):
        self.name = name
        self.emp_id = emp_id
        self.base_salary = base_salary

    def get_details(self):
        return f"{self.name} (ID: {self.emp_id})"


class Manager(Employee):             # Child class inherits from Employee
    pass                             # 'pass' = "nothing extra yet"


# Manager already has EVERYTHING from Employee!
m = Manager("Arjun", "M001", 80000)
print(m.get_details())              # Works! → "Arjun (ID: M001)"
print(m.name)                       # Works! → "Arjun"
```

Just write `class Child(Parent):` — the child gets all parent methods and attributes.

---

## `super()` — Calling the Parent's `__init__`

When Manager needs its OWN extra attributes too:

```python
class Manager(Employee):
    def __init__(self, name, emp_id, base_salary, team_size):
        super().__init__(name, emp_id, base_salary)   # ← calls Employee's __init__
        self.team_size = team_size                    # ← Manager's own extra attribute

m = Manager("Arjun", "M001", 80000, 10)
print(m.name)        # "Arjun"       ← from Employee
print(m.team_size)   # 10            ← Manager's own
```

**What `super().__init__(...)` does:**
- Runs the parent class's `__init__` first
- Sets up all the parent's attributes (`name`, `emp_id`, `base_salary`)
- Then you add the child's own extras after

**Without `super()`:**
```python
class Manager(Employee):
    def __init__(self, name, emp_id, base_salary, team_size):
        # If you forget super().__init__(), self.name won't exist!
        self.team_size = team_size
        # m.name → AttributeError ❌
```

---

## The `isinstance()` Check

```python
m = Manager("Arjun", "M001", 80000, 10)

isinstance(m, Manager)    # True  — m IS a Manager
isinstance(m, Employee)   # True  — m IS ALSO an Employee (child is always parent too)
isinstance(m, str)        # False
```

This is important: **a child object IS an instance of both child and parent classes.**

---

## Visual: The Inheritance Chain

```
Employee
├── name
├── emp_id
├── base_salary
└── get_details()
      │
      ▼
   Manager            (inherits EVERYTHING from Employee)
   ├── team_size      (adds its own)
   └── (more methods you'll add today)
```

---

## Real Pattern: Base Pay Calculation

```python
class Employee:
    def __init__(self, name, emp_id, base_salary):
        self.name = name
        self.emp_id = emp_id
        self.base_salary = base_salary

    def calculate_base_pay(self):
        return self.base_salary                   # straightforward for base class


class Manager(Employee):
    def __init__(self, name, emp_id, base_salary, team_size):
        super().__init__(name, emp_id, base_salary)
        self.team_size = team_size

    def calculate_base_pay(self):
        # Manager gets base + 10% for each team member managed
        return self.base_salary + (self.team_size * 0.10 * self.base_salary)
```

The child *overrides* `calculate_base_pay()`. When you call `m.calculate_base_pay()`, Python uses Manager's version, not Employee's.  
*(Full method overriding = Day 7's topic. Today, focus on `super()`.)*

---

## What You're Building Today

**Employee Payroll System — Day 5 Functions:**

| Function | What it does |
|----------|-------------|
| `Employee` base class | Blueprint with `name`, `emp_id`, `base_salary` |
| `calculate_base_pay(employee)` | Returns base salary of any employee |
| `get_details(employee)` | Returns formatted string with name, ID, salary |

Today you write **pure logic** — no Flask, no website yet. That comes on Day 8.

---

## Common Mistakes to Avoid

| Mistake | Fix |
|---------|-----|
| Forgetting `super().__init__()` in child | Always call it first before adding own attributes |
| Passing wrong args to `super().__init__()` | Match the parent's `__init__` parameter order |
| Calling `super()` with class name inside | Just use `super()` with no args (Python 3 style) |
| Thinking child replaces parent | Child *extends* parent — parent still works independently |

---

## 10-Minute Read Check ✅

You now understand:
- [ ] Why inheritance exists (avoid code duplication)
- [ ] How to write `class Child(Parent):`
- [ ] What `super().__init__()` does and why it's needed
- [ ] That `isinstance(child_obj, ParentClass)` is True
- [ ] The difference between child overriding vs inheriting a method

**Now open `practice.py` and write your 3 functions!**
