import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Day 27 Practice — OOP + File I/O: Merge, Group, Birthday & Export
# Project 7: Contact Book (Part 3: Advanced Operations)
# Topic: set comprehension, dict grouping, datetime, csv.DictWriter, dict.get()
#
# HINT LEVEL: 50%  (Logical steps & syntax pointers provided; write your own code!)

import csv
import json
import os
from datetime import date, timedelta


# ============================================================
# CONTACT MODEL & CONTACTBOOK CLASS (same as Day 25 & 26)
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
            "name":       self.name,
            "phone":      self.phone,
            "email":      self.email,
            "city":       self.city,
            "birthday":   self.birthday,
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            contact_id=data.get("contact_id", ""),
            name=data.get("name", ""),
            phone=data.get("phone", ""),
            email=data.get("email", ""),
            city=data.get("city", ""),
            birthday=data.get("birthday", ""),
        )

    def __str__(self):
        return f"[{self.contact_id}] {self.name} — Phone: {self.phone}  City: {self.city or 'N/A'}"

    def __repr__(self):
        return f'Contact(contact_id="{self.contact_id}", name="{self.name}", phone="{self.phone}")'


class ContactBook:
    def __init__(self):
        self.contacts: list[Contact] = []


# ============================================================
# TASK 1: merge_contacts(base_book, other_book) -> int
# ============================================================
# Merges contacts from other_book into base_book.
# Contacts whose contact_id already exists in base_book are SKIPPED.
#
# Requirements:
# 1. Build a set of existing contact_ids from base_book.
# 2. Loop over other_book.contacts.
# 3. If c.contact_id is NOT in the set, append it to base_book and add the id to the set.
# 4. Count and return the number of contacts actually added.
#
# 💡 50% Hint:
# - `existing_ids = {c.contact_id for c in base_book.contacts}`
# - `if c.contact_id not in existing_ids:`
# - `base_book.contacts.append(c)`
# - `existing_ids.add(c.contact_id)`
# - return the count of new contacts added

def merge_contacts(base_book: ContactBook, other_book: ContactBook) -> int:
    # YOUR CODE HERE
    existing = {c.contact_id for c in base_book.contacts}
    add = 0
    for c in other_book.contacts:
        if c.contact_id not in existing:   # BUG FIX: compare contact_id, not the object itself
            base_book.contacts.append(c)
            existing.add(c.contact_id)
            add += 1
    return add




# ============================================================
# TASK 2: group_by_city(book) -> dict
# ============================================================
# Returns a dict where each key is a city name and the value is a
# list of Contact objects in that city.
# Contacts with an empty city should go under the key "Unknown".
#
# Requirements:
# 1. Loop over book.contacts.
# 2. Use `c.city.strip() or "Unknown"` as the key.
# 3. Append each contact to the correct list in the dict.
# 4. Return the completed dict.
#
# 💡 50% Hint:
# - `groups = {}`
# - `key = c.city.strip() or "Unknown"`
# - `if key not in groups: groups[key] = []`
# - `groups[key].append(c)`

def group_by_city(book: ContactBook) -> dict:
    # YOUR CODE HERE
    citys = {}
    for c in book.contacts:
        key = c.city.strip() or "Unknown"   # BUG FIX: capital U to match test expectation
        if key not in citys:
            citys[key] = []
        citys[key].append(c)
    return citys


# ============================================================
# TASK 3: birthday_reminder(book, days_ahead=7) -> list[Contact]
# ============================================================
# Returns contacts whose birthday (month + day) falls within the
# next `days_ahead` days from today (inclusive of today).
# Contacts with an empty or invalid birthday are silently skipped.
#
# Requirements:
# 1. Get `today = date.today()`.
# 2. For each contact with a birthday, parse it: `date.fromisoformat(c.birthday)`.
# 3. Replace the year with today's year: `bday.replace(year=today.year)`.
# 4. If that date has already passed this year, roll it to next year.
# 5. If `today <= this_year_bday <= today + timedelta(days=days_ahead)`, add to results.
# 6. Return the list.
#
# 💡 50% Hint:
# - `bday = date.fromisoformat(c.birthday)` (wrap in try/except ValueError)
# - `this_year_bday = bday.replace(year=today.year)`
# - `if this_year_bday < today: this_year_bday = bday.replace(year=today.year + 1)`
# - `if today <= this_year_bday <= today + timedelta(days=days_ahead): upcoming.append(c)`

