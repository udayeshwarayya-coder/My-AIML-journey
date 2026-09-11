import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Day 24 Practice — Text Analytics, Tag Grouping & Multi-Format Export
# Project 6: Diary / Notes App (Part 4: Build Day)
# Topic: String processing, dictionary grouping, multi-format file export
# Goal: Build word_count(), tag_notes(), export_all()
#
# HINT LEVEL: 90%

import json
import os


# ============================================================
# NOTE & NOTESMANAGER (carried forward from Days 21-23)
# ============================================================

class Note:
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
                   data["content"], data["tag"], data.get("pinned", False))

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
# TASK 1: word_count(text)
# ============================================================
# Count the number of words, characters (excluding newlines), and 
# calculate estimated reading time in minutes (assuming 200 words/min).
#
# Requirements:
# - words: len(text.split())
# - chars: len(text.replace("\n", ""))
# - reading_time_min: round(words / 200, 2) if words > 0 else 0.0
# - Return a dict: {"words": int, "chars": int, "reading_time_min": float}
#
# Hint:
#   words = text.split()
#   total_words = len(words)
#   total_chars = len(text.replace("\n", ""))
#   reading_time = round(total_words / 200, 2) if total_words > 0 else 0.0
#   return {"words": total_words, "chars": total_chars, "reading_time_min": reading_time}

def word_count(text: str) -> dict:
    # YOUR CODE HERE
    words=text.split()
    total_words=len(words)
    total_char=len(text.replace("\n",""))
    reading_time=round(total_words/200,2) if total_words > 0 else 0.0
    return {"words":total_words,"chars":total_char,"reading_time_min":reading_time}


# ============================================================
# TASK 2: tag_notes(manager)
# ============================================================
# Group all notes in manager by their tag (case-insensitive, lower-cased keys).
#
# Requirements:
# - Return a dictionary where keys are lowercase tag names (e.g., 'work', 'study')
#   and values are lists of Note objects belonging to that tag.
# - If manager.notes is empty, return an empty dictionary {}.
#
# Hint:
#   grouped = {}
#   for note in manager.notes:
#       tag_key = note.tag.lower()
#       if tag_key not in grouped:
#           grouped[tag_key] = []
#       grouped[tag_key].append(note)
#   return grouped

def tag_notes(manager) -> dict[str, list]:
    # YOUR CODE HERE
    grouped={}
    for note in manager.notes:
        note_key=note.tag.lower()
        if note_key not in grouped:
            grouped[note_key]=[]
        grouped[note_key].append(note)
    return grouped


# ============================================================
# TASK 3: export_all(manager, filepath, format="json")
# ============================================================
# Export all notes to a file in the requested format: "json", "markdown" (or "md"), or "txt".
#
# Requirements:
# - format is case-insensitive.
# - If format == "json":
#     Write [note.to_dict() for note in manager.notes] using json.dump with indent=2, encoding="utf-8".
# - If format in ("markdown", "md"):
#     Write markdown formatted entries:
#       # {title}
#       **Tag:** #{tag} | **ID:** {note_id}
#       
#       {content}
#       
#       ---
# - If format == "txt":
#     Write plain text format:
#       [{note_id}] {title} (Tag: {tag})
#       {content}
#       ========================================
# - If format is anything else: raise ValueError(f"Unsupported format '{format}'")
# - Always use encoding="utf-8"
# - Return the count of exported notes: len(manager.notes)
#
# Hint:
#   fmt = format.lower()
#   if fmt == "json":
#       with open(filepath, "w", encoding="utf-8") as f:
#           json.dump([n.to_dict() for n in manager.notes], f, indent=2)
#   elif fmt in ("markdown", "md"):
#       with open(filepath, "w", encoding="utf-8") as f:
#           for n in manager.notes:
#               f.write(f"# {n.title}\n**Tag:** #{n.tag} | **ID:** {n.note_id}\n\n{n.content}\n\n---\n\n")
#   elif fmt == "txt":
#       with open(filepath, "w", encoding="utf-8") as f:
#           for n in manager.notes:
#               f.write(f"[{n.note_id}] {n.title} (Tag: {n.tag})\n{n.content}\n" + "="*40 + "\n\n")
#   else:
#       raise ValueError(f"Unsupported format '{format}'")
#   return len(manager.notes)

