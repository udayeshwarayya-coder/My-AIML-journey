import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Day 22 Practice — Custom Exceptions & `finally`
# Project 6: Diary / Notes App (Part 2: Robust Error Handling)
# Topic: Custom Exception classes, raise, try/except/else/finally, exception chaining
# Goal: Build NoteNotFoundError, DuplicateNoteError, InvalidFieldError,
#       delete_note(), update_note(), safe_add_note()
#
# HINT LEVEL: 95%  (same as Day 21 — pattern: -5% every 3 projects)

import time
import json
import os


# ============================================================
# NOTE & NOTESMANAGER (carried forward from Day 21)
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
        return f'Note(note_id="{self.note_id}", title="{self.title}", tag="{self.tag}", pinned={self.pinned})'


class NotesManager:
    def __init__(self):
        self.notes = []

    def _raw_add(self, note_id, title, content="", tag="general", pinned=False):
        """Internal add — no duplicate check (used in tests for setup)."""
        note = Note(note_id, title, content, tag, pinned)
        self.notes.append(note)
        return note


# ============================================================
# TASK 1: Custom Exception Hierarchy
# ============================================================
# Create a small exception hierarchy for the Notes App.
#
# Requirements:
# - NotesAppError(Exception)      — base class, docstring required
# - NoteNotFoundError(NotesAppError)  — when note_id is not found
# - DuplicateNoteError(NotesAppError) — when note_id already exists
# - InvalidFieldError(NotesAppError)  — when an invalid field is passed to update
#
# All classes need only: class body with a docstring and `pass`

# YOUR CODE HERE
class NotesAppError(Exception):pass
class NoteNotFoundError(NotesAppError):pass
class DuplicateNoteError(NotesAppError):pass
class InvalidFieldError(NotesAppError):pass

# ============================================================
# TASK 2: Helper — find_note(manager, note_id)
# ============================================================
# Search manager.notes for a note whose .note_id == note_id.
# If found, return it.
# If not found, raise NoteNotFoundError with a descriptive message.

def find_note(manager, note_id):
    # YOUR CODE HERE
    for note in manager.notes:
        if note.note_id==note_id:
            return note
    raise NoteNotFoundError(f"noteid {note_id} not found ")



# ============================================================
# TASK 3: delete_note(manager, note_id)
# ============================================================
# Safely delete a note by ID with a guaranteed audit log.
#
# Requirements:
# - Use try / finally
# - In try:  call find_note() to get the note, then manager.notes.remove(note)
#            return the deleted note
# - In finally: ALWAYS print an audit message like:
#               f"🗑️  Audit: delete_note('{note_id}') was called"
# - If NoteNotFoundError propagates out, that is fine — do NOT suppress it here

def delete_note(manager, note_id):
    # YOUR CODE HERE
    try:
        note=find_note(manager,note_id)
        manager.notes.remove(note)
        return note
    finally:
        print(f"🗑️  Audit: delete_note('{note_id}') was called")


# ============================================================
# TASK 4: update_note(manager, note_id, **kwargs)
# ============================================================
# Update one or more fields of an existing note.
#
# Requirements:
# - Call find_note() — let NoteNotFoundError propagate if missing
# - VALID_FIELDS = {"title", "content", "tag", "pinned"}  (already on Note class)
# - For each key in kwargs:
#     - If key NOT in Note.VALID_FIELDS: raise InvalidFieldError(f"'{key}' is not a valid note field")
#     - Otherwise: setattr(note, key, value)
# - Return the updated note
# - Use try/except/else/finally:
#     try: find note + validate + update fields
#     except InvalidFieldError: re-raise (do not suppress)
#     else: print(f"✅ Note '{note_id}' updated: {list(kwargs.keys())}")
#     finally: print(f"📋 Audit: update_note('{note_id}') was called")

def update_note(manager, note_id, **kwargs):
    # YOUR CODE HERE
    try:
        note=find_note(manager,note_id)
        for key,valvue in kwargs.items():
            if key not in Note.VALID_FIELDS:
                raise InvalidFieldError(f"'{key}' is not a valid note field")
            else:
                setattr(note,key,valvue)
        
    except InvalidFieldError:
        raise
    else:
        print(f"✅ Note '{note_id}' updated: {list(kwargs.keys())}")
        return note
    finally:
        print(f"📋 Audit: update_note('{note_id}') was called")

