import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Day 25 Practice — Industrial CSV File Handling & Data Cleaning
# Project 7: Contact Book (Part 1: Ingestion & CSV Persistence)
# Topic: csv.DictReader, csv.DictWriter, sanitization, append mode, batch audit report
#
# HINT LEVEL: 50%  (Logical steps & syntax pointers provided; write your own code!)

import csv
import os


# ============================================================
# CONTACT MODEL & CONTACTBOOK CLASS
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
        return f"[{self.contact_id}] {self.name} — 📞 {self.phone} 📍 {self.city or 'N/A'}"

    def __repr__(self):
        return f'Contact(contact_id="{self.contact_id}", name="{self.name}", phone="{self.phone}")'


class ContactBook:
    def __init__(self):
        self.contacts: list[Contact] = []


# ============================================================
# TASK 1: clean_phone(raw_phone: str) -> str
# ============================================================
# In real life, users input phone numbers like "(123) 456-7890", "+91 98765-43210",
# or "98765 43210". Standardize it to just digits!
#
# Requirements:
# 1. Extract only numeric digit characters (0-9).
# 2. If the resulting digit string is between 10 and 15 digits long, return it.
# 3. Otherwise, raise ValueError(f"Invalid phone number: '{raw_phone}'. Must contain 10-15 digits.")
#
# 💡 50% Hint:
# - Filter with `''.join(ch for ch in str(raw_phone) if ch.isdigit())`.
# - Check `10 <= len(digits) <= 15`. If valid return `digits`, else raise `ValueError`.

def clean_phone(raw_phone: str) -> str:
    # YOUR CODE HERE
    new_num="".join(ch for ch in str(raw_phone) if ch.isdigit())
    if len(new_num) <10 or len(new_num) >15:
        raise ValueError("invalid phone number please add a valid phone number ")
    else:
        return new_num

# ============================================================
# TASK 2: validate_email(email_str: str) -> bool
# ============================================================
# Validates basic email formatting for contacts.
#
# Requirements:
# 1. If email_str is empty or whitespace only, return True (email is optional).
# 2. If email_str is provided:
#    - Must contain exactly one '@' symbol.
#    - Must contain a '.' after the '@' symbol.
#    - Cannot start or end with '@' or '.'.
# 3. If valid, return True; otherwise raise ValueError(f"Invalid email address: '{email_str}'").
#
# 💡 50% Hint:
# - Strip whitespace first. If not email, return `True`.
# - Check if `'@'` is in email and `email.count('@') == 1`.
# - Split by `'@'`: `user, domain = email.split('@')`.
# - Check if `'.' in domain` and `not domain.startswith('.')` and `not domain.endswith('.')` and `len(user) > 0`.
# - Raise `ValueError` if any check fails.

def validate_email(email_str: str) -> bool:
    # YOUR CODE HERE
    pass


# ============================================================
# TASK 3: add_contact(book, name, phone, email="", city="", birthday="") -> Contact
# ============================================================
# Creates, validates, and stores a new Contact.
#
# Requirements:
# 1. Name cannot be empty. If empty, raise ValueError("Name is required.")
# 2. Clean phone using `clean_phone(phone)`.
# 3. Validate email using `validate_email(email)`.
# 4. Prevent duplicate phone numbers: If any contact in `book.contacts` already has
#    this cleaned phone number, raise ValueError(f"Contact with phone '{cleaned_phone}' already exists.")
# 5. Generate next ID: 'C' + 3-digit zero-padded number (e.g. 'C001', 'C002').
# 6. Instantiate `Contact`, append to `book.contacts`, and return the `Contact`.
#
# 💡 50% Hint:
# - Strip `name`. If not name, raise `ValueError`.
# - Call `phone = clean_phone(phone)` and `validate_email(email)`.
# - Check if `any(c.phone == phone for c in book.contacts)`.
# - Auto-generate ID using `f"C{len(book.contacts) + 1:03d}"`.

def add_contact(book: ContactBook, name: str, phone: str, email: str = "", city: str = "", birthday: str = "") -> Contact:
    # YOUR CODE HERE
    pass


# ============================================================
# TASK 4: save_contacts_csv(book, filepath: str, columns: list = None) -> int
# ============================================================
# Exports contacts to a CSV file. Supports exporting all or a subset of columns.
#
# Requirements:
# 1. If `columns` is None, use `Contact.FIELDNAMES`.
# 2. Open `filepath` with `"w"`, `newline=""`, `encoding="utf-8"`.
# 3. Use `csv.DictWriter` with `fieldnames=cols` and `extrasaction="ignore"`.
# 4. Write header, then write all contacts using `c.to_dict()`.
# 5. Return count of saved contacts.
#
# 💡 50% Hint:
# - `cols = columns if columns is not None else Contact.FIELDNAMES`.
# - `with open(filepath, "w", newline="", encoding="utf-8") as f:`.
# - `writer = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")`.
# - `writer.writeheader()`, then loop or `writer.writerows(...)`.

