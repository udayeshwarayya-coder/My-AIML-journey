# Day 28 — Build Day: Project 7 Contact Book Website
## Project 7: Contact Book (Part 4: Build the Website)

> **Revisits from Days 1–27:** All Phase 1 concepts — OOP, CSV/JSON File I/O, decorators, exceptions, magic methods

---

## What You Are Building Today

You consolidate **all 12 logic functions** from Days 25–27 into a Flask API, then the AI-generated frontend lets users:

1. **Add / Edit / Delete** contacts (CRUD)
2. **Search** contacts by name, phone, or city
3. **Group by City** — see contacts organised by location
4. **Birthday Reminders** — see who has a birthday in the next N days
5. **Stats Dashboard** — total contacts, city count, birthday count this month
6. **CSV Import / Export** — upload a CSV or download all contacts
7. **JSON Import / Export** — same for JSON format
8. **Find Duplicates** — highlight contacts with shared phone numbers

---

## Concept 1: Consolidating Logic Functions as API Endpoints

A Flask route is just a function decorated with `@app.route(...)`.

```python
@app.route("/api/contacts", methods=["GET"])
def get_contacts():
    return jsonify([c.to_dict() for c in book.contacts])
```

> **Key rule:** Each logic function from Days 25-27 maps to exactly one API endpoint.

---

## Concept 2: `group_by_city` — Full Implementation

Groups contacts by city, returns a dict `{city: [contact_dicts, ...]}`.

```python
def group_by_city(book) -> dict:
    groups = {}
    for c in book.contacts:
        key = c.city.strip() or "Unknown"
        groups.setdefault(key, []).append(c.to_dict())
    return groups
```

> **`dict.setdefault(key, default)`** — Like `if key not in dict: dict[key] = default`, but one line!

---

## Concept 3: `birthday_reminder` Recap

The Flask endpoint wraps the function to accept a `days` query parameter:

```python
@app.route("/api/birthdays", methods=["GET"])
def get_birthdays():
    days = int(request.args.get("days", 7))
    results = birthday_reminder(book, days_ahead=days)
    return jsonify([c.to_dict() for c in results])
```

---

## Concept 4: `stats()` — New Function for Today

Returns aggregate statistics about the contact book.

```python
from datetime import date

def stats(book) -> dict:
    total = len(book.contacts)
    cities = len({c.city for c in book.contacts if c.city})
    # Birthdays this month
    today = date.today()
    bday_this_month = sum(
        1 for c in book.contacts
        if c.birthday and date.fromisoformat(c.birthday).month == today.month
    )
    return {
        "total_contacts": total,
        "unique_cities": cities,
        "birthdays_this_month": bday_this_month,
    }
```

---

## Concept 5: CSV Upload with Flask

Handling a file upload from the browser:

```python
from flask import request
import csv, io

@app.route("/api/import/csv", methods=["POST"])
def import_csv():
    file = request.files.get("file")
    content = file.read().decode("utf-8")
    reader = csv.DictReader(io.StringIO(content))
    for row in reader:
        book.contacts.append(Contact.from_dict(row))
    return jsonify({"imported": True})
```

---

## Daily Checklist
- [ ] Read concepts above
- [ ] Review `daily/day28/practice.py` — implement `stats()` + 3 integration tests
- [ ] Run `python practice.py` until all tests pass
- [ ] Start the Flask server: `python project/backend/app.py`
- [ ] Open `project/frontend/index.html` in your browser (or via Live Server)