def birthday_reminder(book: ContactBook, days_ahead: int = 7) -> list:
    # BUG FIX: removed erroneous nested def; code now belongs to the outer function
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


# ============================================================
# TASK 4: export_to_csv(book, filepath: str) -> int
# ============================================================
# Writes all contacts to a CSV file with a header row.
# Returns the number of contacts written.
#
# Requirements:
# 1. Open `filepath` with "w", newline="", encoding="utf-8".
# 2. Create a `csv.DictWriter` with fieldnames = Contact.FIELDNAMES.
# 3. Write the header row with `writer.writeheader()`.
# 4. Loop and write each contact: `writer.writerow(c.to_dict())`.
# 5. Return `len(book.contacts)`.
#
# 💡 50% Hint:
# - `with open(filepath, "w", newline="", encoding="utf-8") as f:`
# - `writer = csv.DictWriter(f, fieldnames=Contact.FIELDNAMES)`
# - `writer.writeheader()`
# - `writer.writerow(c.to_dict())`

def export_to_csv(book: ContactBook, filepath: str) -> int:
    # BUG FIX: removed erroneous nested def; code now belongs to the outer function
    fieldnames = ["contact_id", "name", "phone", "email", "city", "birthday"]
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for c in book.contacts:
            writer.writerow(c.to_dict())
    return len(book.contacts)


# ============================================================
# TASK 5: find_duplicates(book) -> list[Contact]
# ============================================================
# Returns all contacts that share their phone number with at least
# one other contact in the book. A phone appearing N>1 times contributes
# all N contacts to the result.
#
# Requirements:
# 1. Build a dict: phone -> count of contacts with that phone.
# 2. Return contacts where count > 1.
#
# 💡 50% Hint:
# - `phone_count = {}`
# - `phone_count[c.phone] = phone_count.get(c.phone, 0) + 1`
# - `return [c for c in book.contacts if phone_count[c.phone] > 1]`

def find_duplicates(book: ContactBook) -> list:
    # BUG FIX: removed erroneous nested def; code now belongs to the outer function
    phone_count = {}
    for c in book.contacts:
        phone_count[c.phone] = phone_count.get(c.phone, 0) + 1
    return [c for c in book.contacts if phone_count[c.phone] > 1]


# ============================================================
# TEST RUNNER — Run: python practice.py
# ============================================================

