# Day 27 — OOP + File I/O: Merge, Group, Birthday & Export
## Project 7: Contact Book (Part 3: Advanced Operations)

> **Revisits from Days 1–26:** `class`, `dict`, `set`, `datetime`, `csv`, `sorted()`, `list comprehension`

---

## What You Are Building Today

1. **`merge_contacts(base_book, other_book)`** — Adds contacts from `other_book` into `base_book`, skipping duplicates by `contact_id`.
2. **`group_by_city(book)`** — Returns a `dict` mapping city → list of contacts.
3. **`birthday_reminder(book, days_ahead=7)`** — Returns contacts whose birthday falls within the next N days.
4. **`export_to_csv(book, filepath)`** — Writes contacts to a CSV file with a header row.
5. **`find_duplicates(book)`** — Returns a list of contacts that share a phone number with another contact.

---

## Concept 1: Merging Two Collections

Real apps need to merge data from multiple sources without creating duplicates.
The trick: build a **set of existing IDs** first, then only add contacts whose ID is not in that set.

```python
def merge_contacts(base_book, other_book) -> int:
    existing_ids = {c.contact_id for c in base_book.contacts}
    added = 0
    for c in other_book.contacts:
        if c.contact_id not in existing_ids:
            base_book.contacts.append(c)
            existing_ids.add(c.contact_id)
            added += 1
    return added
```

> **Why add to `existing_ids` inside the loop?** If `other_book` itself has a duplicate ID, we catch it too.

---

## Concept 2: Grouping with a Dictionary

`group_by_city` should return:
```python
{
  "New York": [<Tony>, <Natasha>],
  "Queens":   [<Peter>],
}
```

Pattern: loop, use the group key as the dict key, append to the list.

```python
def group_by_city(book) -> dict:
    groups = {}
    for c in book.contacts:
        key = c.city.strip() or "Unknown"
        if key not in groups:
            groups[key] = []
        groups[key].append(c)
    return groups
```

---

## Concept 3: Birthday Reminder with `datetime`

Birthdays are stored as `"YYYY-MM-DD"` strings. The goal: compare only **month and day**, ignoring the year, and handle the year-wrap (Dec → Jan).

```python
from datetime import date, timedelta

def birthday_reminder(book, days_ahead: int = 7) -> list:
    today = date.today()
    upcoming = []
    for c in book.contacts:
        if not c.birthday:
            continue
        try:
            bday = date.fromisoformat(c.birthday)
        except ValueError:
            continue
        this_year_bday = bday.replace(year=today.year)
        if this_year_bday < today:
            this_year_bday = bday.replace(year=today.year + 1)
        if today <= this_year_bday <= today + timedelta(days=days_ahead):
            upcoming.append(c)
    return upcoming
```

> **`date.fromisoformat()`** parses `"YYYY-MM-DD"` directly. No `strptime` needed!

---

## Concept 4: Exporting to CSV

You already know `csv.DictWriter` from Day 25. Exporting is just writing each contact dict as a row:

```python
import csv

def export_to_csv(book, filepath: str) -> int:
    fieldnames = ["contact_id", "name", "phone", "email", "city", "birthday"]
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for c in book.contacts:
            writer.writerow(c.to_dict())
    return len(book.contacts)
```

> **`newline=""`** — Always use this with `csv` on Windows to prevent blank rows.

---

## Concept 5: Finding Duplicates

Two contacts sharing the same **phone number** are duplicates.
Strategy: count occurrences per phone using a dict, then collect contacts whose phone appears more than once.

```python
def find_duplicates(book) -> list:
    phone_count = {}
    for c in book.contacts:
        phone_count[c.phone] = phone_count.get(c.phone, 0) + 1
    return [c for c in book.contacts if phone_count[c.phone] > 1]
```

> **`dict.get(key, default)`** — Returns the value if key exists, else the default. No `KeyError`!

---

## Daily Checklist
- [ ] Read concepts above
- [ ] Open `daily/day27/practice.py`
- [ ] Implement all 5 functions with **50% hints**
- [ ] Run `python practice.py` until all tests pass
