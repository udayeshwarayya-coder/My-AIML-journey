# Day 21 + 22 — Context Managers & Custom Exceptions
## Taught Like You Are 10 Years Old 🧒

---

# PART 1 — Context Managers (Day 21)
## "The Magic Bodyguard"

---

### 🧠 The Real-Life Story

Imagine you borrow a library book.

Steps:
1. Walk in — tell the librarian "I want a book"
2. Read the book
3. Return the book BEFORE you leave — even if you trip and fall on the way out!

Python has this exact system for **files, locks, timers, GPU memory** — anything you borrow and must return.

That system is called a **Context Manager**.

---

### 🔑 The `with` keyword

```python
# BAD — if an error happens between open() and close(), file never closes!
f = open("notes.txt", "w")
f.write("hello")
f.close()   # <-- might never reach here if error above!

# GOOD — with GUARANTEES the file closes, always!
with open("notes.txt", "w") as f:
    f.write("hello")
# file automatically closed here — even if an error happened inside
```

Think of `with` as:
> "Hey Python — I'm borrowing this resource. Make sure I return it, no matter what."

---

### 🏗️ How to BUILD your own Context Manager (Class way)

You need exactly 2 magic methods:

```
__enter__  →  runs BEFORE the with block  →  "Walk into the library"
__exit__   →  runs AFTER the with block   →  "Return the book before leaving"
```

```python
class BlockTimer:
    def __init__(self, label="Block"):
        self.label = label       # name of this timer
        self.duration = 0.0      # will store the time taken

    def __enter__(self):
        # STEP 1: record the start time
        self.start_time = time.time()
        return self              # 'self' is given to 'as t' in  "with BlockTimer() as t"

    def __exit__(self, exc_type, exc_val, exc_tb):
        # STEP 2: calculate how long it took
        self.duration = time.time() - self.start_time
        print(f"[{self.label}] took {self.duration:.4f}s")
        return False             # False = "do NOT hide any errors"
```

How you USE it:
```python
import time
with BlockTimer("Simulated work") as t:
    time.sleep(0.05)             # pretend to do some work
# After the block, __exit__ runs automatically
print(t.duration)                # you can still read duration after!
```

Output:
```
[Simulated work] took 0.0503s
0.0503
```

---

### ⚡ Shortcut way — `@contextmanager` + generator

Instead of a whole class, you can use a **function with `yield`**:

```python
from contextlib import contextmanager

@contextmanager
def temp_tag(note, new_tag):
    old_tag = note.tag        # save original tag
    note.tag = new_tag        # change it

    try:
        yield note            # <-- "with block" runs HERE
    finally:
        note.tag = old_tag    # ALWAYS restore, even if error happened
```

Think of it like:
```
Everything BEFORE yield  =  __enter__
The yield itself         =  the 'with' block runs here
Everything AFTER yield   =  __exit__
```

Usage:
```python
with temp_tag(my_note, "urgent") as n:
    print(n.tag)   # urgent
# After block, tag is restored automatically
print(my_note.tag)  # back to original
```

---

### 🤖 ML Connection

```python
# PyTorch — you use context managers EVERY day in ML:
with torch.no_grad():          # turns off gradient tracking (saves memory)
    predictions = model(inputs)

with torch.cuda.amp.autocast(): # uses faster 16-bit math
    loss = model(inputs)
```

---

### 🧩 The 3 Big Rules to Remember

| Rule | Remember it as |
|------|----------------|
| `__enter__` always runs first | "Knock before entering" |
| `__exit__` ALWAYS runs last | "Always return borrowed things" |
| `return False` in `__exit__` | "Don't hide errors" |

---
---

# PART 2 — Custom Exceptions (Day 22)
## "Making Your Own Error Signs"

---

### 🧠 The Real-Life Story

Imagine a restaurant.

When something goes wrong, a good waiter doesn't just say **"Error!"** — they say:
- "Sorry, that dish is **not on the menu**." (ItemNotFoundError)
- "Sorry, we **already have** a reservation under that name." (DuplicateBookingError)
- "Sorry, **kitchen is closed**." (KitchenClosedError)

**Specific errors tell you exactly what went wrong.**

Python lets you create your own error types the same way!

---

### 🔑 How to CREATE a Custom Exception

A custom exception is just a **class** that inherits from `Exception`:

```python
# This is ALL you need!
class NoteNotFoundError(Exception):
    pass
```

That's it. Now you have your own error type.

**Hierarchy** — make a family of related errors:

```python
class NotesAppError(Exception):        # GRANDPARENT — the base error
    pass

class NoteNotFoundError(NotesAppError): # CHILD — specific error
    pass

class DuplicateNoteError(NotesAppError): # CHILD — another specific error
    pass

class InvalidFieldError(NotesAppError):  # CHILD — yet another
    pass
```

