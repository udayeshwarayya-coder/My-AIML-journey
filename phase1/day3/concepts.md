# 📘 Day 3 — List Operations, Sorting & String Methods (Deep Dive)

**Phase:** 1 (Python OOPs & Advanced Core)  
**Project:** Student Record System (Days 1–4)  
**Topic:** List comprehensions, `sorted()`, string methods, searching  
**Time:** ~30 minutes  

---

## 🔁 Quick Recap from Day 2

```python
# Class variable → shared across all instances
Student.total_students += 1

# @classmethod → takes cls, works with class-level data
@classmethod
def count_students(cls): return cls.total

# @staticmethod → no self/cls, pure utility
@staticmethod
def is_passing(avg): return avg >= 40

# lambda → one-line anonymous function
max(students, key=lambda s: s.get_avg())
```

> Today you build the **search & sort** layer of the Student Record System.

---

## 1. `sorted()` vs `.sort()` — Know the Difference

```python
nums = [3, 1, 4, 1, 5]

nums.sort()           # ❌ modifies original list IN PLACE, returns None
copy = sorted(nums)   # ✅ returns NEW sorted list, original unchanged
```

**With objects — use `key=`:**

```python
# Sort students by average (ascending)
sorted_students = sorted(students, key=lambda s: s.get_avg())

# Sort descending (highest first)
sorted_students = sorted(students, key=lambda s: s.get_avg(), reverse=True)

# Sort by name alphabetically
sorted_students = sorted(students, key=lambda s: s.name)
```

> ⚠️ `sorted()` is almost always preferred over `.sort()` because it doesn't destroy the original list.

---

## 2. List Comprehensions — Python's Power Tool

A cleaner, faster way to build lists from existing ones.

```python
# Normal loop
passing = []
for s in students:
    if s.get_avg() >= 40:
        passing.append(s)

# Same thing as a list comprehension
passing = [s for s in students if s.get_avg() >= 40]
```

**Pattern:**
```
[expression  for item in iterable  if condition]
     ↑              ↑                    ↑
  what to keep   loop variable      optional filter
```

**More examples:**
```python
# Get all names
names = [s.name for s in students]

# Get averages for section B only
b_avgs = [s.get_avg() for s in students if s.section == "B"]

# Get (name, avg) tuples
pairs = [(s.name, round(s.get_avg(), 2)) for s in students]
```

---

## 3. String Methods You'll Use Today

```python
name = "  uday hanumanthu  "

name.strip()        # "uday hanumanthu"     → removes leading/trailing spaces
name.lower()        # "  uday hanumanthu  " → all lowercase
name.upper()        # "  UDAY HANUMANTHU  "
name.title()        # "  Uday Hanumanthu  " → Title Case

# Checking content
"uday".startswith("u")          # True
"uday".endswith("y")            # True
"uday" in "uday hanumanthu"     # True
```

**For case-insensitive search (very common):**
```python
# Search for "sneha" even if stored as "Sneha" or "SNEHA"
query = "sneha"
match = query.lower() == student.name.lower()
```

---

## 4. Comparing Objects — Manual vs Operators

You can compare students manually using their average:

```python
def compare_students(s1, s2):
    avg1 = s1.get_avg()
    avg2 = s2.get_avg()
    if avg1 > avg2:
        return f"{s1.name} is better"
    elif avg2 > avg1:
        return f"{s2.name} is better"
    else:
        return "Both are equal"
```

Later (advanced OOP, Day 6+), you'll use `__lt__` to make Python's `<` / `>` operators work directly on objects.

---

## 5. Finding Items in a List

```python
# Find first match
def find_by_name(students, name):
    for s in students:
        if s.name.lower() == name.lower():
            return s
    return None   # always handle "not found"!
```

**Or with list comprehension (returns all matches):**
```python
matches = [s for s in students if name.lower() in s.name.lower()]
```

> ⚠️ Always return `None` (or raise an error) when something isn't found. Never silently return nothing.

---

## Quick Recap

```
sorted()             → returns new sorted list (use this!)
.sort()              → sorts in place, returns None
key=lambda s: ...    → tells sorted() what to sort by
reverse=True         → sorts descending
list comprehension   → [expr for x in list if cond]
.lower() / .strip()  → string normalization for search
None                 → return when item not found
```

---

## What You'll Build in practice.py

Three functions for the **Student Record System**:

1. `compare_students(s1, s2)` — compares two students by average, returns a result string
2. `find_by_name(students, name)` — searches by name (case-insensitive), returns Student or None
3. `sort_by_grade(students)` — returns a NEW sorted list, highest avg first

> These 3 + previous 6 functions = **9 of 12** logic pieces done!
