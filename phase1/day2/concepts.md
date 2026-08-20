# 📘 Day 2 — Instance Variables, Class Variables & Methods (Deep Dive)

**Phase:** 1 (Python OOPs & Advanced Core)  
**Project:** Student Record System (Days 1–4)  
**Topic:** Instance vars, Class vars, `@classmethod`, `@staticmethod`, and building real logic  
<br>**Time:** ~30 minutes  

---

## 🔁 Quick Recap from Day 1

```python
class Student:
    school = "ABC Academy"          # Class variable (shared)
    def __init__(self, name, marks):
        self.name = name             # Instance variable (unique)
        self.marks = marks
```

> Today you go **deeper** — you'll build the actual logic functions for the Student Record System project.

---

## 1. Class Variables — Shared Memory

Class variables are defined **directly inside the class** (not inside `__init__`).  
They are **shared** across ALL instances.

```python
class Student:
    school = "Tech Academy"
    total_students = 0              # tracks how many students exist

    def __init__(self, name, marks):
        self.name = name
        self.marks = marks
        Student.total_students += 1  # update class variable

s1 = Student("Uday", [85, 90, 78])
s2 = Student("Ravi", [70, 65, 80])

print(Student.total_students)   # 2  ← accessed via class name
print(s1.total_students)        # 2  ← also works via instance
```

> ⚠️ Always update class variables using `ClassName.var` (not `self.var`), or you'll accidentally create an instance variable with the same name instead of modifying the shared one.

---

## 2. Instance Methods vs Class Methods vs Static Methods

| Type | First Parameter | Access | Use When |
|------|----------------|--------|----------|
| Instance Method | `self` | instance + class data | most methods |
| Class Method | `cls` | class data only | factory methods, counters |
| Static Method | none | neither | utility/helper functions |

```python
class Student:
    school = "Tech Academy"
    total = 0

    def __init__(self, name, marks):
        self.name = name
        self.marks = marks
        Student.total += 1

    # Instance method — works with self (this specific student)
    def average(self):
        return sum(self.marks) / len(self.marks)

    # Class method — works with cls (the class itself)
    @classmethod
    def get_total(cls):
        return cls.total

    # Static method — no self or cls, just a utility
    @staticmethod
    def is_passing(avg):
        return avg >= 40

s1 = Student("Uday", [85, 90, 78])
print(s1.average())             # 84.33  (instance method)
print(Student.get_total())      # 1      (class method)
print(Student.is_passing(84))   # True   (static method)
```

---

## 3. The `lambda` Keyword (Quick Intro)

You'll use `lambda` a lot for sorting and finding max/min.  
It's just a **one-line anonymous function**:

```python
# Normal function
def get_avg(s):
    return sum(s.marks) / len(s.marks)

# Same thing as lambda
get_avg = lambda s: sum(s.marks) / len(s.marks)

# Used inline with max()
topper = max(students, key=lambda s: sum(s.marks) / len(s.marks))
```

---

## 4. Default Parameter Values

You already used this in Day 1 (`balance=0`). A quick reinforcement:

```python
def __init__(self, name, marks, section="A"):
    self.name = name
    self.marks = marks
    self.section = section          # defaults to "A" if not provided

s1 = Student("Uday", [85, 90])        # section = "A"
s2 = Student("Ravi", [70, 65], "B")   # section = "B"
```

---

## 🔴 Day 1 Bug to Fix Today

In your Day 1 Library code, `is_read` is stored as the **string** `'false'`  
but `unread_books()` checks with `not book.is_read`, which is always `False`  
(because any non-empty string is truthy in Python!).

**Fix:** Use a real boolean:
```python
# Bug (string-based)
self.is_read = 'false'
not book.is_read  # always False — 'false' is a non-empty string!

# Fix (boolean-based)
self.is_read = False
not book.is_read  # True when unread
```

> Keep this in mind: Python booleans are `True` / `False` (not strings).

---

## Quick Recap

```
Class variable     → Shared across all objects, defined outside __init__
Instance variable  → Unique to each object, defined in __init__ with self.
Instance method    → Takes self, most common
@classmethod       → Takes cls, used for class-wide operations
@staticmethod      → No self/cls, pure utility function
lambda             → One-line anonymous function, great for key= arguments
```

---

## What You'll Build in practice.py

Three functions for the **Student Record System**:

1. `count_students()` — returns total number of students created (use a class variable)
2. `get_topper(students)` — returns the student with the highest average marks
3. `calculate_avg(student)` — returns a student's average marks (rounded to 2 decimal places)

> These 3 functions + Day 1's 3 functions = 6 of the 12 logic pieces for the final website!
