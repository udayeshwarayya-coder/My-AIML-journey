import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Day 28 Practice — Build Day: Project 7 Contact Book
# Project 7: Contact Book (Part 4: stats() + Integration Tests)
# Topic: dict comprehension, set comprehension, date arithmetic, Flask integration recap
#
# HINT LEVEL: 50%  (Logical steps & syntax pointers provided; write your own code!)

import csv
import json
import os
from datetime import date, timedelta


# ============================================================
# CONTACT MODEL & CONTACTBOOK CLASS (same as Days 25-27)
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


class ContactBook:
    def __init__(self):
        self.contacts: list[Contact] = []


# ============================================================
# TASK 1: stats(book) -> dict   ← NEW function for Day 28!
# ============================================================
# Returns a dict with aggregate statistics about the contact book:
# {
#   "total_contacts":       int,   — total number of contacts
#   "unique_cities":        int,   — number of distinct non-empty cities
#   "birthdays_this_month": int,   — contacts with a birthday in the current month
#   "birthdays_next_7_days":int,   — contacts with a birthday in the next 7 days
# }
#
# Requirements:
# 1. Count total contacts.
# 2. Build a set of unique non-empty city values and count it.
# 3. For birthdays_this_month: loop contacts, parse birthday with fromisoformat,
#    check if bday.month == date.today().month.
# 4. For birthdays_next_7_days: same logic as birthday_reminder (days_ahead=7).
#
# 💡 50% Hint:
# - `total = len(book.contacts)`
# - `unique_cities = len({c.city for c in book.contacts if c.city.strip()})`
# - `today = date.today()`
# - `bday.month == today.month`   ← for this-month check
# - Use `bday.replace(year=today.year)` and roll to next year if past — same as birthday_reminder

def stats(book: ContactBook) -> dict:
    # YOUR CODE HERE
    total = len(book.contacts)
    unique_cities = len({c.city.strip() for c in book.contacts if c.city.strip()})
    today = date.today()
    bday_this_month = 0
    bday_next_7 = 0
    for c in book.contacts:
        if not c.birthday:
            continue
        try:
            bday = date.fromisoformat(c.birthday)
        except ValueError:
            continue
        # Count birthdays this month
        if bday.month == today.month:
            bday_this_month += 1
        # Count birthdays in next 7 days
        this_year_bday = bday.replace(year=today.year)
        if this_year_bday < today:
            this_year_bday = bday.replace(year=today.year + 1)
        if today <= this_year_bday <= today + timedelta(days=7):
            bday_next_7 += 1
    return {
        "total_contacts":        total,
        "unique_cities":         unique_cities,
        "birthdays_this_month":  bday_this_month,
        "birthdays_next_7_days": bday_next_7,
    }


# ============================================================
# TASK 2: group_by_city_summary(book) -> dict
# ============================================================
# Returns a dict:  { city: count_of_contacts }   (not the full contact list)
# Useful for a lightweight summary to display in a dashboard widget.
#
# Requirements:
# 1. Loop over book.contacts.
# 2. Use c.city.strip() or "Unknown" as the key.
# 3. Increment count.
# 4. Return the dict sorted by count descending.
#
# 💡 50% Hint:
# - `summary = {}`
# - `summary[key] = summary.get(key, 0) + 1`
# - `return dict(sorted(summary.items(), key=lambda x: x[1], reverse=True))`

def group_by_city_summary(book: ContactBook) -> dict:
    # YOUR CODE HERE
    summary = {}
    for c in book.contacts:
        key = c.city.strip() or "Unknown"
        summary[key] = summary.get(key, 0) + 1
    return dict(sorted(summary.items(), key=lambda x: x[1], reverse=True))


# ============================================================
# TASK 3: export_and_reload(book, filepath) -> ContactBook
# ============================================================
# Integration test helper:
# 1. Export book contacts to CSV at filepath.
# 2. Read the CSV back and create a new ContactBook from it.
# 3. Return the new ContactBook.
#
# This proves that your export + import pipeline is lossless.
#
# 💡 50% Hint:
# - `with open(filepath, "w", newline="", encoding="utf-8") as f:`
# - `writer = csv.DictWriter(f, fieldnames=Contact.FIELDNAMES)`
# - `writer.writeheader()`
# - `with open(filepath, "r", encoding="utf-8") as f:`
# - `reader = csv.DictReader(f)`
# - `Contact.from_dict(row)` for each row

