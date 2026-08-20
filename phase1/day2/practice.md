# 📝 Day 2 Practice Guide — Student Record System (Part 2)

**Phase:** 1 | **Day:** 2 of 4 (Project 1)  
**Concepts:** Class variables, `@classmethod`, `@staticmethod`, `lambda`

---

## Your 3 Functions Today

These build on the `Student` class in `practice.py`.

---

### Function 1: `count_students()`

**What it does:** Tracks and returns total students created.

**Approach:**
- Add `total_students = 0` as a class variable
- Increment it inside `__init__` using `Student.total_students += 1`
- Expose it as a `@classmethod`

```python
@classmethod
def count_students(cls):
    return cls.total_students
```

**Test:**
```python
s1 = Student("Uday", [85, 90, 78])
s2 = Student("Ravi", [70, 65, 80])
print(Student.count_students())  # 2
```

---

### Function 2: `get_topper(students)`

**What it does:** Finds the student with the highest average.

**Approach:**
- Use Python's built-in `max()` with a `key` argument
- The `key` should compute the average marks for each student

```python
def get_topper(students):
    return max(students, key=lambda s: sum(s.marks) / len(s.marks))
```

**Test:**
```python
students = [s1, s2, s3]
print(get_topper(students).name)  # whoever has highest avg
```

---

### Function 3: `calculate_avg(student)`

**What it does:** Returns avg + grade as a dictionary.

**Approach:**
- Calculate average using `sum()` and `len()`
- Use `round()` to 2 decimal places
- Apply grade logic with `if/elif/else`
- Return a `dict`

```python
def calculate_avg(student):
    avg = round(sum(student.marks) / len(student.marks), 2)
    if avg >= 85:
        grade = "A"
    elif avg >= 70:
        grade = "B"
    elif avg >= 55:
        grade = "C"
    else:
        grade = "F"
    return {"name": student.name, "avg": avg, "grade": grade}
```

---

## Expected Outputs

```
Student.count_students()  →  4
get_topper(students).name →  "Sneha"
calculate_avg(s1)         →  {"name": "Uday", "avg": 84.33, "grade": "B"}
calculate_avg(s4)         →  {"name": "Priya", "avg": 50.0, "grade": "F"}
```

---

## Project Progress Tracker

| Day | Functions | Status |
|-----|-----------|--------|
| 1 | `create_student()`, `display_info()`, `update_grade()` | ✅ Done |
| 2 | `count_students()`, `get_topper()`, `calculate_avg()` | ⬜ Today |
| 3 | `compare_students()`, `find_by_name()`, `sort_by_grade()` | ⬜ Upcoming |
| 4 | `merge_sections()`, `generate_report()`, `export_data()` + Website | ⬜ Upcoming |

---

## Concepts Introduced Today

| Concept | First Seen | Status |
|---------|-----------|--------|
| Classes & Objects | Day 1 | ✅ |
| `__init__`, `self` | Day 1 | ✅ |
| Instance variables | Day 1 | ✅ |
| Class variables | Day 2 | 🆕 |
| `@classmethod` | Day 2 | 🆕 |
| `@staticmethod` | Day 2 | 🆕 |
| `lambda` (intro) | Day 2 | 🆕 |
| Default parameters | Day 1 | ✅ |