def export_all(manager, filepath: str, format: str = "json") -> int:
    # YOUR CODE HERE
    fmt = format.lower()
    if fmt == "json":
      with open(filepath, "w", encoding="utf-8") as f:
          json.dump([n.to_dict() for n in manager.notes], f, indent=2)
    elif fmt in ("markdown", "md"):
      with open(filepath, "w", encoding="utf-8") as f:
          for n in manager.notes:
              f.write(f"# {n.title}\n**Tag:** #{n.tag} | **ID:** {n.note_id}\n\n{n.content}\n\n---\n\n")
    elif fmt == "txt":
      with open(filepath, "w", encoding="utf-8") as f:
          for n in manager.notes:
              f.write(f"[{n.note_id}] {n.title} (Tag: {n.tag})\n{n.content}\n" + "="*40 + "\n\n")
    else:
      raise ValueError(f"Unsupported format '{format}'")
    return len(manager.notes)


# ============================================================
# TEST RUNNER — Run: python practice.py
# ============================================================

if __name__ == "__main__":
    print("=== Day 24 Practice Tests ===\n")

    # ── Test 1: word_count ────────────────────────────────────
    print("--- Test 1: word_count ---")
    sample_text = "The quick brown fox jumps over the lazy dog.\nLearning Python OOP every day!"
    res = word_count(sample_text)
    assert res["words"] == 14, f"Expected 14 words, got {res['words']}"
    assert res["chars"] == len(sample_text.replace("\n", "")), "Characters count mismatch"
    assert res["reading_time_min"] == round(14 / 200, 2), "Reading time calculation mismatch"

    empty_res = word_count("")
    assert empty_res["words"] == 0
    assert empty_res["reading_time_min"] == 0.0
    print("  PASSED\n")

    # ── Setup manager for remaining tests ─────────────────────
    mgr = NotesManager()
    mgr._raw_add("N01", "Meeting Notes", "Discuss Q3 roadmap and team hiring goals.", "work", pinned=True)
    mgr._raw_add("N02", "Python Generators", "yield pauses execution and produces a generator object.", "study")
    mgr._raw_add("N03", "Weekly Groceries", "Buy oats, milk, coffee beans, and spinach.", "personal")
    mgr._raw_add("N04", "OOP Revision", "Revisit inheritance, polymorphism, and magic methods.", "study")

    # ── Test 2: tag_notes ─────────────────────────────────────
    print("--- Test 2: tag_notes ---")
    tags = tag_notes(mgr)
    assert isinstance(tags, dict), "Should return a dictionary"
    assert set(tags.keys()) == {"work", "study", "personal"}, f"Unexpected tags: {tags.keys()}"
    assert len(tags["study"]) == 2, f"Expected 2 study notes, got {len(tags['study'])}"
    assert len(tags["work"]) == 1
    assert len(tags["personal"]) == 1
    print(f"  Grouped tags: {list(tags.keys())}")
    print("  PASSED\n")

    # ── Test 3: export_all (JSON) ─────────────────────────────
    print("--- Test 3: export_all (JSON) ---")
    json_path = "test_export.json"
    count = export_all(mgr, json_path, format="json")
    assert count == 4, f"Expected 4 exported notes, got {count}"
    assert os.path.exists(json_path), "JSON export file not found"
    with open(json_path, "r", encoding="utf-8") as f:
        loaded = json.load(f)
    assert len(loaded) == 4
    assert loaded[0]["title"] == "Meeting Notes"
    os.remove(json_path)
    print("  JSON export verified & PASSED\n")

    # ── Test 4: export_all (Markdown) ─────────────────────────
    print("--- Test 4: export_all (Markdown) ---")
    md_path = "test_export.md"
    count_md = export_all(mgr, md_path, format="markdown")
    assert count_md == 4
    assert os.path.exists(md_path), "Markdown export file not found"
    with open(md_path, "r", encoding="utf-8") as f:
        md_text = f.read()
    assert "# Meeting Notes" in md_text
    assert "**Tag:** #work" in md_text
    os.remove(md_path)
    print("  Markdown export verified & PASSED\n")

    # ── Test 5: export_all (Unsupported format) ───────────────
    print("--- Test 5: export_all (Unsupported format) ---")
    try:
        export_all(mgr, "test.pdf", format="pdf")
        print("  FAILED — should have raised ValueError")
    except ValueError as e:
        print(f"  ValueError raised correctly: {e}")
        print("  PASSED\n")

    print("🎉 Day 24 Practice — All tests completed successfully!")
