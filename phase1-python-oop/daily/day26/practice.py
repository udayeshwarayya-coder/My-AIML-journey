import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Day 26 Practice — JSON Persistence, Search, Filter & Sort
# Project 7: Contact Book (Part 2: JSON Persistence & Smart Querying)
# Topic: json.dump, json.load, list comprehension filtering, sorted(), getattr/setattr, **kwargs
#
# HINT LEVEL: 50%  (Logical steps & syntax pointers provided; write your own code!)

import csv
import json
import os


# ============================================================
# CONTACT MODEL & CONTACTBOOK CLASS (same as Day 25)
# ============================================================

class Contact:
    FIELDNAMES = ["contact_id", "name", "phone", "email", "city", "birthday"]

    def __init__(self, contact_id: str, name: str, phone: str, email: str = "", city: str = "", birthday: str = ""):
        self.contact_id = str(contact_id).strip()
        self.name       = str(name).strip()
        self.phone      = str(phone).strip()
        self.email      = str(email).strip()
        self.city       = str(city).strip()
        self.birthday   = str(birthday).strip()

    def to_dict(self) -> dict:
        return {
            "contact_id": self.contact_id,
            "name": self.name,
            "phone": self.phone,
            "email": self.email,
            "city": self.city,
            "birthday": self.birthday
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            contact_id=data.get("contact_id", ""),
            name=data.get("name", ""),
            phone=data.get("phone", ""),
            email=data.get("email", ""),
            city=data.get("city", ""),
            birthday=data.get("birthday", "")
        )

    def __str__(self):
        return f"[{self.contact_id}] {self.name} — Phone: {self.phone}  City: {self.city or 'N/A'}"

    def __repr__(self):
        return f'Contact(contact_id="{self.contact_id}", name="{self.name}", phone="{self.phone}")'


class ContactBook:
    def __init__(self):
        self.contacts: list[Contact] = []


# ============================================================
# TASK 1: save_contacts_json(book, filepath: str) -> int
# ============================================================
# Saves all contacts to a JSON file (replaces the file each time).
#
# Requirements:
# 1. Convert every Contact to a dict using `contact.to_dict()`.
# 2. Open `filepath` with "w" mode, encoding="utf-8".
# 3. Write with `json.dump(data, f, indent=2, ensure_ascii=False)`.
# 4. Return the count of contacts saved.
#
# 💡 50% Hint:
# - `data = [c.to_dict() for c in book.contacts]`
# - `with open(filepath, "w", encoding="utf-8") as f:`
# - `json.dump(data, f, indent=2, ensure_ascii=False)`
# - `return len(data)`

def save_contacts_json(book: ContactBook, filepath: str) -> int:
    # YOUR CODE HERE
    data=[c.to_dict() for c in book.contacts]
    with open(filepath,"w",encoding="utf-8") as f:
        json.dump(data,f,indent=2,ensure_ascii=False)
    return len(data)
# ============================================================
# TASK 2: load_contacts_json(book, filepath: str) -> int
# ============================================================
# Loads contacts from a JSON file into `book`, replacing existing contacts.
#
# Requirements:
# 1. If `filepath` does not exist, raise `FileNotFoundError(f"File not found: '{filepath}'")`
# 2. Open with "r" mode, encoding="utf-8".
# 3. Use `json.load(f)` to get a list of dicts.
# 4. Call `book.contacts.clear()` to reset the book.
# 5. Loop over loaded dicts and append `Contact.from_dict(item)` to `book.contacts`.
# 6. Return the count of contacts loaded.
#
# 💡 50% Hint:
# - `if not os.path.exists(filepath): raise FileNotFoundError(...)`
# - `data = json.load(f)`
# - `book.contacts.clear()`
# - `book.contacts.append(Contact.from_dict(item))`

def load_contacts_json(book: ContactBook, filepath: str) -> int:
    # YOUR CODE HERE
    if os.path.exists(filepath):
        with open(filepath,"r",encoding="utf-8") as f:
            data=json.load(f)
            book.contacts.clear()
            for item in data:
                book.contacts.append(Contact.from_dict(item))
            return len(data)
    else:
        raise FileNotFoundError(f"file {filepath} not found ")

# ============================================================
# TASK 3: search_contacts(book, query: str) -> list[Contact]
# ============================================================
# Returns a list of contacts whose name, phone, email, OR city
# contains the query string (case-insensitive).
#
# Requirements:
# 1. Strip and lowercase the query: `q = query.strip().lower()`.
# 2. Return contacts where `q` appears in any of: name, phone, email, city (all lowercased).
# 3. Return an empty list if nothing matches (not an error).
#
# 💡 50% Hint:
# - Use a list comprehension with `if q in c.name.lower() or q in c.phone or ...`
# - `c.city.lower()` handles empty city gracefully (empty string won't crash)

