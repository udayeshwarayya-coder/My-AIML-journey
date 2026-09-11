# Project 6: Chronicle — Diary, Notes & Task Journal Backend API
# Built for Phase 1 Python OOP Milestone (Days 21–24)
# Concepts covered:
# - Day 21: Exception Handling (try...except, input validation)
# - Day 22: Custom Exceptions (NoteNotFoundError, DuplicateNoteError, etc.)
# - Day 23: File I/O Persistence (JSON load/save, search)
# - Day 24: Text Analytics (word_count, tag_notes, export_all)
#
# Run:
#   cd "d:/python next/phase1-python-oop/projects/project06-diary-notes/backend"
#   python app.py

import os
import json
from datetime import datetime
from flask import Flask, jsonify, request, send_file, Response
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing for frontend

DATA_FILE = os.path.join(os.path.dirname(__file__), "notes_data.json")


# ============================================================
# CUSTOM EXCEPTIONS (Day 22)
# ============================================================

class NotesAppError(Exception):
    """Base exception for Chronicle notes app."""
    pass

class NoteNotFoundError(NotesAppError):
    """Raised when a note ID does not exist."""
    pass

class DuplicateNoteError(NotesAppError):
    """Raised when creating a note with an already existing ID."""
    pass

class InvalidFieldError(NotesAppError):
    """Raised when invalid field or empty title is provided."""
    pass


# ============================================================
# NOTE MODEL (Days 21–24)
# ============================================================

class Note:
    VALID_FIELDS = {"note_id", "title", "content", "tag", "pinned", "created_at"}

    def __init__(self, note_id: str, title: str, content: str = "", tag: str = "general", pinned: bool = False, created_at: str = None):
        if not title or not title.strip():
            raise InvalidFieldError("Note title cannot be empty.")

        self.note_id = str(note_id).strip()
        self.title = title.strip()
        self.content = content or ""
        self.tag = (tag or "general").strip().lower()
        self.pinned = bool(pinned)
        self.created_at = created_at or datetime.now().isoformat()

    def to_dict(self) -> dict:
        return {
            "note_id": self.note_id,
            "title": self.title,
            "content": self.content,
            "tag": self.tag,
            "pinned": self.pinned,
            "created_at": self.created_at
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            note_id=data.get("note_id", ""),
            title=data.get("title", ""),
            content=data.get("content", ""),
            tag=data.get("tag", "general"),
            pinned=data.get("pinned", False),
            created_at=data.get("created_at")
        )

    def __str__(self):
        pin = "📌" if self.pinned else "  "
        return f"{pin} [{self.note_id}] {self.title!r}  tag=#{self.tag}"

    def __repr__(self):
        return f'Note(note_id="{self.note_id}", title="{self.title}", tag="{self.tag}")'


# ============================================================
# DAY 24 TEXT ANALYTICS & UTILITIES
# ============================================================

def word_count(text: str) -> dict:
    """
    Day 24 Task 1:
    Analyzes text and returns word count, character count, and estimated reading time.
    """
    if not text:
        return {"words": 0, "chars": 0, "reading_time_min": 0.0}

    words = text.split()
    total_words = len(words)
    total_chars = len(text.replace("\n", ""))
    reading_time = round(total_words / 200, 2) if total_words > 0 else 0.0

    return {
        "words": total_words,
        "chars": total_chars,
        "reading_time_min": reading_time
    }


def tag_notes(manager) -> dict[str, list]:
    """
    Day 24 Task 2:
    Groups notes by lowercase tag.
    """
    grouped = {}
    for note in manager.notes:
        note_key = note.tag.lower()
        if note_key not in grouped:
            grouped[note_key] = []
        grouped[note_key].append(note)
    return grouped


def export_all(manager, filepath: str, format: str = "json") -> int:
    """
    Day 24 Task 3:
    Exports all notes to a file in json, markdown, or txt format.
    """
    fmt = format.lower()
    if fmt == "json":
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump([n.to_dict() for n in manager.notes], f, indent=2)
    elif fmt in ("markdown", "md"):
        with open(filepath, "w", encoding="utf-8") as f:
            for n in manager.notes:
                pin = "📌 " if n.pinned else ""
                f.write(f"# {pin}{n.title}\n**Tag:** #{n.tag} | **ID:** {n.note_id}\n\n{n.content}\n\n---\n\n")
    elif fmt == "txt":
        with open(filepath, "w", encoding="utf-8") as f:
            for n in manager.notes:
                f.write(f"[{n.note_id}] {n.title} (Tag: #{n.tag})\n{n.content}\n" + "=" * 40 + "\n\n")
    else:
        raise ValueError(f"Unsupported format '{format}'. Choose json, markdown, or txt.")
    return len(manager.notes)


# ============================================================
# NOTES MANAGER (Days 21–24 Core OOP)
# ============================================================

