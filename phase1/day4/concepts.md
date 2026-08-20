# 📘 Day 4 — Build Day: Student Record System Complete

**Phase:** 1 (Python OOPs & Advanced Core)  
**Project:** Student Record System (Days 1–4) ← **FINAL DAY**  
**Topic:** Merging data, report generation, data export — then the website goes live!  
**Time:** ~30 minutes  

---

## 🔁 Quick Recap from Day 3

```python
sorted(students, key=lambda s: s.get_avg(), reverse=True)  # sorted descending
[s for s in students if s.get_avg() >= 40]                 # list comprehension
s.name.lower() == query.lower()                            # case-insensitive search
return None   # always return None when not found
```

> Today you write the **last 3 logic functions** — then your code becomes a live website!

---

## 1. Merging Two Groups — merge_sections()

You have students from Section A and Section B stored separately. Merging them is simple:

```python
section_a = [s1, s2]
section_b = [s3, s4]

# Option 1: + operator (creates new list)
merged = section_a + section_b

# Option 2: extend (modifies in place — avoid this)
section_a.extend(section_b)   # changes original
```

Always use `+` when you want a new combined list without touching the originals.

**Deduplication — removing duplicates:**
```python
# If a student might be in both lists, filter by name
seen = set()
unique = []
for s in merged:
    if s.name not in seen:
        seen.add(s.name)
        unique.append(s)
```

---

## 2. Report Generation — Returning Structured Data

A "report" is just a list of dictionaries — each dict represents one row of data.

```python
# Bad: return a raw string (hard to display/format)
return "Uday: 84.33 — Pass"

# Good: return structured data (flexible)
return [
    {"name": "Uday", "avg": 84.33, "grade": "B", "status": "Pass"},
    {"name": "Ravi", "avg": 71.67, "grade": "C", "status": "Pass"},
]
```

**Grade logic (you will use this today):**
```python
def get_grade(avg):
    if avg >= 90: return "A"
    elif avg >= 75: return "B"
    elif avg >= 60: return "C"
    elif avg >= 40: return "D"
    else:          return "F"
```

**Status logic:**
```python
status = "Pass" if avg >= 40 else "Fail"
```

---

## 3. Exporting Data — Dicts to CSV String

The website needs to download data as a CSV file. You return a CSV-formatted string from Python.

```python
# A CSV file looks like this:
# Name,Average,Grade,Status
# Uday,84.33,B,Pass
# Ravi,71.67,C,Pass

def export_data(students):
    lines = ["Name,Average,Grade,Status"]   # header row
    for s in students:
        avg = round(s.get_avg(), 2)
        grade = get_grade(avg)
        status = "Pass" if avg >= 40 else "Fail"
        lines.append(f"{s.name},{avg},{grade},{status}")
    return "\n".join(lines)   # joins all lines with newline
```

`"\n".join(list)` is the clean way to build multi-line strings in Python.

---

## 4. __repr__ vs __str__ — Quick Note

You used `__repr__` in the Student class. Here is when to use which:

```python
class Student:
    def __repr__(self):
        # Used in: console/debugging, repr(obj), when printed in a list
        return f"Student({self.name}, avg={self.get_avg():.1f})"

    def __str__(self):
        # Used in: print(obj), str(obj), f-strings
        return f"{self.name} [{self.get_avg():.1f}]"
```

```python
s = Student("Uday", [85, 90, 78])
repr(s)   # "Student(Uday, avg=84.3)"
str(s)    # "Uday [84.3]"
print(s)  # "Uday [84.3]"                <- uses __str__
[s]       # [Student(Uday, avg=84.3)]    <- uses __repr__
```

Rule of thumb: `__repr__` = for developers (unambiguous), `__str__` = for users (readable).

---

## Quick Recap

```
list_a + list_b        -> new merged list (non-destructive)
set()                  -> track seen items to deduplicate
return [dict, dict]    -> structured report data
"\n".join(lines)       -> build a CSV string
get_grade(avg)         -> A/B/C/D/F logic
__repr__               -> dev-facing, shown in console/lists
__str__                -> user-facing, used in print/f-strings
```

---

## What You Will Build in practice.py

Three final functions to **complete** the Student Record System:

1. `merge_sections(section_a, section_b)` — combines two student lists (no duplicates), sorted by avg descending
2. `generate_report(students)` — returns a list of dicts with name, avg, grade, status
3. `export_data(students)` — returns a CSV-formatted string ready to download

After practice.py, the website goes live — you will see all your logic working in a real UI!
