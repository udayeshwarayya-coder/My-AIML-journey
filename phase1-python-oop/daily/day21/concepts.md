# Day 21 — Python Context Managers & the `with` Statement
## Project 6: Diary / Notes App (Part 1: Resource Management)

> **Revisits from Days 1–20:** `class`, `__init__`, `self`, `__str__`, `__repr__`, `@property`, `yield`, Generators, Decorators (`@timer`, `@wraps`)

---

## What You Already Know (Quick Recap)

In Days 17–19, you mastered **Decorators & Generators** to wrap functions and stream data lazily.
In Day 20, you shipped the Task/Todo Manager website.

**The Problem:** When dealing with external resources (files, database connections, locks, GPU memory, or ML inference modes), we often need to **acquire a resource, do some work, and guarantee cleanup** (closing files, releasing locks, restoring states) even if an error occurs.

Using `try...finally` works, but gets repetitive and error-prone:
```python
file = open("notes.json", "w")
try:
    file.write(data)
finally:
    file.close()
```

**Today's Superpower:** **Context Managers & the `with` Statement** — Python's standard mechanism to manage resources safely, handle setup/teardown, and guarantee cleanup.

---

## Concept 1: The `with` Statement & Dunder Protocol (`__enter__`, `__exit__`)

Any class can become a Context Manager by implementing two magic (dunder) methods:
1. `__enter__(self)`: Runs **before** the code block inside `with`. Its return value is bound to the variable after `as` (e.g. `with Context() as ctx:`).
2. `__exit__(self, exc_type, exc_val, exc_tb)`: Runs **after** the code block finishes, **guaranteed** (even if an exception was raised inside the `with` block).

### Anatomy of a Context Manager Class:

```python
class FileManager:
    def __init__(self, filename, mode):
        self.filename = filename
        self.mode = mode
        self.file = None

    def __enter__(self):
        print(f"📂 Opening {self.filename}")
        self.file = open(self.filename, self.mode, encoding="utf-8")
        return self.file  # Bound to variable in 'as'

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.file:
            print(f"🔒 Closing {self.filename}")
            self.file.close()
        # Return True if you want to suppress an exception, False otherwise
        return False
```

### Usage:
```python
with FileManager("notes.txt", "w") as f:
    f.write("Note 1: Learn Context Managers\n")
# Output:
# 📂 Opening notes.txt
# 🔒 Closing notes.txt
```

---

## Concept 2: Class-based vs Function-based (`@contextmanager`)

Python provides a shortcut to create context managers using **generators + `@contextmanager`** from `contextlib`:

```python
from contextlib import contextmanager
import time

@contextmanager
def execution_timer(label="Task"):
    start = time.time()
    print(f"▶️ Starting: {label}")
    try:
        yield  # Code inside 'with' block executes here
    finally:
        duration = time.time() - start
        print(f"⏹️ {label} completed in {duration:.4f}s")
```

### Usage:
```python
with execution_timer("Processing notes"):
    time.sleep(0.5)
```

---

## Concept 3: Why AI & ML Love Context Managers

In Machine Learning (PyTorch, TensorFlow, HuggingFace), context managers are used everywhere to control execution contexts:

1. **Disabling Gradient Computation (Inference):**
   ```python
   with torch.no_grad():
       predictions = model(inputs)
   ```
2. **Mixed Precision Acceleration:**
   ```python
   with torch.cuda.amp.autocast():
       loss = model(inputs)
   ```
3. **Benchmarking & Profiling:**
   ```python
   with execution_timer("Model Training Epoch 1"):
       train_one_epoch()
   ```

---

## Concept 4: JSON File Persistence for Notes App

Today, we will equip our `NotesManager` with **JSON persistence** using context managers and Python's built-in `json` module:

```python
import json

# Saving notes to disk:
with open("notes.json", "w", encoding="utf-8") as f:
    json.dump([n.to_dict() for n in notes], f, indent=2)

# Loading notes from disk:
with open("notes.json", "r", encoding="utf-8") as f:
    data = json.load(f)
```

---

## What You Are Building Today

| Component | Description |
|:----------|:------------|
| `BlockTimer` | Class-based context manager (`__enter__`, `__exit__`) measuring block execution time |
| `suppress_errors(*exceptions)` | Context manager that catches and silences specified exception types safely |
| `temp_tag(note, new_tag)` | Generator-based context manager (`@contextmanager`) temporarily changing a note's tag and restoring it afterwards |
| `Note.to_dict()` & `Note.from_dict()` | Serialization methods to convert Note objects to/from dictionary representation |
| `NotesManager` (Persistence Edition) | Methods `save_to_json(filepath)` and `load_from_json(filepath)` with safe context manager file handling |

---

## 10-Minute Read Check

- [ ] `__enter__` executes before entering the `with` block; whatever it returns is assigned to `as target`.
- [ ] `__exit__` always runs when exiting the block, making cleanup deterministic.
- [ ] `@contextmanager` lets you convert a generator with a single `yield` into a context manager.
- [ ] Context managers keep code clean, error-safe, and avoid manual resource leakage.
- [ ] In ML, `torch.no_grad()` and `autocast()` are both context managers you'll use daily.
