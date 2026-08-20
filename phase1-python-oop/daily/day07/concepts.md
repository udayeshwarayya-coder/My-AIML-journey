# Day 7 — Dunder Methods & Operator Overloading
## Project 2: Employee Payroll System (continued)

> **Builds on Day 6:** @property, Method Overriding, Polymorphism

---

## Quick Recap — What You Built So Far

```
Employee (base)
+-- calculate_pay  ?  base_salary         (@property)
+-- get_details()  ?  formatted string

Manager (child)
+-- team_size
+-- calculate_pay  ?  base_salary + team_size * 5000   (@property)
+-- total_pay      ?  same (another @property)
+-- get_team_info()

Intern (child)
+-- stipend, college
+-- calculate_pay  ?  stipend             (@property)
+-- get_intern_info()
```

Today you will make your classes **smarter** using Python special built-in hooks.

---

## Concept 1: What Are Dunder Methods?

"Dunder" = **D**ouble **Under**score (also called magic methods).

Python calls these automatically when you use built-in operations:

```python
e1 + e2      # calls  __add__
e1 == e2     # calls  __eq__
print(e1)    # calls  __str__
len(e1)      # calls  __len__
e1 > e2      # calls  __gt__
```

You already used `__init__`, `__str__`, `__repr__` — those are also dunders!

---

## Concept 2: `__str__` vs `__repr__`

| Method | When called | Purpose |
|--------|-------------|---------|
| `__str__` | `print(obj)`, `str(obj)` | Human-friendly display |
| `__repr__` | `repr(obj)`, in the REPL | Developer/debug display |

```python
class Employee:
    def __str__(self):
        return f"{self.name} [{self.emp_id}]"

    def __repr__(self):
        return f"Employee({self.name!r}, {self.base_salary})"
```

---

## Concept 3: Comparison Dunders

Make your objects comparable with ==, <, >:

```python
class Employee:
    def __eq__(self, other):
        return self.emp_id == other.emp_id

    def __lt__(self, other):
        return self.calculate_pay < other.calculate_pay

    def __gt__(self, other):
        return self.calculate_pay > other.calculate_pay
```

Once __lt__ and __eq__ are defined, you can use sorted() and max()!

```python
employees = [e1, m1, i1]
print(sorted(employees))   # sorted by pay low to high
print(max(employees))      # highest paid automatically
```

---

## Concept 4: `__add__` — Operator Overloading

```python
class Employee:
    def __add__(self, other):
        return self.calculate_pay + other.calculate_pay
```

```python
e1 + m1    # 50000 + 120000 = 170000  (total payroll of two)
```

---

## Concept 5: `__len__` and `__bool__`

```python
class Employee:
    def __len__(self):
        return self.base_salary // 10000   # salary in units of 10K

    def __bool__(self):
        return self.calculate_pay > 0      # False if unpaid
```

```python
len(e1)    # 5  (50000 // 10000)
bool(i1)   # False if stipend == 0
```

---

## Dunder Cheat Sheet

```
Operator / Use        Dunder method
-------------------------------------
print(obj)         ?  __str__
repr(obj)          ?  __repr__
obj1 == obj2       ?  __eq__
obj1 != obj2       ?  __ne__
obj1 < obj2        ?  __lt__
obj1 > obj2        ?  __gt__
obj1 + obj2        ?  __add__
len(obj)           ?  __len__
bool(obj)          ?  __bool__
```

---

## What You Are Building Today

| Task | Dunder | Description |
|------|--------|-------------|
| 1 | `__eq__` | Two employees are equal if same emp_id |
| 2 | `__lt__` and `__gt__` | Compare by calculate_pay |
| 3 | `__add__` | e1 + e2 returns combined pay |
| 4 | `__len__` | len(emp) = salary in units of 10K |
| 5 | `__bool__` | bool(emp) = False if pay is 0 |
| BONUS | sorted() and max() | Use your dunders on a mixed list |

---

## Common Mistakes Today

| Mistake | Fix |
|---------|-----|
| Forgetting `other` parameter | Always `def __eq__(self, other):` |
| Using () on a @property inside dunder | `self.calculate_pay` not `self.calculate_pay()` |
| __add__ modifying objects | Should RETURN a value, not change state |

---

## 10-Minute Read Check

You now understand:
- [ ] What dunder methods are and when Python calls them
- [ ] Difference between __str__ and __repr__
- [ ] How to make objects comparable with __eq__, __lt__, __gt__
- [ ] How __add__ overloads the + operator
- [ ] How sorted() and max() use dunders automatically

**Now open practice.py and build Day 7!**
