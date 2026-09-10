import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Day 23 Practice — File I/O
# Project 6: Diary / Notes App (Part 3: Persistence)
# Topic: Reading/writing JSON files, text files, FileNotFoundError
# Goal: Build save_to_file(), load_from_file(), search_notes()
#
# HINT LEVEL: 95%  (pattern: -5% every 3 projects)

import json
import os
import time


# ============================================================
# NOTE & NOTESMANAGER (carried forward from Days 21-22)
# ============================================================

class Note:
    VALID_FIELDS = {"title", "content", "tag", "pinned"}

    def __init__(self, note_id, title, content="", tag="general", pinned=False):
        self.note_id = note_id
        self.title   = title
        self.content = content
        self.tag     = tag
        self.pinned  = pinned

    def to_dict(self):
        return {
            "note_id": self.note_id, "title": self.title,
            "content": self.content, "tag": self.tag, "pinned": self.pinned
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data["note_id"], data["title"],
                   data["content"], data["tag"], data["pinned"])

    def __str__(self):
        pin = "📌" if self.pinned else "  "
        return f"{pin} [{self.note_id}] {self.title!r}  tag={self.tag}"

    def __repr__(self):
        return f'Note(note_id="{self.note_id}", title="{self.title}", tag="{self.tag}")'


class NotesManager:
    def __init__(self):
        self.notes = []

    def _raw_add(self, note_id, title, content="", tag="general", pinned=False):
        note = Note(note_id, title, content, tag, pinned)
        self.notes.append(note)
        return note


# ============================================================
# EXCEPTION HIERARCHY (carried forward from Day 22)
# ============================================================

class NotesAppError(Exception): pass
class NoteNotFoundError(NotesAppError): pass
class DuplicateNoteError(NotesAppError): pass
class InvalidFieldError(NotesAppError): pass


# ============================================================
# TASK 1: save_to_file(manager, filepath)
# ============================================================
# Save all notes in manager.notes to a JSON file.
#
# Requirements:
# - Convert each note to a dict using note.to_dict()
# - Write the list of dicts to filepath using json.dump()
# - Use indent=2 for pretty printing
# - Always use encoding="utf-8"
# - Print a confirmation: f"💾 Saved {len(data)} notes to '{filepath}'"
#
# Hint:
#   data = [note.to_dict() for note in manager.notes]
#   with open(filepath, "w", encoding="utf-8") as f:
#       json.dump(data, f, indent=2)

def save_to_file(manager, filepath):
    # YOUR CODE HERE
    notes_list=[]
    for no in manager.notes:
        notes_list.append(no.to_dict())
    with open(filepath,'w',encoding="utf-8") as f:
        json.dump(notes_list,f,indent=2)



# ============================================================
# TASK 2: load_from_file(manager, filepath)
# ============================================================
# Load notes from a JSON file into manager.notes.
#
# Requirements:
# - Use try/except to handle FileNotFoundError
# - If file not found: raise NoteNotFoundError(f"File '{filepath}' does not exist")
# - If found: read with json.load(), then rebuild each note using Note.from_dict()
# - Replace manager.notes entirely with the loaded notes
# - Print: f"📂 Loaded {len(manager.notes)} notes from '{filepath}'"
#
# Hint:
#   try:
#       with open(filepath, "r", encoding="utf-8") as f:
#           data = json.load(f)
#       manager.notes = [Note.from_dict(d) for d in data]
#   except FileNotFoundError:
#       raise NoteNotFoundError(...)

def load_from_file(manager, filepath):
    # YOUR CODE HERE
    try:
        with open(filepath,'r',encoding="utf-8") as f :
            data=json.load(f)
            manager.notes=[Note.from_dict(d) for d in data]
            print(f"📂 Loaded {len(manager.notes)} notes from '{filepath}'")
    except FileNotFoundError:
        raise NoteNotFoundError(f"File '{filepath}' does not exist")


# ============================================================
# TASK 3: search_notes(manager, keyword)
# ============================================================
# Search notes where keyword appears in title OR content.
#
# Requirements:
# - Search is CASE-INSENSITIVE (use .lower() on both sides)
# - Returns a list of matching Note objects (can be empty list [])
# - Do NOT raise an error if nothing is found — just return []
#
# Hint:
#   keyword_lower = keyword.lower()
#   return [
#       note for note in manager.notes
#       if keyword_lower in note.title.lower()
#       or keyword_lower in note.content.lower()
#   ]