class NotesManager:
    def __init__(self):
        self.notes: list[Note] = []

    def add_note(self, note_id: str, title: str, content: str = "", tag: str = "general", pinned: bool = False, created_at: str = None) -> Note:
        """Adds a new note with validation and duplicate prevention."""
        if any(n.note_id == note_id for n in self.notes):
            raise DuplicateNoteError(f"Note with ID '{note_id}' already exists.")

        note = Note(note_id, title, content, tag, pinned, created_at)
        self.notes.append(note)
        return note

    def get_note(self, note_id: str) -> Note:
        """Finds a note by note_id or raises NoteNotFoundError."""
        for note in self.notes:
            if note.note_id == note_id:
                return note
        raise NoteNotFoundError(f"Note '{note_id}' was not found.")

    def update_note(self, note_id: str, **kwargs) -> Note:
        """Updates note fields with validation."""
        note = self.get_note(note_id)

        for key, value in kwargs.items():
            if key not in Note.VALID_FIELDS:
                raise InvalidFieldError(f"Invalid field: '{key}'.")
            if key == "title":
                if not value or not str(value).strip():
                    raise InvalidFieldError("Title cannot be empty.")
                note.title = str(value).strip()
            elif key == "content":
                note.content = str(value)
            elif key == "tag":
                note.tag = str(value).strip().lower()
            elif key == "pinned":
                note.pinned = bool(value)

        return note

    def delete_note(self, note_id: str) -> Note:
        """Deletes a note by note_id."""
        note = self.get_note(note_id)
        self.notes.remove(note)
        return note

    def search_notes(self, query: str) -> list[Note]:
        """Day 23: Case-insensitive search across title, content, and tag."""
        if not query or not query.strip():
            return self.notes

        q = query.strip().lower()
        return [
            n for n in self.notes
            if q in n.title.lower() or q in n.content.lower() or q in n.tag.lower()
        ]

    def save_to_file(self, filepath: str = DATA_FILE):
        """Day 23: Save notes database to JSON file."""
        data = [n.to_dict() for n in self.notes]
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def load_from_file(self, filepath: str = DATA_FILE):
        """Day 23: Load notes database from JSON file with error handling."""
        if not os.path.exists(filepath):
            self.seed_defaults()
            self.save_to_file(filepath)
            return

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.notes = [Note.from_dict(item) for item in data]
        except (json.JSONDecodeError, FileNotFoundError):
            self.seed_defaults()
            self.save_to_file(filepath)

    def seed_defaults(self):
        """Seeds initial default notes if data file is missing."""
        self.notes = [
            Note("N001", "Phase 1 Python OOP Milestone",
                 "Completed Days 1 to 24 of the 300-day roadmap!\nCovered:\n[x] Magic methods (__str__, __repr__)\n[x] Custom Exceptions (try...except)\n[x] File I/O & JSON persistence\n[x] Build Project 6 Website & Backend",
                 "study", pinned=True),
            Note("N002", "Sprint Planning & Task Checklist",
                 "[x] Check Day 23 practice tests\n[x] Formulate Day 24 text analytics tasks\n[x] Write Flask backend endpoints for Project 6\n[x] Connect frontend with CORS enabled",
                 "todo", pinned=True),
            Note("N003", "Diary: Reflections on Machine Learning Journey",
                 "Building full projects with both Python OOP logic and visual frontends gives true mastery. Excited to dive into Phase 2 NumPy and Data Manipulation soon.",
                 "diary", pinned=False),
            Note("N004", "Grocery & Meal Prep List",
                 "[ ] Greek yogurt\n[x] Almond milk\n[ ] Espresso roast coffee beans\n[x] Fresh spinach",
                 "personal", pinned=False),
        ]


# Initialize manager & load persistent notes
manager = NotesManager()
manager.load_from_file(DATA_FILE)


# ============================================================
# FLASK REST API ENDPOINTS
# ============================================================

@app.route("/api/notes", methods=["GET"])
def get_notes():
    """
    GET /api/notes
    Query params:
      - q: search query string
      - tag: tag filter
    """
    q = request.args.get("q", "").strip()
    tag = request.args.get("tag", "").strip().lower()

    results = manager.notes
    if q:
        results = manager.search_notes(q)
    if tag:
        results = [n for n in results if n.tag == tag]

    # Sort: pinned first, then newest first
    sorted_notes = sorted(
        results,
        key=lambda n: (not n.pinned, n.created_at),
        reverse=False
    )
    # pinned notes first (not n.pinned = False comes before True)
    sorted_notes = sorted(results, key=lambda n: (0 if n.pinned else 1, n.created_at), reverse=False)

    return jsonify([n.to_dict() for n in sorted_notes])


@app.route("/api/notes", methods=["POST"])
def create_note():
    """
    POST /api/notes
    Body JSON: { note_id, title, content, tag, pinned }
    """
    data = request.get_json(force=True, silent=True)
    if not data:
        return jsonify({"error": "Request body must be valid JSON."}), 400

    note_id = data.get("note_id")
    title = data.get("title")

    if not title:
        return jsonify({"error": "Title is required."}), 400

    # Auto-generate note_id if omitted
    if not note_id:
        existing_nums = [
            int(n.note_id.replace("N", ""))
            for n in manager.notes if n.note_id.startswith("N") and n.note_id[1:].isdigit()
        ]
        next_num = max(existing_nums, default=0) + 1
        note_id = f"N{next_num:03d}"

    try:
        note = manager.add_note(
            note_id=note_id,
            title=title,
            content=data.get("content", ""),
            tag=data.get("tag", "general"),
            pinned=data.get("pinned", False),
            created_at=data.get("created_at")
        )
        manager.save_to_file()
        return jsonify(note.to_dict()), 201
    except DuplicateNoteError as e:
        return jsonify({"error": str(e)}), 409
    except InvalidFieldError as e:
        return jsonify({"error": str(e)}), 400