def save_contacts_csv(book: ContactBook, filepath: str, columns: list = None) -> int:
    # YOUR CODE HERE
    pass


# ============================================================
# TASK 5: append_contact_csv(filepath: str, contact: Contact) -> None
# ============================================================
# Appends a single contact record to an existing (or new) CSV file.
# Useful for real-time logging without rewriting the whole database file.
#
# Requirements:
# 1. Check if the file already exists using `os.path.exists(filepath)`.
# 2. Open `filepath` in append mode (`"a"`), with `newline=""`, `encoding="utf-8"`.
# 3. Use `csv.DictWriter(f, fieldnames=Contact.FIELDNAMES)`.
# 4. If file DID NOT exist before opening, call `writer.writeheader()` first.
# 5. Write the contact row: `writer.writerow(contact.to_dict())`.
#
# 💡 50% Hint:
# - `file_exists = os.path.exists(filepath)`.
# - `with open(filepath, "a", newline="", encoding="utf-8") as f:`.
# - If `not file_exists: writer.writeheader()`.
# - `writer.writerow(contact.to_dict())`.

def append_contact_csv(filepath: str, contact: Contact) -> None:
    # YOUR CODE HERE
    pass


# ============================================================
# TASK 6: load_contacts_csv(book, filepath: str) -> int
# ============================================================
# Loads contacts from a CSV file into `book.contacts`.
#
# Requirements:
# 1. If `filepath` does not exist, raise `FileNotFoundError(f"File not found: '{filepath}'")`.
# 2. Open file with `"r"`, `newline=""`, `encoding="utf-8"`.
# 3. Use `csv.DictReader(f)` to read row dictionaries.
# 4. Instantiate `Contact.from_dict(row)` and append to `book.contacts`.
# 5. Return total contacts loaded.
#
# 💡 50% Hint:
# - `if not os.path.exists(filepath): raise FileNotFoundError(...)`.
# - `reader = csv.DictReader(f)`.
# - Loop over `reader` and append `Contact.from_dict(row)`.

def load_contacts_csv(book: ContactBook, filepath: str) -> int:
    # YOUR CODE HERE
    pass


# ============================================================
# TASK 7: import_csv_with_report(book, filepath: str) -> dict
# ============================================================
# Real-world batch ingestion engine! Reads a potentially messy CSV file,
# imports all valid contacts, skips invalid ones, and generates an audit report.
#
# Requirements:
# 1. If `filepath` does not exist, raise `FileNotFoundError`.
# 2. Track an audit report dictionary:
#    `{"total_rows": 0, "success_count": 0, "skipped_count": 0, "errors": []}`
# 3. Open CSV using `csv.DictReader(f)`.
# 4. For each row (enumerate starting at index 1):
#    - Increment `total_rows`.
#    - Wrap `add_contact()` call in a `try...except Exception as e:` block.
#    - On success: increment `success_count`.
#    - On failure: increment `skipped_count`, append `{"row_index": index, "data": row, "error": str(e)}` to `errors`.
# 5. Return the report dictionary.
#
# 💡 50% Hint:
# - Set up the report dict template.
# - Loop: `for idx, row in enumerate(reader, start=1):`
# - In `try`: call `add_contact(book, row.get('name'), row.get('phone'), ...)`.
# - In `except Exception as err`: record the skip in report.

def import_csv_with_report(book: ContactBook, filepath: str) -> dict:
    # YOUR CODE HERE
    pass


# ============================================================
# TEST RUNNER — Run: python practice.py
# ============================================================