def search_notes(manager, keyword):
    # YOUR CODE HERE
    keyword_lower=keyword.lower()
    return [note for note in manager.notes if keyword_lower in note.title.lower() or keyword_lower in note.content.lower()]


# ============================================================
# TEST YOUR CODE — run: python practice.py
# ============================================================

if __name__ == "__main__":

    SAVE_PATH = "test_notes.json"   # temp file for testing

    # ── Test 1: save_to_file ──────────────────────────────────
    print("=== Test 1: save_to_file ===")
    mgr = NotesManager()
    mgr._raw_add("N001", "Buy groceries", content="milk, eggs, bread", tag="personal")
    mgr._raw_add("N002", "Sprint planning", content="review backlog items", tag="work", pinned=True)
    mgr._raw_add("N003", "Python notes", content="file io is useful", tag="study")

    save_to_file(mgr, SAVE_PATH)
    assert os.path.exists(SAVE_PATH), "File should exist after save"
    print(f"  File size: {os.path.getsize(SAVE_PATH)} bytes")
    print("  PASSED\n")


    # ── Test 2: load_from_file ────────────────────────────────
    print("=== Test 2: load_from_file ===")
    mgr2 = NotesManager()
    load_from_file(mgr2, SAVE_PATH)
    assert len(mgr2.notes) == 3, f"Should have 3 notes, got {len(mgr2.notes)}"
    assert mgr2.notes[0].note_id == "N001", "First note should be N001"
    assert mgr2.notes[1].pinned is True, "N002 should be pinned"
    for note in mgr2.notes:
        print(f"  Loaded: {note}")
    print("  PASSED\n")


    # ── Test 3: load_from_file — missing file ─────────────────
    print("=== Test 3: load_from_file (missing file) ===")
    try:
        load_from_file(mgr2, "ghost_file.json")
        print("  FAILED — should have raised NoteNotFoundError")
    except NoteNotFoundError as e:
        print(f"  NoteNotFoundError raised correctly: {e}")
    print("  PASSED\n")


    # ── Test 4: search_notes ──────────────────────────────────
    print("=== Test 4: search_notes ===")
    results = search_notes(mgr2, "python")         # case-insensitive
    assert len(results) == 1, f"Should find 1 result, got {len(results)}"
    assert results[0].note_id == "N003"
    print(f"  Found: {results[0]}")

    results2 = search_notes(mgr2, "review")         # appears in content
    assert len(results2) == 1
    assert results2[0].note_id == "N002"
    print(f"  Found: {results2[0]}")

    results3 = search_notes(mgr2, "MILK")           # uppercase search
    assert len(results3) == 1
    assert results3[0].note_id == "N001"
    print(f"  Found: {results3[0]}")

    results4 = search_notes(mgr2, "zzznomatch")     # no match
    assert results4 == [], f"Should return empty list, got {results4}"
    print(f"  No match returned [] — correct")
    print("  PASSED\n")


    # ── Test 5: Round-trip integrity ──────────────────────────
    print("=== Test 5: Round-trip integrity ===")
    # Save mgr2, load into mgr3, compare
    save_to_file(mgr2, SAVE_PATH)
    mgr3 = NotesManager()
    load_from_file(mgr3, SAVE_PATH)
    assert len(mgr3.notes) == len(mgr2.notes), "Note count must match"
    for orig, loaded in zip(mgr2.notes, mgr3.notes):
        assert orig.note_id  == loaded.note_id,  "note_id must match"
        assert orig.title    == loaded.title,    "title must match"
        assert orig.content  == loaded.content,  "content must match"
        assert orig.tag      == loaded.tag,      "tag must match"
        assert orig.pinned   == loaded.pinned,   "pinned must match"
    print("  All fields match after save → load round-trip")
    print("  PASSED\n")


    # Cleanup test file
    if os.path.exists(SAVE_PATH):
        os.remove(SAVE_PATH)

    print("Day 23 — All tests passed! 🎉")
