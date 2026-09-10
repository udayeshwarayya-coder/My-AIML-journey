# Day 23 — File I/O (Reading & Writing Files)
## Taught Like You Are 10 Years Old 🧒

---

## 🧠 The Real-Life Story

Imagine you write your diary every night.

- You **open** the diary
- You **write** something
- You **close** the diary

The next day, you **open** it again and **read** what you wrote.

Python does **exactly** this with files.
Files are just diaries that Python can open, read, write, and close.

---

## 🔑 Opening a File — the `with` keyword

`python
# GOOD — context manager (you learned this Day 21!)
with open("notes.txt", "w") as f:
    f.write("Hello, world!\n")
# file is automatically closed here — ALWAYS
`

You already know `with` from **Day 21**. Files are just another resource you borrow and return.

---

## 📂 The Three Modes

`python
open("file.txt", "w")   # write  — creates new file (or WIPES existing!)
open("file.txt", "a")   # append — adds to end of file (safe!)
open("file.txt", "r")   # read   — reads existing file (default)
`

Memory trick:
`
"w" = Wipe & Write
"a" = Add to end
"r" = Read only
`

Always add encoding="utf-8" to handle all characters safely:
`python
with open("notes.txt", "w", encoding="utf-8") as f:
    f.write("Hello World\n")
`

---

## 📝 Writing Text Files

`python
# Write a single string
with open("diary.txt", "w", encoding="utf-8") as f:
    f.write("Day 1: Started my journey.\n")
    f.write("Day 2: Learned File I/O.\n")

# Write a list of lines at once
lines = ["Line 1\n", "Line 2\n", "Line 3\n"]
with open("diary.txt", "w", encoding="utf-8") as f:
    f.writelines(lines)
`

---

## 📖 Reading Text Files

`python
# Read entire file as one big string
with open("diary.txt", "r", encoding="utf-8") as f:
    content = f.read()
    print(content)

# Read line by line (best for large files)
with open("diary.txt", "r", encoding="utf-8") as f:
    for line in f:
        print(line.strip())   # .strip() removes trailing \n

# Read all lines into a list
with open("diary.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()     # ["Line 1\n", "Line 2\n", ...]
`

---

## 🗃️ JSON Files — Save Python Objects

Text files store strings. But what about your **Note objects**?
You need to convert them to JSON first.

`
Note object  →  dict  →  JSON string  →  file
file  →  JSON string  →  dict  →  Note object
`

### Writing JSON

`python
import json

notes_data = [
    {"note_id": "N001", "title": "Buy milk", "tag": "personal"},
    {"note_id": "N002", "title": "Sprint review", "tag": "work"}
]

with open("notes.json", "w", encoding="utf-8") as f:
    json.dump(notes_data, f, indent=2)
`

The file will look like:
`json
[
  {
    "note_id": "N001",
    "title": "Buy milk",
    "tag": "personal"
  }
]
`

### Reading JSON

`python
with open("notes.json", "r", encoding="utf-8") as f:
    notes_data = json.load(f)

print(notes_data[0]["title"])  # "Buy milk"
`

### Quick Comparison

| Function         | Direction       | Input       |
|------------------|-----------------|-------------|
| json.dump(obj,f) | Python → File   | file handle |
| json.load(f)     | File → Python   | file handle |
| json.dumps(obj)  | Python → String | (no file)   |
| json.loads(s)    | String → Python | (no file)   |

---

## 🚨 Handling Missing Files

`python
# This CRASHES with FileNotFoundError:
with open("missing.json", "r") as f:
    data = json.load(f)

# Handle it gracefully (Day 22 skills!):
try:
    with open("notes.json", "r", encoding="utf-8") as f:
        data = json.load(f)
except FileNotFoundError:
    raise NoteNotFoundError(f"File 'notes.json' does not exist")
`

---

## 🗺️ os.path — Check Before You Open

`python
import os

os.path.exists("notes.json")        # True if file exists
os.path.getsize("notes.json")       # size in bytes
os.path.dirname("data/notes.json")  # "data"
os.path.basename("data/notes.json") # "notes.json"
`

---

## 🔄 Full Round-Trip Example

`python
import json

# --- Save ---
def save(notes, filepath):
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(notes, f, indent=2)

# --- Load ---
def load(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# Usage
data = [{"id": "N001", "title": "Hello"}]
save(data, "notes.json")
loaded = load("notes.json")
print(loaded)  # [{"id": "N001", "title": "Hello"}]
`

---

## 🤖 ML Connection

`python
# Saving model config (same concept!)
import json

model_config = {"learning_rate": 0.001, "epochs": 50, "accuracy": 0.94}

with open("model_config.json", "w") as f:
    json.dump(model_config, f, indent=2)

with open("model_config.json", "r") as f:
    config = json.load(f)

print(config["accuracy"])  # 0.94

# PyTorch does the same under the hood:
# torch.save(model.state_dict(), "model.pth")
# model.load_state_dict(torch.load("model.pth"))
`

---

## 🧩 The 4 Big Rules

| Rule                             | Remember it as                            |
|----------------------------------|-------------------------------------------|
| Always use with open(...)        | "Day 21 — always return borrowed things"  |
| Always specify encoding="utf-8"  | "Don't break on emoji or special chars"   |
| "w" wipes the file               | "w = Wipe & Write — be careful!"          |
| Catch FileNotFoundError          | "Day 22 — specific errors, specific cases"|

---

## 📝 Quick Summary — Day 23 in 6 Lines

`
open(file, "w")     →  create/overwrite file
open(file, "a")     →  append to file
open(file, "r")     →  read file
json.dump(obj, f)   →  Python object → JSON file
json.load(f)        →  JSON file → Python object
FileNotFoundError   →  raised when file doesn't exist
`

---

## ✅ 10-Second Read Check

- [ ] with open(...) automatically closes the file — even on error.
- [ ] "w" mode wipes the existing file. Use "a" to append.
- [ ] json.dump(data, f) writes a Python list/dict to a JSON file.
- [ ] json.load(f) reads a JSON file back into a Python list/dict.
- [ ] FileNotFoundError is raised when reading a missing file.
- [ ] Always use encoding="utf-8" to handle all characters.
- [ ] os.path.exists(path) checks if a file exists before opening.