def search_contacts(book: ContactBook, query: str) -> list:
    # YOUR CODE HERE
    q=query.strip().lower()
    return [c for c in book.contacts if q in c.name.lower() or q in c.phone.lower() or q in c.email.lower() or q in c.city.lower()]


# ============================================================
# TASK 4: filter_by_city(book, city: str) -> list[Contact]
# ============================================================
# Returns all contacts whose city exactly matches (case-insensitive).
#
# Requirements:
# 1. Strip and lowercase the target city.
# 2. Return contacts where `c.city.lower() == city_lower`.
#
# 💡 50% Hint:
# - `city_lower = city.strip().lower()`
# - `return [c for c in book.contacts if c.city.lower() == city_lower]`

def filter_by_city(book: ContactBook, city: str) -> list:
    # YOUR CODE HERE
    city_lower=city.strip().lower()
    return [c for c in book.contacts if c.city.lower() == city_lower]



# ============================================================
# TASK 5: sort_contacts(book, by: str = "name") -> list[Contact]
# ============================================================
# Returns a sorted copy of book.contacts (does NOT modify in place).
#
# Requirements:
# 1. Only allow sorting by: "name", "city", "contact_id".
#    If `by` is anything else, raise ValueError(f"Cannot sort by '{by}'. Choose: name, city, contact_id").
# 2. Sort case-insensitively using `getattr(c, by).lower()` as the key.
# 3. Return sorted list (use `sorted(...)`, NOT `.sort()`).
#
# 💡 50% Hint:
# - `valid = {"name", "city", "contact_id"}`
# - `if by not in valid: raise ValueError(...)`
# - `return sorted(book.contacts, key=lambda c: getattr(c, by).lower())`

def sort_contacts(book: ContactBook, by: str = "name") -> list:
    # YOUR CODE HERE
    valid={"name","city","contact_id"}
    if by not in valid:
        raise ValueError(f"contacts cannot be sorted {by} this methods ")
    return sorted(book.contacts,key=lambda c:getattr(c,by).lower())


# ============================================================
# TASK 6: contact_stats(book) -> dict
# ============================================================
# Returns a statistics summary of the contact book.
#
# Requirements: Return a dict with these keys:
# - "total"          : total number of contacts
# - "unique_cities"  : number of distinct non-empty city values
# - "with_email"     : number of contacts that have a non-empty email
# - "without_email"  : total - with_email
#
# 💡 50% Hint:
# - `cities = {c.city for c in book.contacts if c.city}` gives a set of unique cities
# - `with_email = sum(1 for c in book.contacts if c.email)`

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
# ============================================================
# TASK 7: delete_contact(book, contact_id: str) -> Contact
# ============================================================
# Removes and returns the contact with matching contact_id.
# Raises KeyError if the contact_id is not found.
#
# Requirements:
# 1. Loop through `book.contacts` with `enumerate`.
# 2. If `c.contact_id == contact_id`, call `book.contacts.pop(i)` and return the removed contact.
# 3. If the loop ends without a match, raise `KeyError(f"Contact '{contact_id}' not found.")`.
#
# 💡 50% Hint:
# - `for i, c in enumerate(book.contacts):`
# - `if c.contact_id == contact_id: return book.contacts.pop(i)`
# - `raise KeyError(...)` after the loop

def delete_contact(book: ContactBook, contact_id: str) -> Contact:
    # YOUR CODE HERE
    for i,c in enumerate(book.contacts):
        if c.contact_id==contact_id:
            return book.contacts.pop(i)
    raise KeyError(f"Contact '{contact_id}' not found.")


# ============================================================
# TASK 8: update_contact(book, contact_id: str, **kwargs) -> Contact
# ============================================================
# Updates one or more fields of an existing contact.
# Raises KeyError if the contact_id is not found.
#
# Requirements:
# 1. Loop through `book.contacts` to find contact with matching contact_id.
# 2. For each key-value pair in `kwargs`:
#    - Only update if the attribute exists (`hasattr(c, field)`).
#    - Use `setattr(c, field, str(value).strip())` to set the value.
# 3. Return the updated contact.
# 4. Raise `KeyError(f"Contact '{contact_id}' not found.")` if not found.
#
# 💡 50% Hint:
# - `for c in book.contacts: if c.contact_id == contact_id:`
# - `for field, value in kwargs.items(): if hasattr(c, field): setattr(c, field, str(value).strip())`
# - `raise KeyError(...)` after the loop

def update_contact(book: ContactBook, contact_id: str, **kwargs) -> Contact:
    # YOUR CODE HERE
    for c in book.contacts:
        if c.contact_id==contact_id:
            for f,v in kwargs.items():
                if hasattr(c,f):
                    setattr(c,f,str(v).strip())
            return c
    raise KeyError(f"Contact '{contact_id}' not found.")


# ============================================================
# TEST RUNNER — Run: python practice.py
# ============================================================

