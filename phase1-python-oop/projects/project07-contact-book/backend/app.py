import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Project 7: Contact Book — Flask Backend API
# Built for Phase 1 Python OOP Milestone (Days 25–28)
# Concepts covered:
# - Day 25: CSV reading/writing (load_contacts_csv, save_contacts_csv, add_contact)
# - Day 26: JSON reading/writing (export_json, import_json, merge_contacts)
# - Day 27: Advanced OOP + File I/O (merge, group_by_city, birthday_reminder, export_to_csv, find_duplicates)
# - Day 28: Build Day — stats(), group_by_city(), birthday_reminder() as API endpoints
#
# Run:
#   cd "d:/python next/phase1-python-oop/projects/project07-contact-book/backend"
#   pip install flask flask-cors
#   python app.py

import csv
import io
import json
import os
import uuid
from datetime import date, timedelta
from flask import Flask, jsonify, request, send_file, Response
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

DATA_FILE = os.path.join(os.path.dirname(__file__), "contacts_data.json")


# ============================================================
# CONTACT MODEL (Days 25–28)
# ============================================================

class Contact:
    FIELDNAMES = ["contact_id", "name", "phone", "email", "city", "birthday"]

    def __init__(self, contact_id: str, name: str, phone: str,
                 email: str = "", city: str = "", birthday: str = ""):
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
# PERSISTENCE HELPERS (Day 25 & 26)
# ============================================================

def _load_from_file() -> ContactBook:
    """Load contacts from the JSON data file into a ContactBook."""
    book = ContactBook()
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            book.contacts = [Contact.from_dict(d) for d in data]
        except (json.JSONDecodeError, KeyError):
            book.contacts = []
    return book


def _save_to_file(book: ContactBook) -> None:
    """Persist the ContactBook to the JSON data file."""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump([c.to_dict() for c in book.contacts], f, indent=2, ensure_ascii=False)


# ============================================================
# LOGIC FUNCTIONS (Days 25–28)
# ============================================================

def merge_contacts(base_book: ContactBook, other_book: ContactBook) -> int:
    """Day 26/27: Add contacts from other_book into base_book, skip duplicate IDs."""
    existing_ids = {c.contact_id for c in base_book.contacts}
    added = 0
    for c in other_book.contacts:
        if c.contact_id not in existing_ids:
            base_book.contacts.append(c)
            existing_ids.add(c.contact_id)
            added += 1
    return added


def group_by_city(book: ContactBook) -> dict:
    """Day 27/28: Returns dict mapping city -> list of contact dicts."""
    groups: dict[str, list] = {}
    for c in book.contacts:
        key = c.city.strip() or "Unknown"
        groups.setdefault(key, []).append(c.to_dict())
    return groups


def birthday_reminder(book: ContactBook, days_ahead: int = 7) -> list:
    """Day 27/28: Returns contacts whose birthday falls within the next N days."""
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


def find_duplicates(book: ContactBook) -> list:
    """Day 27: Returns contacts that share a phone number with another contact."""
    phone_count: dict[str, int] = {}
    for c in book.contacts:
        phone_count[c.phone] = phone_count.get(c.phone, 0) + 1
    return [c for c in book.contacts if phone_count[c.phone] > 1]


def stats(book: ContactBook) -> dict:
    """Day 28: Returns aggregate statistics about the contact book."""
    total = len(book.contacts)
    unique_cities = len({c.city.strip() for c in book.contacts if c.city.strip()})
    today = date.today()
    bday_this_month = 0
    bday_next_7_days = 0
    for c in book.contacts:
        if not c.birthday:
            continue
        try:
            bday = date.fromisoformat(c.birthday)
        except ValueError:
            continue
        if bday.month == today.month:
            bday_this_month += 1
        this_year = bday.replace(year=today.year)
        if this_year < today:
            this_year = bday.replace(year=today.year + 1)
        if today <= this_year <= today + timedelta(days=7):
            bday_next_7_days += 1
    return {
        "total_contacts":      total,
        "unique_cities":       unique_cities,
        "birthdays_this_month": bday_this_month,
        "birthdays_next_7_days": bday_next_7_days,
    }


# ============================================================
# API ROUTES
# ============================================================

# ── CRUD: Contacts ────────────────────────────────────────────

@app.route("/api/contacts", methods=["GET"])
def get_contacts():
    """GET /api/contacts — List all contacts (supports ?search= query param)."""
    book = _load_from_file()
    query = request.args.get("search", "").strip().lower()
    contacts = book.contacts
    if query:
        contacts = [
            c for c in contacts
            if query in c.name.lower()
            or query in c.phone.lower()
            or query in c.email.lower()
            or query in c.city.lower()
        ]
    return jsonify([c.to_dict() for c in contacts])