if __name__ == "__main__":
    print("=== Day 25 Practice Tests (Industrial CSV & Validation) ===\n")

    # ── Test 1: Data Cleaning & Normalization ───────────────────
    print("--- Test 1: clean_phone & validate_email ---")
    assert clean_phone("(123) 456-7890") == "1234567890"
    assert clean_phone("+91 98765-43210") == "919876543210"
    try:
        clean_phone("123")  # Too short
        assert False, "Should reject short phone number"
    except ValueError:
        pass

    assert validate_email("tony@stark.com") is True
    assert validate_email("") is True  # Optional
    try:
        validate_email("bad-email-without-at.com")
        assert False, "Should reject email without @"
    except ValueError:
        pass
    print("  Phone cleaning & Email validation PASSED\n")

    # ── Test 2: add_contact & Duplicate Prevention ─────────────
    print("--- Test 2: add_contact ---")
    book = ContactBook()
    c1 = add_contact(book, "Tony Stark", "(987) 654-3210", "tony@stark.com", "New York", "1970-05-29")
    assert c1.contact_id == "C001"
    assert c1.phone == "9876543210"  # Stored cleaned!
    assert len(book.contacts) == 1

    try:
        # Duplicate phone test (even with different formatting)
        add_contact(book, "Tony Clone", "987-654-3210")
        assert False, "Should reject duplicate phone number"
    except ValueError as e:
        print(f"  Duplicate phone prevented: {e}")
    print("  add_contact PASSED\n")

    # ── Test 3: save_contacts_csv (Full & Partial Columns) ─────
    print("--- Test 3: save_contacts_csv ---")
    add_contact(book, "Peter Parker", "9123456780", "peter@dailybugle.com", "Queens", "2001-08-10")
    
    # 3A: Full Export
    csv_full = "test_full.csv"
    count = save_contacts_csv(book, csv_full)
    assert count == 2
    assert os.path.exists(csv_full)
    with open(csv_full, "r", encoding="utf-8") as f:
        header = f.readline().strip()
    assert header == "contact_id,name,phone,email,city,birthday"
    print("  Full CSV export verified")

    # 3B: Partial Columns Export (e.g. for phone directory)
    csv_partial = "test_partial.csv"
    save_contacts_csv(book, csv_partial, columns=["name", "phone"])
    with open(csv_partial, "r", encoding="utf-8") as f:
        partial_header = f.readline().strip()
    assert partial_header == "name,phone"
    print("  Partial columns export verified")

    os.remove(csv_full)
    os.remove(csv_partial)
    print("  PASSED\n")

    # ── Test 4: append_contact_csv ─────────────────────────────
    print("--- Test 4: append_contact_csv ---")
    csv_append = "test_append.csv"
    if os.path.exists(csv_append):
        os.remove(csv_append)

    c_app1 = Contact("C001", "Steve Rogers", "9000000001", "cap@avengers.com", "Brooklyn")
    append_contact_csv(csv_append, c_app1)  # Created new file with header
    
    c_app2 = Contact("C002", "Natasha Romanoff", "9000000002", "nat@avengers.com", "St. Petersburg")
    append_contact_csv(csv_append, c_app2)  # Appended row only

    with open(csv_append, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]
    assert len(lines) == 3, f"Expected 3 lines (1 header + 2 contacts), got {len(lines)}"
    assert lines[0].startswith("contact_id")
    assert "Steve Rogers" in lines[1]
    assert "Natasha Romanoff" in lines[2]
    os.remove(csv_append)
    print("  Incremental CSV append verified & PASSED\n")

    # ── Test 5: load_contacts_csv ─────────────────────────────
    print("--- Test 5: load_contacts_csv ---")
    test_load_file = "test_load.csv"
    save_contacts_csv(book, test_load_file)
    
    fresh_book = ContactBook()
    loaded_cnt = load_contacts_csv(fresh_book, test_load_file)
    assert loaded_cnt == 2
    assert fresh_book.contacts[0].name == "Tony Stark"
    assert fresh_book.contacts[1].name == "Peter Parker"
    os.remove(test_load_file)
    print("  load_contacts_csv verified & PASSED\n")

    # ── Test 6: import_csv_with_report (Batch Audit Ingestion) ─
    print("--- Test 6: import_csv_with_report ---")
    dirty_csv = "test_dirty.csv"
    # Create sample dirty CSV: 2 valid rows, 1 bad phone, 1 duplicate phone
    with open(dirty_csv, "w", newline="", encoding="utf-8") as f:
        f.write("name,phone,email,city,birthday\n")
        f.write("Bruce Banner,9988776655,banner@avengers.com,Dayton,1969-12-18\n")  # Valid
        f.write("Thor Odinson,123,thor@asgard.com,Asgard,0965-01-01\n")               # Bad Phone (<10 digits)
        f.write("Clint Barton,9911223344,hawkeye@avengers.com,Waverly,1971-01-07\n") # Valid
        f.write("Bruce Imposter,9988776655,fake@banner.com,Dayton,1969-12-18\n")      # Duplicate Phone
    
    audit_book = ContactBook()
    report = import_csv_with_report(audit_book, dirty_csv)
    
    assert report["total_rows"] == 4, f"Expected 4 total rows, got {report['total_rows']}"
    assert report["success_count"] == 2, f"Expected 2 successes, got {report['success_count']}"
    assert report["skipped_count"] == 2, f"Expected 2 skipped rows, got {report['skipped_count']}"
    assert len(report["errors"]) == 2
    assert len(audit_book.contacts) == 2
    print(f"  Audit Report: {report['success_count']} imported, {report['skipped_count']} skipped.")
    print(f"  Captured Errors: {[e['error'] for e in report['errors']]}")
    
    os.remove(dirty_csv)
    print("  Resilient batch import verified & PASSED\n")

    print("🎉 Day 25 Practice — All industrial tests completed successfully!")
