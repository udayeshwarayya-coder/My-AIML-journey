# Day 25 — CSV File Handling: Reading, Writing & Real-World Ingestion
## Project 7: Contact Book (Part 1: Industrial CSV Persistence & Data Cleaning)

> **Revisits from Days 1–24:** `class`, `__init__`, `self`, `to_dict()`/`from_dict()`, Custom Exceptions, File I/O (`with open`), Context Managers

---

## 🧒 Taught Like You Are 10 Years Old

Imagine receiving an Excel sheet of 500 phone numbers from your school or company.
Some people typed `"+91 98765-43210"`, others wrote `"(123) 456-7890"`, some forgot to enter their phone number entirely, and someone entered a fake email without an `@` sign!

If a computer program just crashes on line 12 because of one bad character, it's useless.
A **real-world software engineer** builds:
1. **Data Sanitizers:** Automatically cleans messy inputs (removing spaces, dashes, parentheses).
2. **Resilient CSV Exporters & Importers:** Capable of writing selected columns, appending new records on the fly, and ingesting dirty CSV spreadsheets while generating an **audit report** of what was saved and what was skipped.

---

## What You Are Building Today

Today, you build an industrial-grade Contact data engine:

1. **`clean_phone(raw_phone)`** — Cleans and standardizes phone numbers (e.g., `"(123) 456-7890"` ➔ `"1234567890"`).
2. **`validate_email(email)`** — Verifies email syntax.
3. **`add_contact(book, ...)`** — Validates, cleans data, checks for duplicates, and auto-generates IDs (`C001`, `C002`).
4. **`save_contacts_csv(book, filepath, columns=None)`** — Full or partial column export using `csv.DictWriter`.
5. **`append_contact_csv(filepath, contact)`** — Incrementally appends a single row (`mode="a"`) without re-writing the entire file.
6. **`load_contacts_csv(book, filepath)`** — Standard CSV loading with `csv.DictReader`.
7. **`import_csv_with_report(book, filepath)`** — Industrial batch importer that processes dirty CSV files, adds valid rows, and outputs a diagnostic report of successes and skips.

---

## Concept 1: Data Cleaning & Normalization

Never trust user or CSV input blindly! Always sanitize before storing:

```python
def clean_phone(raw_phone: str) -> str:
    # Keep only digits
    digits = "".join(ch for ch in str(raw_phone) if ch.isdigit())
    if len(digits) < 10 or len(digits) > 15:
        raise ValueError(f"Invalid phone number: '{raw_phone}'. Must contain 10-15 digits.")
    return digits
```

---

## Concept 2: Writing & Partial Column Export (`csv.DictWriter`)

When saving to CSV, users sometimes want only specific columns (e.g. just `name` and `phone` for an SMS campaign):

```python
import csv

def save_contacts_csv(book, filepath, columns=None):
    cols = columns or Contact.FIELDNAMES
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        # extrasaction="ignore" safely ignores dictionary keys not in cols!
        writer = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        writer.writeheader()
        for contact in book.contacts:
            writer.writerow(contact.to_dict())
```

---

## Concept 3: Incremental File Appending (`mode="a"`)

Opening a 100MB file with `mode="w"` rewrites the whole file from scratch (slow!).
Instead, use `mode="a"` (append mode) to add a single new row to the end of the CSV instantly:

```python
def append_contact_csv(filepath: str, contact: Contact):
    file_exists = os.path.exists(filepath)
    with open(filepath, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=Contact.FIELDNAMES)
        if not file_exists:
            writer.writeheader()
        writer.writerow(contact.to_dict())
```

---

## Concept 4: Resilient Batch Ingestion (The Audit Report Pattern)

In production data engineering, a CSV importer must **never crash** halfway through a file.
It should use a `try...except` inside the row loop:

```python
report = {"total_rows": 0, "success_count": 0, "skipped_count": 0, "errors": []}

for index, row in enumerate(reader, start=1):
    report["total_rows"] += 1
    try:
        # Validate and add contact
        add_contact(book, ...)
        report["success_count"] += 1
    except Exception as err:
        report["skipped_count"] += 1
        report["errors"].append({"row_index": index, "data": row, "error": str(err)})
```

---

## 🎯 Daily Checklist
- [ ] Read concepts above
- [ ] Open `daily/day25/practice.py`
- [ ] Implement all 6 functions with **50% hints**
- [ ] Run `python practice.py` until all tests pass