# ============================================================
# TASK 5: safe_add_note(manager, note_id, title, **kwargs)
# ============================================================
# Add a new note, but raise DuplicateNoteError if note_id already exists.
#
# Requirements:
# - Check if any note in manager.notes already has .note_id == note_id
# - If yes: raise DuplicateNoteError(f"Note '{note_id}' already exists")
# - If no: create and append the new Note, return it
# - Hint: use manager._raw_add(note_id, title, **kwargs) internally

# ✅ Fix — scan ALL notes first, then add
def safe_add_note(manager, note_id, title, **kwargs):
    for note in manager.notes:
        if note.note_id == note_id:
            raise DuplicateNoteError(f"Note '{note_id}' already exists")
    return manager._raw_add(note_id, title, **kwargs)



# ============================================================
# TEST YOUR CODE — run: python practice.py
# ============================================================

if __name__ == "__main__":

    # ── Test 1: Exception Hierarchy ───────────────────────────
    print("=== Test 1: Exception Hierarchy ===")
    assert issubclass(NoteNotFoundError, NotesAppError), "NoteNotFoundError must inherit NotesAppError"
    assert issubclass(DuplicateNoteError, NotesAppError), "DuplicateNoteError must inherit NotesAppError"
    assert issubclass(InvalidFieldError, NotesAppError), "InvalidFieldError must inherit NotesAppError"
    assert issubclass(NotesAppError, Exception), "NotesAppError must inherit Exception"
    print("  Hierarchy correct — PASSED\n")


    # ── Test 2: find_note ──────────────────────────────────────
    print("=== Test 2: find_note ===")
    mgr = NotesManager()
    mgr._raw_add("N001", "Buy groceries", tag="personal")
    mgr._raw_add("N002", "Sprint planning", tag="work", pinned=True)

    found = find_note(mgr, "N001")
    assert found.title == "Buy groceries", "Should find N001"
    print(f"  Found: {found}")

    try:
        find_note(mgr, "N999")
        print("  FAILED — should have raised NoteNotFoundError")
    except NoteNotFoundError as e:
        print(f"  NoteNotFoundError raised correctly: {e}")
    print("  PASSED\n")


    # ── Test 3: delete_note ────────────────────────────────────
    print("=== Test 3: delete_note ===")
    deleted = delete_note(mgr, "N001")
    assert deleted.note_id == "N001", "Should return deleted note"
    assert len(mgr.notes) == 1, f"Should have 1 note left, got {len(mgr.notes)}"
    print(f"  Deleted: {deleted}")

    try:
        delete_note(mgr, "N001")   # Already deleted
        print("  FAILED — should have raised NoteNotFoundError")
    except NoteNotFoundError as e:
        print(f"  NoteNotFoundError raised correctly: {e}")
    print("  PASSED\n")


    # ── Test 4: update_note ────────────────────────────────────
    print("=== Test 4: update_note ===")
    updated = update_note(mgr, "N002", title="Sprint Review", pinned=False)
    assert updated.title == "Sprint Review", "Title should be updated"
    assert updated.pinned is False, "Pinned should be updated"
    print(f"  Updated: {updated}")

    try:
        update_note(mgr, "N002", colour="red")   # Invalid field
        print("  FAILED — should have raised InvalidFieldError")
    except InvalidFieldError as e:
        print(f"  InvalidFieldError raised correctly: {e}")

    try:
        update_note(mgr, "N999", title="Ghost")  # Non-existent ID
        print("  FAILED — should have raised NoteNotFoundError")
    except NoteNotFoundError as e:
        print(f"  NoteNotFoundError raised correctly: {e}")
    print("  PASSED\n")


    # ── Test 5: safe_add_note ──────────────────────────────────
    print("=== Test 5: safe_add_note ===")
    new_note = safe_add_note(mgr, "N003", "Book ideas", content="Sci-fi story", tag="creative")
    assert new_note.note_id == "N003", "New note should have correct ID"
    assert len(mgr.notes) == 2, f"Should have 2 notes, got {len(mgr.notes)}"
    print(f"  Added: {new_note}")

    try:
        safe_add_note(mgr, "N003", "Duplicate!")  # Already exists
        print("  FAILED — should have raised DuplicateNoteError")
    except DuplicateNoteError as e:
        print(f"  DuplicateNoteError raised correctly: {e}")
    print("  PASSED\n")

    print("Day 22 — All tests passed! 🎉")
