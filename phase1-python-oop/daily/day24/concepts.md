# Day 24 — Project 6 Build Day: Diary / Notes & Task Journal
## Project 6: Diary / Notes App (Part 4: Build & Polish 🚀)

> **Revisits from Days 1–23:** `class`, `__init__`, `to_dict()`/`from_dict()`, Custom Exceptions (`try...except`), File I/O (`json`, text), Decorators, Generators

---

## 🧒 Taught Like You Are 10 Years Old

Imagine you have a magical notebook.
- On **Day 21**, you taught the notebook to guard itself against errors (Exception Handling).
- On **Day 22**, you created your own custom alarms like `NoteNotFoundError`.
- On **Day 23**, you taught the notebook how to save its memory into a file on disk so it never forgets when you turn off the computer.

Today, on **Day 24**, you are giving your notebook **superpowers**:
1. It can count words and calculate how long it takes to read (`word_count`).
2. It organizes notes into tidy colored folders by tag (`tag_notes`).
3. It can package all your thoughts into pretty export files (`export_all`).
4. And finally, you connect it to an interactive web interface!

---

## What You Are Building Today

Today is **Build Day** for Project 6. You finalize the core analytics logic:
- **Task 1: `word_count(text_or_note)`** — Word count, character count, and reading time estimation.
- **Task 2: `tag_notes(manager)`** — Grouping notes by tags using dictionaries and sets.
- **Task 3: `export_all(manager, filepath, format="json"|"markdown"|"txt")`** — Multi-format export with error handling.

---

## Concept 1: `word_count(text)` — Text Analysis & Reading Time

Counting words in Python is simple using `.split()`.
`.split()` splits on any whitespace (spaces, tabs, newlines) and removes consecutive whitespaces.

```python
def word_count(text: str) -> dict:
    """
    Analyzes text and returns statistics:
    - words: total number of words
    - chars: total characters (excluding newlines)
    - reading_time_min: estimated reading time (avg 200 words per minute)
    """
    words = text.split()
    total_words = len(words)
    total_chars = len(text.replace("\n", ""))
    reading_time = round(total_words / 200, 2) if total_words > 0 else 0.0

    return {
        "words": total_words,
        "chars": total_chars,
        "reading_time_min": reading_time
    }
```

### 💡 Why `.split()` instead of `.split(" ")`?
- `"hello   world".split(" ")` returns `['hello', '', '', 'world']` (unwanted empty strings!)
- `"hello   world".split()` returns `['hello', 'world']` (clean words, handles tabs & newlines)

---

## Concept 2: `tag_notes(manager)` — Grouping by Category

In real-world apps, users tag notes as `#work`, `#personal`, `#study`, or `#todo`.
We want a dictionary where each **tag** maps to a list of Note objects:

```python
def tag_notes(manager) -> dict[str, list]:
    """
    Groups all notes in manager by their tag.
    Returns: { "work": [Note, Note], "personal": [Note], ... }
    """
    grouped = {}
    for note in manager.notes:
        tag = note.tag.lower()
        if tag not in grouped:
            grouped[tag] = []
        grouped[tag].append(note)
    return grouped
```

### 💡 Pro Tip: `collections.defaultdict`
You can also use:
```python
from collections import defaultdict

grouped = defaultdict(list)
for note in manager.notes:
    grouped[note.tag.lower()].append(note)
return dict(grouped)
```

---

## Concept 3: `export_all(manager, filepath, format="json")`

Users want to backup or share their diary. We support 3 formats:
1. **`json`**: Machine-readable, full fidelity (preserves note_id, pinned status, etc.)
2. **`markdown`**: Human-readable with `# Title`, tags, and divider lines.
3. **`txt`**: Simple plain text summary.

```python
def export_all(manager, filepath: str, format: str = "json") -> int:
    """
    Exports all notes to filepath in the specified format ('json', 'markdown', 'txt').
    Returns the count of exported notes.
    Raises ValueError if format is unsupported.
    """
    format = format.lower()
    if format == "json":
        data = [note.to_dict() for note in manager.notes]
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    elif format in ("markdown", "md"):
        with open(filepath, "w", encoding="utf-8") as f:
            for note in manager.notes:
                pin = "📌 " if getattr(note, "pinned", False) else ""
                f.write(f"# {pin}{note.title}\n")
                f.write(f"**Tag:** #{note.tag} | **ID:** {note.note_id}\n\n")
                f.write(f"{note.content}\n\n")
                f.write("---\n\n")

    elif format == "txt":
        with open(filepath, "w", encoding="utf-8") as f:
            for note in manager.notes:
                f.write(f"[{note.note_id}] {note.title} (Tag: {note.tag})\n")
                f.write(f"{note.content}\n")
                f.write("=" * 40 + "\n\n")
    else:
        raise ValueError(f"Unsupported format '{format}'. Choose json, markdown, or txt.")

    return len(manager.notes)
```

---

## 🎯 Daily Checklist
- [ ] Read concepts above
- [ ] Open `daily/day24/practice.py` and implement all 3 tasks
- [ ] Run `python practice.py` until all tests pass
- [ ] Launch the Project 6 Frontend website in your browser!