if __name__ == "__main__":
    print("=== Day 27 Practice Tests (Merge, Group, Birthday, Export, Duplicates) ===\n")

    # Shared sample contacts
    def make_book():
        book = ContactBook()
        book.contacts = [
            Contact("C001", "Tony Stark",      "9876543210", "tony@stark.com",    "New York",  "1970-05-29"),
            Contact("C002", "Peter Parker",    "9123456780", "peter@bugle.com",   "Queens",    "2001-08-10"),
            Contact("C003", "Bruce Banner",    "9988776655", "banner@shield.com", "Dayton",    "1969-12-18"),
            Contact("C004", "Natasha Romanoff","9111222333", "nat@shield.com",    "New York",  "1984-11-22"),
            Contact("C005", "Clint Barton",    "9911223344", "",                  "Waverly",   "1971-01-07"),
        ]
        return book

    # ── Test 1: merge_contacts ────────────────────────────────
    print("--- Test 1: merge_contacts ---")
    base  = make_book()
    other = ContactBook()
    other.contacts = [
        Contact("C002", "Peter Parker",  "9123456780", "peter@bugle.com", "Queens", "2001-08-10"),  # duplicate
        Contact("C006", "Thor Odinson",  "9000000001", "thor@asgard.com", "Asgard", "0964-11-04"),  # new
        Contact("C007", "Wanda Maximoff","9000000002", "wanda@hex.com",   "Westview","1989-02-10"), # new
    ]
    added = merge_contacts(base, other)
    assert added == 2,                    f"Expected 2 added, got {added}"
    assert len(base.contacts) == 7,       f"Expected 7 total, got {len(base.contacts)}"
    ids = [c.contact_id for c in base.contacts]
    assert "C006" in ids and "C007" in ids, "New contacts not merged"
    assert ids.count("C002") == 1,        "Duplicate C002 should not be added"
    print("  merge_contacts PASSED\n")

    # ── Test 2: group_by_city ─────────────────────────────────
    print("--- Test 2: group_by_city ---")
    book = make_book()
    groups = group_by_city(book)
    assert "New York" in groups,           "Expected New York key"
    assert len(groups["New York"]) == 2,   f"Expected 2 New York contacts, got {len(groups['New York'])}"
    assert "Queens" in groups
    assert len(groups["Queens"]) == 1
    assert "Dayton" in groups
    # Add a contact with no city to test "Unknown"
    book.contacts.append(Contact("C010", "Nick Fury", "9000000099", "", "", ""))
    groups2 = group_by_city(book)
    assert "Unknown" in groups2,           "Expected 'Unknown' key for empty city"
    print("  group_by_city PASSED\n")

    # ── Test 3: birthday_reminder ─────────────────────────────
    print("--- Test 3: birthday_reminder ---")
    book = ContactBook()
    today = date.today()
    # Contact whose birthday is TODAY
    bday_today = Contact("BT1", "Today Person", "1111111111", "", "City", today.strftime("%Y-%m-%d"))
    # Contact whose birthday is in 5 days
    bday_soon  = Contact("BT2", "Soon Person",  "2222222222", "", "City", (today + timedelta(days=5)).strftime("%Y-%m-%d"))
    # Contact whose birthday is in 30 days (outside default 7-day window)
    bday_far   = Contact("BT3", "Far Person",   "3333333333", "", "City", (today + timedelta(days=30)).strftime("%Y-%m-%d"))
    # Contact with no birthday
    bday_none  = Contact("BT4", "No Bday",      "4444444444", "", "City", "")
    book.contacts = [bday_today, bday_soon, bday_far, bday_none]

    results = birthday_reminder(book, days_ahead=7)
    ids_found = [c.contact_id for c in results]
    assert "BT1" in ids_found, "Today's birthday should be included"
    assert "BT2" in ids_found, "5-days-away birthday should be included"
    assert "BT3" not in ids_found, "30-days-away birthday should NOT be included"
    assert "BT4" not in ids_found, "No-birthday contact should NOT be included"
    print("  birthday_reminder PASSED\n")

    # ── Test 4: export_to_csv ─────────────────────────────────
    print("--- Test 4: export_to_csv ---")
    book = make_book()
    csv_path = "test_export.csv"
    written = export_to_csv(book, csv_path)
    assert written == 5,          f"Expected 5 written, got {written}"
    assert os.path.exists(csv_path)
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    assert len(rows) == 5,        f"Expected 5 rows in CSV, got {len(rows)}"
    assert rows[0]["name"] == "Tony Stark"
    assert rows[0]["city"] == "New York"
    os.remove(csv_path)
    print("  export_to_csv PASSED\n")

    # ── Test 5: find_duplicates ───────────────────────────────
    print("--- Test 5: find_duplicates ---")
    book = ContactBook()
    book.contacts = [
        Contact("D001", "Alice",   "9999999999", "", ""),
        Contact("D002", "Alice2",  "9999999999", "", ""),   # same phone as D001
        Contact("D003", "Bob",     "8888888888", "", ""),
        Contact("D004", "Charlie", "7777777777", "", ""),
    ]
    dups = find_duplicates(book)
    dup_ids = [c.contact_id for c in dups]
    assert "D001" in dup_ids and "D002" in dup_ids, "Both contacts with shared phone should be returned"
    assert "D003" not in dup_ids, "Unique phone should NOT be a duplicate"
    assert len(dups) == 2,  f"Expected 2 duplicates, got {len(dups)}"
    # No duplicates case
    book2 = make_book()
    assert find_duplicates(book2) == [], "No duplicates expected in clean book"
    print("  find_duplicates PASSED\n")

    print("🎉 Day 27 Practice — All tests completed successfully!")