@app.route("/api/contacts", methods=["POST"])
def add_contact():
    """POST /api/contacts — Add a new contact."""
    book = _load_from_file()
    data = request.get_json(force=True)
    if not data.get("name") or not data.get("phone"):
        return jsonify({"error": "name and phone are required"}), 400
    # Auto-generate ID if not provided
    if not data.get("contact_id"):
        data["contact_id"] = "C" + str(uuid.uuid4())[:6].upper()
    # Check duplicate ID
    existing_ids = {c.contact_id for c in book.contacts}
    if data["contact_id"] in existing_ids:
        return jsonify({"error": f"contact_id {data['contact_id']} already exists"}), 409
    contact = Contact.from_dict(data)
    book.contacts.append(contact)
    _save_to_file(book)
    return jsonify(contact.to_dict()), 201


@app.route("/api/contacts/<contact_id>", methods=["GET"])
def get_contact(contact_id):
    """GET /api/contacts/<id> — Get a single contact by ID."""
    book = _load_from_file()
    for c in book.contacts:
        if c.contact_id == contact_id:
            return jsonify(c.to_dict())
    return jsonify({"error": f"Contact {contact_id} not found"}), 404


@app.route("/api/contacts/<contact_id>", methods=["PUT"])
def update_contact(contact_id):
    """PUT /api/contacts/<id> — Update an existing contact."""
    book = _load_from_file()
    data = request.get_json(force=True)
    for c in book.contacts:
        if c.contact_id == contact_id:
            c.name     = data.get("name",     c.name).strip()
            c.phone    = data.get("phone",    c.phone).strip()
            c.email    = data.get("email",    c.email).strip()
            c.city     = data.get("city",     c.city).strip()
            c.birthday = data.get("birthday", c.birthday).strip()
            _save_to_file(book)
            return jsonify(c.to_dict())
    return jsonify({"error": f"Contact {contact_id} not found"}), 404


@app.route("/api/contacts/<contact_id>", methods=["DELETE"])
def delete_contact(contact_id):
    """DELETE /api/contacts/<id> — Remove a contact."""
    book = _load_from_file()
    before = len(book.contacts)
    book.contacts = [c for c in book.contacts if c.contact_id != contact_id]
    if len(book.contacts) == before:
        return jsonify({"error": f"Contact {contact_id} not found"}), 404
    _save_to_file(book)
    return jsonify({"deleted": contact_id})


# ── Advanced Logic Routes ────────────────────────────────────

@app.route("/api/stats", methods=["GET"])
def get_stats():
    """GET /api/stats — Return aggregate statistics (Day 28)."""
    book = _load_from_file()
    return jsonify(stats(book))


@app.route("/api/group-by-city", methods=["GET"])
def get_group_by_city():
    """GET /api/group-by-city — Group all contacts by city (Day 27/28)."""
    book = _load_from_file()
    return jsonify(group_by_city(book))


@app.route("/api/birthdays", methods=["GET"])
def get_birthdays():
    """GET /api/birthdays?days=7 — Contacts with upcoming birthdays (Day 27/28)."""
    book = _load_from_file()
    days = int(request.args.get("days", 7))
    results = birthday_reminder(book, days_ahead=days)
    return jsonify([c.to_dict() for c in results])


@app.route("/api/duplicates", methods=["GET"])
def get_duplicates():
    """GET /api/duplicates — Contacts sharing a phone number (Day 27)."""
    book = _load_from_file()
    dups = find_duplicates(book)
    return jsonify([c.to_dict() for c in dups])


# ── CSV Import / Export ──────────────────────────────────────

