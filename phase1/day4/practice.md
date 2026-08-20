# 📝 Day 4 Practice — Hints & Walkthrough

## Function 1: merge_sections(section_a, section_b)

**What it does:** Combines two section lists, removes duplicates by name, returns sorted by avg (highest first).

**Step-by-step:**
```
1. Combine:  merged = section_a + section_b
2. Deduplicate using a set() of names already seen
3. Sort the unique list: sorted(..., key=lambda s: s.get_avg(), reverse=True)
```

**Common mistake:** Using `.extend()` instead of `+` — that mutates section_a!

---

## Function 2: generate_report(students)

**What it does:** Returns a list of dicts sorted highest avg first.

**Step-by-step:**
```
1. Sort students by avg descending (sorted + reverse=True)
2. For each student, build a dict:
   {
       "name":    s.name,
       "avg":     round(s.get_avg(), 2),
       "grade":   get_grade(round(s.get_avg(), 2)),
       "status":  "Pass" if avg >= 40 else "Fail",
       "section": s.section
   }
3. Collect all dicts in a list and return it
```

**Tip:** Use a list comprehension for clean one-liner generation.

---

## Function 3: export_data(students)

**What it does:** Returns a multi-line string in CSV format.

**Step-by-step:**
```
1. Start with: lines = ["Name,Average,Grade,Status,Section"]
2. For each student, build a comma-separated line string
3. Return "\n".join(lines)
```

**Tip:** Sort the students highest avg first (same as generate_report).

---

## Self-Check: Expected Outputs

```
=== Merged (no duplicates, sorted) ===
Sneha [91.7]
Uday [84.3]
Ravi [71.7]
Priya [50.0]

=== Report ===
{"name": "Sneha", "avg": 91.67, "grade": "A", "status": "Pass", "section": "A"}
{"name": "Uday",  "avg": 84.33, "grade": "B", "status": "Pass", "section": "A"}
{"name": "Ravi",  "avg": 71.67, "grade": "C", "status": "Pass", "section": "A"}
{"name": "Priya", "avg": 50.0,  "grade": "D", "status": "Pass", "section": "B"}

=== CSV Export ===
Name,Average,Grade,Status,Section
Sneha,91.67,A,Pass,A
Uday,84.33,B,Pass,A
Ravi,71.67,C,Pass,A
Priya,50.0,D,Pass,B
```

---

> Once your output matches — you are done with the Student Record System logic!
> The website will be built for you using all 12 functions.
