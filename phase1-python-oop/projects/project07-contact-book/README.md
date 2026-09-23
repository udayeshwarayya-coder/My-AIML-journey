# Project 7: Contact Book Pro

> **Phase 1 Capstone** — Days 25–28 | Python OOP + File I/O + Flask + Vanilla JS

---

## 🚀 What It Does

A full-stack contact management application built entirely with Python backend logic from Days 25–28:

| Feature | Python Functions Used |
|---|---|
| Add / Edit / Delete contacts | `Contact` class, `ContactBook` class |
| Search contacts | list comprehension, str methods |
| Group by City | `group_by_city()` |
| Birthday Reminders | `birthday_reminder()` |
| Statistics Dashboard | `stats()` |
| Find Duplicate Phones | `find_duplicates()` |
| CSV Import / Export | `csv.DictWriter`, `csv.DictReader` |
| JSON Import / Export | `json.dump`, `json.load`, `merge_contacts()` |

---

## 🛠️ Setup & Run

```bash
# 1. Install dependencies
pip install flask flask-cors

# 2. Start the backend
cd "d:/python next/phase1-python-oop/projects/project07-contact-book/backend"
python app.py

# 3. Open the frontend
# Open project07-contact-book/frontend/index.html in your browser
# (or use VS Code Live Server)
```

Backend runs on: **http://localhost:5007**

---

## 📁 File Structure

```
project07-contact-book/
├── backend/
│   ├── app.py              ← Flask API (all 12 logic functions as endpoints)
│   └── contacts_data.json  ← Auto-created data file
└── frontend/
    └── index.html          ← Premium dark-mode UI
```

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/contacts` | List / search contacts |
| POST | `/api/contacts` | Add a contact |
| PUT | `/api/contacts/<id>` | Update a contact |
| DELETE | `/api/contacts/<id>` | Delete a contact |
| GET | `/api/stats` | Statistics dashboard |
| GET | `/api/group-by-city` | Contacts grouped by city |
| GET | `/api/birthdays?days=7` | Upcoming birthday reminders |
| GET | `/api/duplicates` | Find duplicate phone numbers |
| GET | `/api/export/csv` | Download contacts.csv |
| POST | `/api/import/csv` | Upload CSV file |
| GET | `/api/export/json` | Download contacts.json |
| POST | `/api/import/json` | Upload JSON file |
| POST | `/api/seed` | Load sample Marvel contacts |

---

## 🐍 Phase 1 Concepts Revisited

- **Day 1–4:** `class`, `__init__`, `self`, objects
- **Day 5–8:** Inheritance, `@classmethod`, `@property`
- **Day 13–16:** `__str__`, `__repr__`, magic methods
- **Day 21–22:** Exception handling, custom exceptions
- **Day 25:** `csv.DictReader`, `csv.DictWriter`
- **Day 26:** `json.dump`, `json.load`
- **Day 27:** `merge_contacts`, `group_by_city`, `birthday_reminder`, `find_duplicates`
- **Day 28:** `stats()`, `group_by_city_summary()`, `export_and_reload()`