def export_and_reload(book: ContactBook, filepath: str) -> "ContactBook":
    # YOUR CODE HERE
    # Step 1: Export to CSV
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=Contact.FIELDNAMES)
        writer.writeheader()
        for c in book.contacts:
            writer.writerow(c.to_dict())
    # Step 2: Reload from CSV
    new_book = ContactBook()
    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            new_book.contacts.append(Contact.from_dict(row))
    return new_book


# ============================================================
# TEST RUNNER — Run: python practice.py
# ============================================================

if __name__ == "__main__":
    print("=== Day 28 Practice Tests (Stats, City Summary, Export-Reload) ===\n")

    def make_book():
        book = ContactBook()
        today = date.today()
        book.contacts = [
            Contact("C001", "Tony Stark",       "9876543210", "tony@stark.com",    "New York",   "1970-05-29"),
            Contact("C002", "Peter Parker",     "9123456780", "peter@bugle.com",   "Queens",     "2001-08-10"),
            Contact("C003", "Bruce Banner",     "9988776655", "banner@shield.com", "Dayton",     "1969-12-18"),
            Contact("C004", "Natasha Romanoff", "9111222333", "nat@shield.com",    "New York",   "1984-11-22"),
            Contact("C005", "Clint Barton",     "9911223344", "",                  "Waverly",    "1971-01-07"),
            # Birthday today (guaranteed to be counted in next-7-days)
            Contact("C006", "Birthday Person",  "9000000001", "",                  "Asgard",
                    today.strftime("%Y-%m-%d")),
            # Birthday in 5 days (within next 7)
            Contact("C007", "Soon Birthday",    "9000000002", "",                  "Westview",
                    (today + timedelta(days=5)).strftime("%Y-%m-%d")),
            # No birthday
            Contact("C008", "No Bday",          "9000000003", "",                  "",           ""),
        ]
        return book

    # ── Test 1: stats() ───────────────────────────────────────
    print("--- Test 1: stats() ---")
    book = make_book()
    result = stats(book)

    assert isinstance(result, dict),                    "stats() must return a dict"
    assert result["total_contacts"] == 8,               f"Expected 8 total, got {result['total_contacts']}"
    assert result["unique_cities"] == 6,                f"Expected 6 cities, got {result['unique_cities']}"
    # Contacts with birthday this month:
    today = date.today()
    expected_this_month = sum(
        1 for c in book.contacts
        if c.birthday and date.fromisoformat(c.birthday).month == today.month
    )
    assert result["birthdays_this_month"] == expected_this_month, \
        f"Expected {expected_this_month} this-month birthdays, got {result['birthdays_this_month']}"
    # C006 (today) and C007 (in 5 days) should both be in next_7_days
    assert result["birthdays_next_7_days"] >= 2, \
        f"Expected at least 2 next-7-day birthdays, got {result['birthdays_next_7_days']}"
    print("  stats() PASSED\n")

    # ── Test 2: group_by_city_summary() ───────────────────────
    print("--- Test 2: group_by_city_summary() ---")
    book = make_book()
    summary = group_by_city_summary(book)

    assert isinstance(summary, dict),               "Must return dict"
    assert "New York" in summary,                   "New York should be a key"
    assert summary["New York"] == 2,                f"Expected 2 New York contacts, got {summary['New York']}"
    assert "Unknown" in summary,                    "Empty city should map to 'Unknown'"
    # First key should have the highest count
    first_key = list(summary.keys())[0]
    assert summary[first_key] >= summary.get("Waverly", 0), \
        "Summary should be sorted by count descending"
    print("  group_by_city_summary() PASSED\n")

    # ── Test 3: export_and_reload() ───────────────────────────
    print("--- Test 3: export_and_reload() ---")
    book    = make_book()
    path    = "test_day28.csv"
    reloaded = export_and_reload(book, path)

    assert len(reloaded.contacts) == len(book.contacts), \
        f"Expected {len(book.contacts)} reloaded, got {len(reloaded.contacts)}"
    orig_ids     = sorted(c.contact_id for c in book.contacts)
    reloaded_ids = sorted(c.contact_id for c in reloaded.contacts)
    assert orig_ids == reloaded_ids,    "contact_ids must round-trip perfectly"
    assert reloaded.contacts[0].name == book.contacts[0].name, \
        "Names must survive export → reload"
    os.remove(path)
    print("  export_and_reload() PASSED\n")

    print("🎉 Day 28 Practice — All tests completed successfully!")
    print()
    print("📦 Project ready! Run the website:")
    print("   cd project07-contact-book/backend")
    print("   pip install flask flask-cors")
    print("   python app.py")
    print("   Then open: project07-contact-book/frontend/index.html")