@app.route("/api/export/csv", methods=["GET"])
def export_csv():
    """GET /api/export/csv — Download all contacts as a CSV file."""
    book = _load_from_file()
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=Contact.FIELDNAMES)
    writer.writeheader()
    for c in book.contacts:
        writer.writerow(c.to_dict())
    response = Response(output.getvalue(), mimetype="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=contacts.csv"
    return response


@app.route("/api/import/csv", methods=["POST"])
def import_csv():
    """POST /api/import/csv — Upload a CSV file to add contacts."""
    book = _load_from_file()
    file = request.files.get("file")
    if not file:
        return jsonify({"error": "No file uploaded"}), 400
    content = file.read().decode("utf-8-sig")  # Handle BOM
    reader = csv.DictReader(io.StringIO(content))
    existing_ids = {c.contact_id for c in book.contacts}
    added = 0
    for row in reader:
        if not row.get("contact_id") or not row.get("name") or not row.get("phone"):
            continue
        if row["contact_id"] not in existing_ids:
            book.contacts.append(Contact.from_dict(row))
            existing_ids.add(row["contact_id"])
            added += 1
    _save_to_file(book)
    return jsonify({"imported": added, "total": len(book.contacts)})


# ── JSON Import / Export ─────────────────────────────────────

@app.route("/api/export/json", methods=["GET"])
def export_json():
    """GET /api/export/json — Download all contacts as a JSON file."""
    book = _load_from_file()
    data = json.dumps([c.to_dict() for c in book.contacts], indent=2, ensure_ascii=False)
    response = Response(data, mimetype="application/json")
    response.headers["Content-Disposition"] = "attachment; filename=contacts.json"
    return response


@app.route("/api/import/json", methods=["POST"])
def import_json_contacts():
    """POST /api/import/json — Upload a JSON file to add contacts."""
    book = _load_from_file()
    file = request.files.get("file")
    if not file:
        return jsonify({"error": "No file uploaded"}), 400
    try:
        data = json.loads(file.read().decode("utf-8"))
    except json.JSONDecodeError:
        return jsonify({"error": "Invalid JSON file"}), 400
    other_book = ContactBook()
    other_book.contacts = [Contact.from_dict(d) for d in data]
    added = merge_contacts(book, other_book)
    _save_to_file(book)
    return jsonify({"imported": added, "total": len(book.contacts)})


# ── Seed sample data ─────────────────────────────────────────

@app.route("/api/seed", methods=["POST"])
def seed_data():
    """POST /api/seed — Load sample contacts (for demo/testing)."""
    book = ContactBook()
    from datetime import date, timedelta
    today = date.today()
    book.contacts = [
        Contact("C001", "Tony Stark",       "9876543210", "tony@stark.com",     "New York",   "1970-05-29"),
        Contact("C002", "Peter Parker",     "9123456780", "peter@bugle.com",    "Queens",     "2001-08-10"),
        Contact("C003", "Bruce Banner",     "9988776655", "banner@shield.com",  "Dayton",     "1969-12-18"),
        Contact("C004", "Natasha Romanoff", "9111222333", "nat@shield.com",     "New York",   "1984-11-22"),
        Contact("C005", "Clint Barton",     "9911223344", "clint@shield.com",   "Waverly",    "1971-01-07"),
        Contact("C006", "Thor Odinson",     "9000000001", "thor@asgard.com",    "Asgard",     "0964-11-04"),
        Contact("C007", "Wanda Maximoff",   "9000000002", "wanda@hex.com",      "Westview",   "1989-02-10"),
        Contact("C008", "Sam Wilson",       "9055544433", "sam@shield.com",     "New York",   "1978-09-23"),
        Contact("C009", "Steve Rogers",     "9012345678", "steve@shield.com",   "Brooklyn",   "1918-07-04"),
        Contact("C010", "Nick Fury",        "9000000099", "fury@shield.com",    "Washington", "1965-03-12"),
        # Upcoming birthday in next 7 days (seeded dynamically)
        Contact("C011", "Carol Danvers",    "9111000001", "carol@marvel.com",   "Los Angeles",
                (today + timedelta(days=3)).strftime("%Y-%m-%d")),
        Contact("C012", "Scott Lang",       "9222000002", "scott@pym.com",      "San Francisco",
                (today + timedelta(days=1)).strftime("%Y-%m-%d")),
    ]
    _save_to_file(book)
    return jsonify({"seeded": len(book.contacts)})


# ── Health Check ─────────────────────────────────────────────

@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "project": "Contact Book", "day": 28})


if __name__ == "__main__":
    print("🚀 Project 7: Contact Book API")
    print("   Endpoints:")
    print("   GET    /api/contacts         — list / search contacts")
    print("   POST   /api/contacts         — add a contact")
    print("   PUT    /api/contacts/<id>    — update a contact")
    print("   DELETE /api/contacts/<id>    — delete a contact")
    print("   GET    /api/stats            — statistics dashboard")
    print("   GET    /api/group-by-city    — contacts grouped by city")
    print("   GET    /api/birthdays?days=7 — upcoming birthday reminders")
    print("   GET    /api/duplicates       — find duplicate phone numbers")
    print("   GET    /api/export/csv       — export contacts as CSV")
    print("   POST   /api/import/csv       — import contacts from CSV")
    print("   GET    /api/export/json      — export contacts as JSON")
    print("   POST   /api/import/json      — import contacts from JSON")
    print("   POST   /api/seed             — load sample data")
    print()
    app.run(debug=True, port=5007)