Think of it like:
```
NotesAppError
├── NoteNotFoundError    (note ID does not exist)
├── DuplicateNoteError   (note ID already taken)
└── InvalidFieldError    (you passed a bad field name)
```

---

### 🔑 How to RAISE (throw) a custom exception

```python
def find_note(manager, note_id):
    for note in manager.notes:
        if note.note_id == note_id:
            return note                  # found it!

    # If we reach here — note was NOT found
    raise NoteNotFoundError(f"Note '{note_id}' does not exist.")
#   ^^^^^                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#   keyword                 the message (you can write anything)
```

---

### 🔑 How to CATCH your custom exception

```python
try:
    note = find_note(mgr, "N999")     # this will raise NoteNotFoundError
except NoteNotFoundError as e:
    print(f"Caught it! {e}")           # e is the error message
```

**Catching parent catches ALL children:**
```python
try:
    note = find_note(mgr, "N999")
except NotesAppError as e:             # catches NoteNotFoundError too!
    print("Something went wrong in the notes app")
```

---

### 🔑 The FULL try/except/else/finally anatomy

Most beginners only know `try` and `except`. There are 4 parts:

```python
try:
    note = find_note(mgr, "N001")     # the risky code goes here
except NoteNotFoundError as e:
    print("Note not found:", e)        # runs ONLY if error happened
else:
    print("Note found:", note)         # runs ONLY if NO error happened
finally:
    print("This ALWAYS runs!")         # runs NO MATTER WHAT
```

Simple memory trick:

```
try     →  "attempt this"
except  →  "if it fails, do this"
else    →  "if it succeeds, do this"
finally →  "always do this no matter what"
```

---

### 🔑 Using `finally` as an AUDIT LOG

```python
def delete_note(manager, note_id):
    try:
        note = find_note(manager, note_id)   # raises if not found
        manager.notes.remove(note)
        return note
    finally:
        # This prints WHETHER the delete worked OR raised an error
        print(f"Audit: tried to delete '{note_id}'")
```

Run it on a note that EXISTS:
```
Audit: tried to delete 'N001'    ← finally ran
# delete succeeded
```

Run it on a note that DOES NOT exist:
```
Audit: tried to delete 'N999'    ← finally STILL ran
NoteNotFoundError: Note 'N999' does not exist.
```

---

### 🔑 `setattr` — setting attributes by string name

In `update_note`, you need to update whatever fields the caller passes.
Instead of:
```python
if "title" in kwargs:
    note.title = kwargs["title"]
if "tag" in kwargs:
    note.tag = kwargs["tag"]
# etc...
```

You use **`setattr`**:
```python
setattr(note, "title", "New Title")   # same as: note.title = "New Title"
setattr(note, "tag",   "work")        # same as: note.tag = "work"
```

So in a loop:
```python
for key, value in kwargs.items():
    setattr(note, key, value)         # works for any field name!
```

---

### 🤖 ML Connection

```python
# Scikit-learn does this exact pattern:
class NotFittedError(Exception):
    """Raised when predict() is called before fit()."""
    pass

def predict(self, X):
    if not self.is_fitted:
        raise NotFittedError("Call fit() before predict()!")
    return self.model.predict(X)
```

---

### 🧩 Full Syntax Cheatsheet

```python
# 1. Define exceptions
class MyBaseError(Exception): pass
class MySpecificError(MyBaseError): pass

# 2. Raise them
raise MySpecificError("something went wrong")

# 3. Catch them
try:
    risky_code()
except MySpecificError as e:
    print(e)                       # handles specific
except MyBaseError as e:
    print(e)                       # handles all children
else:
    print("no error!")             # only if try succeeded
finally:
    print("always runs")           # always

# 4. setattr (update attributes by name)
setattr(obj, "field_name", new_value)  # same as obj.field_name = new_value
```

---

## 📝 Quick Summary — Day 21 + 22 in 6 Lines

```
with   →  borrow a resource, guarantee it's returned (context manager)
__enter__  →  setup code (before with block)
__exit__   →  cleanup code (after with block, always)
@contextmanager + yield  →  shortcut to make a context manager from a function

raise CustomError("msg")  →  throw your own specific error
try/except/else/finally   →  handle errors cleanly with guaranteed cleanup
```

---

## ✅ 10-Second Read Check

- [ ] `with` guarantees cleanup even if an error occurs inside the block.
- [ ] `__enter__` runs before, `__exit__` runs after — always.
- [ ] `yield` in a `@contextmanager` function marks where the `with` block runs.
- [ ] Custom exceptions inherit from `Exception` (or another exception class).
- [ ] `raise` triggers an exception; `except` catches it.
- [ ] `finally` runs no matter what — perfect for audit logs and cleanup.
- [ ] `setattr(obj, "field", value)` sets any attribute by name dynamically.