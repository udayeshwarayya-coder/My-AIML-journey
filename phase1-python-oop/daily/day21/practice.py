import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Day 21 Practice — Python Context Managers & the `with` Statement
# Project 6: Diary / Notes App (Part 1: Resource Management)
# Topic: __enter__, __exit__, @contextmanager, JSON Persistence
# Goal: Build BlockTimer, suppress_errors, temp_tag, and JSON save/load on NotesManager
#
# HINT LEVEL: 95%  (reduced 5% from baseline — pattern: -5% every 3 projects)
# Hint levels: P1-P3=100% | P4-P6=95% | P7-P9=90% | P10-P12=85% | ...

import time
import json
import os
from contextlib import contextmanager


# ============================================================
# TASK 1: BlockTimer Context Manager (Class-based Protocol)
# ============================================================
# Build a class-based context manager using `__enter__` and `__exit__`.
# It measures the wall-clock time taken by any block of code inside `with`.
#
# Requirements:
# - `__init__(self, label="Block")`: Store label; set self.duration = 0.0
# - `__enter__(self)`:
#     - Record self.start_time = time.time()
#     - Return self
# - `__exit__(self, exc_type, exc_val, exc_tb)`:
#     - Calculate self.duration from start_time
#     - Print the label and duration (format is up to you)
#     - Return False

class BlockTimer:
    def __init__(self, label="Block"):
        # YOUR CODE HERE
        pass

    def __enter__(self):
        # YOUR CODE HERE
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        # YOUR CODE HERE
        pass


# ============================================================
# TASK 2: suppress_errors Context Manager (Exception Handling)
# ============================================================
# Build a context manager that silences specific exception types so the
# program can continue without crashing.
#
# Requirements:
# - `__init__(self, *exceptions)`: Store the exception classes in self.exceptions
# - `__enter__(self)`: Return self
# - `__exit__(self, exc_type, exc_val, exc_tb)`:
#     - If exc_type is not None AND issubclass(exc_type, self.exceptions):
#         - Print the exception type name and value
#         - Return True
#     - Otherwise return False

class suppress_errors:
    def __init__(self, *exceptions):
        # YOUR CODE HERE
        pass

    def __enter__(self):
        # YOUR CODE HERE
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        # YOUR CODE HERE
        pass


# ============================================================
# TASK 3: temp_tag (@contextmanager Generator Function)
# ============================================================
# Write a function-based context manager using `@contextmanager`.
# It temporarily changes a Note's tag for the duration of the `with` block,
# then ALWAYS restores the original tag — even if an exception occurs.
#
# Requirements:
# - Save old_tag = note.tag
# - Set note.tag = new_tag
# - Use try...finally:
#     try: yield note
#     finally: restore note.tag

@contextmanager
def temp_tag(note, new_tag):
    # YOUR CODE HERE
    pass


# ============================================================
# TASK 4: Note Serialization & NotesManager Persistence
# ============================================================
# Complete the Note class serialization methods (`to_dict`, `from_dict`)
# and NotesManager JSON persistence methods (`save_to_json`, `load_from_json`).

class Note:
    def __init__(self, note_id, title, content="", tag="general", pinned=False):
        self.note_id = note_id
        self.title   = title
        self.content = content
        self.tag     = tag
        self.pinned  = pinned

    def to_dict(self):
        """Returns a dict with all 5 fields: note_id, title, content, tag, pinned."""
        # YOUR CODE HERE
        pass

    @classmethod
    def from_dict(cls, data):
        """Creates a Note from a dict."""
        # YOUR CODE HERE
        pass

    def __str__(self):
        pin = "📌" if self.pinned else "  "
        return f"{pin} [{self.note_id}] {self.title!r}  tag={self.tag}"

    def __repr__(self):
        return f'Note(note_id="{self.note_id}", title="{self.title}", tag="{self.tag}", pinned={self.pinned})'


class NotesManager:
    def __init__(self):
        self.notes = []

    def add_note(self, note_id, title, content="", tag="general", pinned=False):
        note = Note(note_id, title, content, tag, pinned)
        self.notes.append(note)
        return note

    def save_to_json(self, filepath):
        """Save all notes to a JSON file using a `with open(...)` context manager.

        Steps:
        1. Open filepath in 'w' mode with encoding='utf-8' using `with`
        2. Use json.dump with indent=2
        3. Print a confirmation message
        """
        # YOUR CODE HERE
        pass

    def load_from_json(self, filepath):
        """Load notes from a JSON file using a `with open(...)` context manager.

        Steps:
        1. If file doesn't exist: print a warning and return False
        2. Open and read with json.load
        3. Rebuild self.notes using Note.from_dict
        4. Return True
        """
        # YOUR CODE HERE
        pass


# ============================================================
# TEST YOUR CODE — run: python practice.py
# ============================================================

if __name__ == "__main__":

    # ── Test 1: BlockTimer ────────────────────────────────────
    print("=== Test 1: BlockTimer ===")
    with BlockTimer("Simulated work") as t:
        time.sleep(0.05)
    print(f"  Captured duration: {t.duration:.4f}s")
    assert t.duration >= 0.04, "Duration should be >= 0.04s"
    print("  PASSED\n")


    # ── Test 2: suppress_errors ───────────────────────────────
    print("=== Test 2: suppress_errors ===")

    with suppress_errors(ZeroDivisionError):
        _ = 1 / 0
    print("  Continued after ZeroDivisionError — PASSED")

    with suppress_errors(KeyError, ValueError):
        d = {}
        _ = d["missing"]
    print("  Continued after KeyError — PASSED")

    try:
        with suppress_errors(ValueError):
            raise TypeError("not suppressed")
        print("  FAILED — should have raised TypeError")
    except TypeError:
        print("  TypeError correctly propagated — PASSED\n")


    # ── Test 3: temp_tag ──────────────────────────────────────
    print("=== Test 3: temp_tag ===")
    note = Note("N001", "Meeting notes", tag="work")
    print(f"  Before: tag={note.tag}")

    with temp_tag(note, "urgent") as n:
        print(f"  Inside: tag={n.tag}")
        assert n.tag == "urgent", "Tag should be 'urgent' inside context"

    print(f"  After:  tag={note.tag}")
    assert note.tag == "work", "Tag should be restored to 'work'"
    print("  PASSED\n")


    # ── Test 4: NotesManager JSON Persistence ─────────────────
    print("=== Test 4: NotesManager JSON Persistence ===")
    path = "test_notes.json"

    mgr = NotesManager()
    mgr.add_note("N001", "Buy groceries",   content="Milk, Eggs, Bread",   tag="personal")
    mgr.add_note("N002", "Sprint planning", content="Define user stories",  tag="work",    pinned=True)
    mgr.add_note("N003", "Book ideas",      content="Sci-fi short story",   tag="creative")

    mgr.save_to_json(path)

    new_mgr = NotesManager()
    result = new_mgr.load_from_json(path)
    assert result is True, "load_from_json should return True on success"
    assert len(new_mgr.notes) == 3, f"Expected 3 notes, got {len(new_mgr.notes)}"

    print(f"  Loaded {len(new_mgr.notes)} notes:")
    for n in new_mgr.notes:
        print(f"    {n}")

    sprint = next(n for n in new_mgr.notes if n.note_id == "N002")
    assert sprint.pinned is True, "Pinned field should survive JSON round-trip"

    result2 = new_mgr.load_from_json("does_not_exist.json")
    assert result2 is False, "Should return False when file is missing"
    print("  Missing-file warning handled — PASSED")

    if os.path.exists(path):
        os.remove(path)

    print("\nDay 21 — All tests passed!")