@app.route("/api/notes/<note_id>", methods=["GET"])
def get_single_note(note_id):
    """GET /api/notes/<note_id>"""
    try:
        note = manager.get_note(note_id)
        stats = word_count(note.content)
        data = note.to_dict()
        data["stats"] = stats
        return jsonify(data)
    except NoteNotFoundError as e:
        return jsonify({"error": str(e)}), 404


@app.route("/api/notes/<note_id>", methods=["PUT"])
def update_single_note(note_id):
    """
    PUT /api/notes/<note_id>
    Body JSON: partial or full fields to update
    """
    data = request.get_json(force=True, silent=True)
    if not data:
        return jsonify({"error": "Request body must be valid JSON."}), 400

    try:
        note = manager.update_note(note_id, **data)
        manager.save_to_file()
        return jsonify(note.to_dict())
    except NoteNotFoundError as e:
        return jsonify({"error": str(e)}), 404
    except InvalidFieldError as e:
        return jsonify({"error": str(e)}), 400


@app.route("/api/notes/<note_id>", methods=["DELETE"])
def delete_single_note(note_id):
    """DELETE /api/notes/<note_id>"""
    try:
        note = manager.delete_note(note_id)
        manager.save_to_file()
        return jsonify({"message": f"Note '{note_id}' deleted successfully.", "deleted": note.to_dict()})
    except NoteNotFoundError as e:
        return jsonify({"error": str(e)}), 404


@app.route("/api/notes/tags", methods=["GET"])
def get_tags():
    """
    GET /api/notes/tags
    Uses Day 24 tag_notes() logic to group notes by tag.
    """
    grouped = tag_notes(manager)
    serialized = {
        tag: [n.to_dict() for n in notes_list]
        for tag, notes_list in grouped.items()
    }
    return jsonify(serialized)


@app.route("/api/notes/stats", methods=["GET"])
def get_stats():
    """
    GET /api/notes/stats
    Uses Day 24 word_count() logic across all notes.
    """
    total_notes = len(manager.notes)
    pinned_count = sum(1 for n in manager.notes if n.pinned)

    total_words = 0
    total_chars = 0
    for note in manager.notes:
        wc = word_count(note.content)
        total_words += wc["words"]
        total_chars += wc["chars"]

    reading_time_min = round(total_words / 200, 2) if total_words > 0 else 0.0
    grouped = tag_notes(manager)
    tag_summary = {tag: len(notes) for tag, notes in grouped.items()}

    return jsonify({
        "total_notes": total_notes,
        "pinned_notes": pinned_count,
        "total_words": total_words,
        "total_chars": total_chars,
        "reading_time_min": reading_time_min,
        "tags_count": len(tag_summary),
        "tag_breakdown": tag_summary
    })


@app.route("/api/export", methods=["GET"])
def export_notes():
    """
    GET /api/export?format=json|markdown|txt
    Uses Day 24 export_all() logic to download file.
    """
    fmt = request.args.get("format", "json").lower()
    temp_filename = f"export_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    extension_map = {
        "json": (".json", "application/json"),
        "markdown": (".md", "text/markdown"),
        "md": (".md", "text/markdown"),
        "txt": (".txt", "text/plain")
    }

    if fmt not in extension_map:
        return jsonify({"error": f"Unsupported format '{fmt}'. Choose json, markdown, or txt."}), 400

    ext, mimetype = extension_map[fmt]
    export_path = os.path.join(os.path.dirname(__file__), temp_filename + ext)

    try:
        count = export_all(manager, export_path, format=fmt)
        with open(export_path, "r", encoding="utf-8") as f:
            content = f.read()
        os.remove(export_path)

        return Response(
            content,
            mimetype=mimetype,
            headers={"Content-Disposition": f"attachment;filename=chronicle_notes{ext}"}
        )
    except Exception as e:
        if os.path.exists(export_path):
            os.remove(export_path)
        return jsonify({"error": str(e)}), 500


# ============================================================
# SERVER LAUNCHER
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("🚀 Chronicle Notes API — Flask Backend Running")
    print("📍 URL: http://localhost:5000")
    print("📚 Endpoints:")
    print("   GET    /api/notes         — List & search notes")
    print("   POST   /api/notes         — Create a note")
    print("   GET    /api/notes/<id>    — Get single note")
    print("   PUT    /api/notes/<id>    — Update note")
    print("   DELETE /api/notes/<id>    — Delete note")
    print("   GET    /api/notes/tags    — Grouped by tags")
    print("   GET    /api/notes/stats   — Text & notes metrics")
    print("   GET    /api/export        — Multi-format export")
    print("=" * 60)
    app.run(host="0.0.0.0", port=5000, debug=True)