if __name__ == "__main__":
    print("=== Day 26 Practice Tests (JSON Persistence & Smart Querying) ===\n")

    # ── Test 1: JSON Save & Load ─────────────────────────────────
    print("--- Test 1: save_contacts_json & load_contacts_json ---")
    book = ContactBook()
    book.contacts = [
        Contact("C001", "Tony Stark",     "9876543210", "tony@stark.com",   "New York",  "1970-05-29"),
        Contact("C002", "Peter Parker",   "9123456780", "peter@bugle.com",  "Queens",    "2001-08-10"),
        Contact("C003", "Bruce Banner",   "9988776655", "banner@shield.com","Dayton",    "1969-12-18"),
        Contact("C004", "Natasha Romanoff","9111222333","nat@shield.com",   "New York",  "1984-11-22"),
        Contact("C005", "Clint Barton",   "9911223344", "",                 "Waverly",   "1971-01-07"),
    ]

    json_file = "test_contacts.json"
    saved = save_contacts_json(book, json_file)
    assert saved == 5, f"Expected 5 saved, got {saved}"
    assert os.path.exists(json_file)

    fresh_book = ContactBook()
    loaded = load_contacts_json(fresh_book, json_file)
    assert loaded == 5, f"Expected 5 loaded, got {loaded}"
    assert fresh_book.contacts[0].name == "Tony Stark"
    assert fresh_book.contacts[2].city == "Dayton"

    try:
        load_contacts_json(fresh_book, "no_such_file.json")
        assert False, "Should raise FileNotFoundError"
    except FileNotFoundError:
        pass

    os.remove(json_file)
    print("  JSON save & load PASSED\n")

    # ── Test 2: search_contacts ─────────────────────────────────
    print("--- Test 2: search_contacts ---")
    results = search_contacts(book, "tony")
    assert len(results) == 1 and results[0].name == "Tony Stark"

    results = search_contacts(book, "new york")
    assert len(results) == 2  # Tony & Natasha

    results = search_contacts(book, "shield.com")
    assert len(results) == 2  # Banner & Natasha

    results = search_contacts(book, "ZZZNOMATCH")
    assert results == []

    print("  search_contacts PASSED\n")

    # ── Test 3: filter_by_city ──────────────────────────────────
    print("--- Test 3: filter_by_city ---")
    ny = filter_by_city(book, "New York")
    assert len(ny) == 2

    ny_case = filter_by_city(book, "new york")
    assert len(ny_case) == 2  # Case-insensitive!

    none_found = filter_by_city(book, "Asgard")
    assert none_found == []

    print("  filter_by_city PASSED\n")

    # ── Test 4: sort_contacts ───────────────────────────────────
    print("--- Test 4: sort_contacts ---")
    by_name = sort_contacts(book, by="name")
    names = [c.name for c in by_name]
    assert names == sorted(names, key=str.lower), f"Not sorted by name: {names}"

    by_city = sort_contacts(book, by="city")
    cities = [c.city for c in by_city]
    assert cities == sorted(cities, key=str.lower), f"Not sorted by city: {cities}"

    try:
        sort_contacts(book, by="birthday")
        assert False, "Should raise ValueError for invalid sort key"
    except ValueError:
        pass

    print("  sort_contacts PASSED\n")

    # ── Test 5: contact_stats ───────────────────────────────────
    print("--- Test 5: contact_stats ---")
    stats = contact_stats(book)
    assert stats["total"] == 5,            f"Expected 5 total, got {stats['total']}"
    assert stats["unique_cities"] == 4,    f"Expected 4 cities, got {stats['unique_cities']}"
    assert stats["with_email"] == 4,       f"Expected 4 with email, got {stats['with_email']}"  # Clint has no email
    assert stats["without_email"] == 1,    f"Expected 1 without email, got {stats['without_email']}"
    print(f"  Stats: {stats}")
    print("  contact_stats PASSED\n")

    # ── Test 6: delete_contact ──────────────────────────────────
    print("--- Test 6: delete_contact ---")
    removed = delete_contact(book, "C003")
    assert removed.name == "Bruce Banner"
    assert len(book.contacts) == 4

    try:
        delete_contact(book, "C003")  # Already deleted
        assert False, "Should raise KeyError"
    except KeyError:
        pass

    print("  delete_contact PASSED\n")

    # ── Test 7: update_contact ──────────────────────────────────
    print("--- Test 7: update_contact ---")
    updated = update_contact(book, "C001", city="Malibu", email="tony@malibu.com")
    assert updated.city == "Malibu"
    assert updated.email == "tony@malibu.com"
    assert updated.name == "Tony Stark"  # Unchanged field stays intact

    try:
        update_contact(book, "C999", name="Ghost")
        assert False, "Should raise KeyError"
    except KeyError:
        pass

    print("  update_contact PASSED\n")

    print("🎉 Day 26 Practice — All tests completed successfully!")
