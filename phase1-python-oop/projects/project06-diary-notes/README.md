# Project 6: Chronicle — Diary, Notes & Task Manager 📔

A modern, responsive Diary, Notes, and Task Journal application combining **Python OOP, Exception Handling, File I/O persistence, and Text Analytics** with an ultra-sleek web UI.

---

## 🚀 Features

- **Full Notes & Diary Management**: Create, edit, delete, pin to top, and categorize.
- **Checklist / Todo Integration**: Type `[ ] Task item` and `[x] Completed item` for interactive task lists inside notes.
- **Live Search & Filter**: Real-time case-insensitive search by title, content, or `#tag`.
- **Day 24 Text Analytics (`word_count`)**: Real-time word count, character count, and estimated reading time.
- **Day 24 Tag Grouping (`tag_notes`)**: Automatic categorization and filtering by `#work`, `#study`, `#todo`, `#diary`, `#ideas`.
- **Day 24 Multi-Format Export (`export_all`)**: One-click download as **JSON**, **Markdown (.md)**, or **Plain Text (.txt)**.
- **Hybrid Storage & Sync**: Runs in offline LocalStorage mode immediately, and automatically syncs with Flask when backend is running on `http://localhost:5000`.

---

## 📂 Project Structure

```
project06-diary-notes/
├── backend/
│   ├── app.py           # Flask REST API backend (you write this!)
│   └── notes_data.json  # Saved notes database
├── frontend/
│   └── index.html       # Chronicle Web App (Vanilla HTML/CSS/JS)
└── README.md
```

---

## 🛠️ How to Run the Website

### Step 1: Open Frontend
Simply open `frontend/index.html` in your browser (double-click the file or use Live Server in VS Code).
It works instantly in LocalStorage mode with sample seed notes!

### Step 2: Write & Run the Flask Backend
1. Go to `backend/` directory:
   ```bash
   cd phase1-python-oop/projects/project06-diary-notes/backend
   ```
2. Install dependencies:
   ```bash
   pip install flask flask-cors
   ```
3. Create your `app.py` implementing the REST API endpoints:
   - `GET  /api/notes` — Return list of notes
   - `POST /api/notes` — Create note
   - `PUT  /api/notes/<id>` — Update note
   - `DELETE /api/notes/<id>` — Delete note
   - `GET  /api/notes/tags` — Group notes by tag (`tag_notes`)
   - `GET  /api/notes/stats` — Metrics and word count (`word_count`)
4. Run your backend:
   ```bash
   python app.py
   ```
5. Refresh `frontend/index.html` — the status indicator in the sidebar turns **🟢 Backend: Connected (Flask)**!
