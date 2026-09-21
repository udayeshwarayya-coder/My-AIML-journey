# Day 26 — JSON Persistence, Search, Filter & Sort
## Project 7: Contact Book (Part 2: JSON Persistence & Smart Querying)

> **Revisits from Days 1–25:** `class`, `__init__`, `to_dict()`/`from_dict()`, Custom Exceptions, File I/O (`json`, `csv`), `sorted()`, `lambda`, `list comprehension`

---

## 🧒 Taught Like You Are 10 Years Old

On **Day 25**, you built a Contact Book that could read and write **CSV** files.
But CSV has one problem — every time you want to update a contact, you have to re-read the whole file, find the row, change it, and re-write everything. That is slow!

**JSON** is smarter for this. It stores your contacts in a nested dictionary structure so Python can load the whole thing into memory instantly, modify it, and save it back — all in 3 lines!

Today you also teach the Contact Book to **search**, **filter**, and **sort** — just like Google Contacts does when you type a name in the search bar.

---

## What You Are Building Today

1. **`save_contacts_json(book, filepath)`** — Exports all contacts to a JSON file.
2. **`load_contacts_json(book, filepath)`** — Loads contacts from a JSON file (clears book first).
3. **`search_contacts(book, query)`** — Case-insensitive search across name, phone, email, city.
4. **`filter_by_city(book, city)`** — Returns all contacts in a given city.
5. **`sort_contacts(book, by="name")`** — Returns contacts sorted by `name`, `city`, or `contact_id`.
6. **`contact_stats(book)`** — Returns a summary dict: total, unique_cities, with_email, without_email.
7. **`delete_contact(book, contact_id)`** — Removes a contact by ID; raises `KeyError` if not found.
8. **`update_contact(book, contact_id, **kwargs)`** — Updates one or more fields of an existing contact.

---

## Concept 1: JSON Persistence (`json.dump` / `json.load`)

JSON is the industry standard for storing structured data. Python's `json` module converts dicts/lists to text files and back:

```python
import json

def save_contacts_json(book, filepath: str) -> int:
    data = [c.to_dict() for c in book.contacts]
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    return len(data)
```

Loading back:
```python
def load_contacts_json(book, filepath: str) -> int:
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)          # Returns a Python list of dicts
    book.contacts.clear()            # Reset the book first!
    for item in data:
        book.contacts.append(Contact.from_dict(item))
    return len(book.contacts)
```

> **`ensure_ascii=False`** lets non-English characters (like Indian names) be stored as-is instead of ugly `\u0041` escape codes.

---

## Concept 2: Search with List Comprehensions

Real search engines are case-insensitive — searching "tony" finds "Tony Stark":

```python
def search_contacts(book, query: str) -> list:
    q = query.strip().lower()
    return [
        c for c in book.contacts
        if q in c.name.lower()
        or q in c.phone
        or q in c.email.lower()
        or q in c.city.lower()
    ]
```

💡 **Why `strip().lower()`?** Because `"  TONY  "` should still match `"tony@stark.com"`.

---

## Concept 3: Filter & Sort

**Filter** returns a subset by condition:
```python
def filter_by_city(book, city: str) -> list:
    city_lower = city.strip().lower()
    return [c for c in book.contacts if c.city.lower() == city_lower]
```

**Sort** uses Python's built-in `sorted()` with a `key=` lambda:
```python
def sort_contacts(book, by: str = "name") -> list:
    valid_keys = {"name", "city", "contact_id"}
    if by not in valid_keys:
        raise ValueError(f"Cannot sort by '{by}'. Choose from: {valid_keys}")
    return sorted(book.contacts, key=lambda c: getattr(c, by).lower())
```

> **`getattr(c, by)`** is a clever trick: instead of writing `if by == "name": key = c.name`, you dynamically access the attribute by its string name.

---

## Concept 4: Stats Dictionary

A stats function answers questions like "How many cities are represented?" in one call:

```python
def contact_stats(book) -> dict:
    total = len(book.contacts)
    cities = {c.city for c in book.contacts if c.city}   # A set removes duplicates!
    with_email = sum(1 for c in book.contacts if c.email)
    return {
        "total": total,
        "unique_cities": len(cities),
        "with_email": with_email,
        "without_email": total - with_email,
    }
```

---

## Concept 5: Delete & Update by ID

In a real database, records are identified by a unique key (like `contact_id`).

**Delete:**
```python
def delete_contact(book, contact_id: str) -> Contact:
    for i, c in enumerate(book.contacts):
        if c.contact_id == contact_id:
            return book.contacts.pop(i)
    raise KeyError(f"Contact '{contact_id}' not found.")
```

**Update (with `**kwargs` for flexibility):**
```python
def update_contact(book, contact_id: str, **kwargs) -> Contact:
    for c in book.contacts:
        if c.contact_id == contact_id:
            for field, value in kwargs.items():
                if hasattr(c, field):
                    setattr(c, field, str(value).strip())
            return c
    raise KeyError(f"Contact '{contact_id}' not found.")
```

> **`setattr(obj, name, value)`** is the write version of `getattr`. It lets you set any attribute by its string name dynamically.

---

## Daily Checklist
- [ ] Read concepts above
- [ ] Open `daily/day26/practice.py`
- [ ] Implement all 8 functions with **50% hints**
- [ ] Run `python practice.py` until all tests pass
