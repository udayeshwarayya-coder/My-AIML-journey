# Day 19 — Python Generators & `yield`
## Project 5: Task/Todo Manager (Part 3)

> **Revisits from Days 1–18:** `class`, `__init__`, `self`, `__str__`, `__repr__`, `@property`, `*args, **kwargs`, `@wraps`, `@timer` (Essential 2-Layer Decorator)

---

## What You Already Know (Quick Recap)

Until now, when functions produce multiple items (like tasks), they create a `list` in memory and return the whole list at once:

```python
def get_pending_tasks(tasks):
    result = []
    for t in tasks:
        if not t.done:
            result.append(t)
    return result    # Returns the entire list stored in RAM
```

**The Problem:** What if you had **1,000,000 tasks** or an AI dataset with **100,000 images**? Creating a list of 100,000 items in memory will slow down or crash your computer.

**Today's Superpower:** **Generators & `yield`** — produce items **one by one on demand** without storing the whole collection in RAM.

---

## Concept 1: `return` vs `yield`

| Feature | `return` (Normal Function) | `yield` (Generator Function) |
|:---|:---|:---|
| **Execution** | Runs to completion and terminates | **Pauses** execution, remembers its state, and resumes when asked |
| **Memory** | Stores ALL items in memory (RAM) at once | Generates **ONE item at a time** on-the-fly (O(1) memory) |
| **Return Value** | The final value / list | A **Generator Object** you can iterate over |

### Side-by-Side Example:

```python
# 1. Normal list function
def get_numbers():
    return [1, 2, 3]

# 2. Generator function (using yield)
def generate_numbers():
    yield 1
    yield 2
    yield 3
```

When you call `generate_numbers()`, it doesn't run immediately. It returns a **generator object**:

```python
gen = generate_numbers()

for num in gen:
    print(num)
# Output:
# 1
# 2
# 3
```

---

## Concept 2: How `yield` Works Step-by-Step

Think of `yield` like a **pause button**:

```python
def task_stream(task_list):
    for task in task_list:
        if not task.done:
            yield task   # Pauses here, gives task to caller, waits for next loop iteration
```

You can consume a generator using:
1. **`for` loop (Standard & Recommended):**
   ```python
   for task in task_stream(tasks):
       print(task.title)
   ```
2. **`next()` (Manual one-by-one):**
   ```python
   gen = task_stream(tasks)
   first_task = next(gen)
   ```
3. **`list()` (Convert all remaining items to list if needed):**
   ```python
   pending_list = list(task_stream(tasks))
   ```

---

## Concept 3: Why AI & ML Love Generators (Batching)

In Machine Learning (like PyTorch and TensorFlow), we train models on large datasets in **batches** (e.g. 32 or 64 samples at a time).

A **Batch Generator** yields chunks of data:

```python
def batch_generator(items, batch_size=2):
    for i in range(0, len(items), batch_size):
        yield items[i : i + batch_size]   # Yields a slice of size `batch_size`
```

Usage:
```python
tasks = ["Task 1", "Task 2", "Task 3", "Task 4", "Task 5"]

for batch in batch_generator(tasks, batch_size=2):
    print("Processing batch:", batch)

# Output:
# Processing batch: ['Task 1', 'Task 2']
# Processing batch: ['Task 3', 'Task 4']
# Processing batch: ['Task 5']
```

---

## Concept 4: The ONLY Custom Decorator You Need — `@timer`

To benchmark code (e.g. comparing list performance vs generator streaming), we use the simple, standard **2-layer `@timer` decorator**:

```python
import time
from functools import wraps

def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        duration = time.time() - start
        print(f"⏱ {func.__name__} took {duration:.5f}s")
        return result
    return wrapper
```

> **Why this matters:** You will use this exact `@timer` pattern in Machine Learning to benchmark inference speeds and model training times!

---

## What You Are Building Today

| Component | Description |
|:----------|:------------|
| `@timer` | Standard execution-time benchmarking decorator |
| `task_id_generator(start=1)` | Infinite ID generator using `while True:` and `yield` |
| `pending_tasks_generator(tasks)` | Generator yielding only pending tasks one-by-one |
| `batch_tasks(tasks, batch_size)` | Generator streaming tasks in batches (chunks) |
| `TaskManager` (Streaming Edition) | Task manager equipped with generator methods (`iter_pending()`, `iter_by_priority()`, `batch_export()`) |

---

## 10-Minute Read Check

You now understand:
- [ ] `yield` pauses a function and returns a value; it resumes on the next request.
- [ ] Generators do not load everything into RAM at once — they compute items on demand.
- [ ] You iterate over generators using a standard `for` loop or convert to a list with `list()`.
- [ ] `@timer` is a straightforward 2-layer decorator that measures execution duration using `time.time()`.

**Now open `practice.py` to write your Day 19 exercises!**
