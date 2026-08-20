# 📝 Day 3 Practice Guide — Student Record System (Part 3)

**Phase:** 1 | **Day:** 3 of 4 (Project 1)  
**Concepts:** `sorted()`, list comprehensions, string search, object comparison

---

## Your 3 Functions Today

These build on the same `Student` class in `practice.py`.

---

### Function 1: `compare_students(s1, s2)`

**What it does:** Compares two students by average and returns a descriptive string.

**Approach:**
- Call `.get_avg()` on each student
- Compare the two averages
- Return a formatted string showing the winner (or tie)

```python
def compare_students(s1, s2):
    avg1 = round(s1.get_avg(), 2)
    avg2 = round(s2.get_avg(), 2)
    if avg1 > avg2:
        return f"{s1.name} ({avg1}) > {s2.name} ({avg2})"
    elif avg2 > avg1:
        return f"{s2.name} ({avg2}) > {s1.name} ({avg1})"
    else:
        return f"{s1.name} and {s2.name} are equal ({avg1})"
```

**Test:**
```python
print(compare_students(s1, s2))  # Uday (84.33) > Ravi (71.67)
print(compare_students(s1, s3))  # Sneha (91.67) > Uday (84.33)
```

---

### Function 2: `find_by_name(students, name)`

**What it does:** Searches the list for a student by name (case-insensitive).

**Approach:**
- Loop through students
- Compare `.lower()` versions to ignore case
- Return the Student object if found, `None` if not

```python
def find_by_name(students, name):
    for s in students:
        if s.name.lower() == name.strip().lower():
            return s
    return None
```

**Test:**
```python
result = find_by_name(students, "sneha")
print(result.name if result else "Not found")   # Sneha

result = find_by_name(students, "Unknown")
print(result.name if result else "Not found")   # Not found
```

---

### Function 3: `sort_by_grade(students)`

**What it does:** Returns a **new** sorted list of students, highest average first.

**Approach:**
- Use `sorted()` (not `.sort()`) — preserves original list
- Use `key=lambda s: s.get_avg()`
- Set `reverse=True` for descending order

```python
def sort_by_grade(students):
    return sorted(students, key=lambda s: s.get_avg(), reverse=True)
```

**Test:**
```python
ranked = sort_by_grade(students)
for i, s in enumerate(ranked, start=1):
    print(f"{i}. {s.name} — {s.get_avg():.2f}")

# Expected:
# 1. Sneha — 91.67
# 2. Uday  — 84.33
# 3. Ravi  — 71.67
# 4. Priya — 50.00
```

---

## Expected Outputs

```
compare_students(s1, s2)    →  "Uday (84.33) > Ravi (71.67)"
compare_students(s1, s3)    →  "Sneha (91.67) > Uday (84.33)"
find_by_name(students, "sneha")    →  Student object (name = Sneha)
find_by_name(students, "ghost")    →  None
sort_by_grade(students)[0].name    →  "Sneha"
sort_by_grade(students)[-1].name   →  "Priya"
```

---

## Project Progress Tracker

| Day | Functions | Status |
|-----|-----------|--------|
| 1 | `create_student()`, `display_info()`, `update_grade()` | ✅ Done |
| 2 | `count_students()`, `get_topper()`, `calculate_avg()` | ✅ Done |
| 3 | `compare_students()`, `find_by_name()`, `sort_by_grade()` | ⬜ Today |
| 4 | `merge_sections()`, `generate_report()`, `export_data()` + Website | ⬜ Upcoming |

---

## Concepts Introduced Today

| Concept | First Seen | Status |
|---------|-----------|--------|
| Classes & Objects | Day 1 | ✅ |
| `__init__`, `self` | Day 1 | ✅ |
| Instance variables | Day 1 | ✅ |
| Class variables | Day 2 | ✅ |
| `@classmethod` | Day 2 | ✅ |
| `@staticmethod` | Day 2 | ✅ |
| `lambda` | Day 2 | ✅ |
| `sorted()` + `key=` | Day 3 | 🆕 |
| List comprehensions | Day 3 | 🆕 |
| String methods (`.lower()`, `.strip()`) | Day 3 | 🆕 |
| Returning `None` for not-found | Day 3 | 🆕 |
