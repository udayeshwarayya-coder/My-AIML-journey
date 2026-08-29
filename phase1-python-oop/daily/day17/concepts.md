# Day 17 — Python Decorators
## Project 5: Task/Todo Manager (Part 1)

> **Revisits from Days 1–16:** `class`, `__init__`, `self`, `@property`, `__str__`, `__repr__`, `__eq__`, `__lt__`, `@classmethod`, `@staticmethod`, Inheritance, `super()`

---

## What You Already Know (Quick Recap)

You've been *using* decorators since Day 1 without realising it:

```python
@property          # ← decorator
def price(self): ...

@classmethod       # ← decorator
def from_string(cls, ...): ...

@app.route("/")    # ← decorator
def home(): ...
```

**Today**: You learn how decorators actually *work* — and write your own from scratch.

---

## Concept 1: What is a Decorator?

A **decorator** is a function that **takes another function** and **wraps it** to add extra behaviour — without modifying the original function's code.

```python
def my_decorator(func):       # takes a function
    def wrapper(*args, **kwargs):
        print("Before")
        result = func(*args, **kwargs)   # run the original
        print("After")
        return result
    return wrapper             # returns the new wrapped version

@my_decorator
def say_hello():
    print("Hello!")

say_hello()
# Before
# Hello!
# After
```

> `@my_decorator` is just shorthand for: `say_hello = my_decorator(say_hello)`

---

## Concept 2: `*args` and `**kwargs` — Why You Need Them

The wrapper must accept **any** arguments so it can forward them to the original function:

```python
def log_action(func):
    def wrapper(*args, **kwargs):    # accept anything
        print(f"Calling {func.__name__}")
        return func(*args, **kwargs) # forward everything
    return wrapper

@log_action
def add_task(title, priority="medium"):
    print(f"Added: {title}")

add_task("Study OOP", priority="high")
# Calling add_task
# Added: Study OOP
```

> Without `*args, **kwargs` the wrapper would fail if the original takes any arguments.

---

## Concept 3: `functools.wraps` — Always Use It

Without `@wraps`, the wrapped function loses its name and docstring:

```python
from functools import wraps

def log_action(func):
    @wraps(func)               # ← preserves __name__, __doc__
    def wrapper(*args, **kwargs):
        print(f"[LOG] {func.__name__} called")
        return func(*args, **kwargs)
    return wrapper

@log_action
def add_task(title):
    """Adds a task to the list."""
    pass

print(add_task.__name__)   # add_task  ✅  (without @wraps → "wrapper" ❌)
print(add_task.__doc__)    # Adds a task to the list.
```

> **Rule:** Always put `@wraps(func)` as the first line inside your decorator.

---

## Concept 4: Stacking Decorators

You can apply multiple decorators on one function — they stack from bottom to top:

```python
@log_action           # applied second (outer)
@validate_not_empty   # applied first (inner)
def add_task(title):
    print(f"Task '{title}' added.")

# Equivalent to:
# add_task = log_action(validate_not_empty(add_task))
```

```
call add_task("Study")
  → log_action wrapper runs first
      → validate_not_empty wrapper runs second
          → original add_task runs
```

---

## Concept 5: Decorator with a Parameter (Factory Pattern)

When you want `@repeat(3)` — a decorator that *takes a config argument*:

```python
def repeat(n):                         # outer: config
    def decorator(func):               # middle: takes function
        @wraps(func)
        def wrapper(*args, **kwargs):  # inner: runs logic
            for _ in range(n):
                func(*args, **kwargs)
        return wrapper
    return decorator

@repeat(3)
def greet(name):
    print(f"Hello, {name}!")

greet("Uday")
# Hello, Uday!
# Hello, Uday!
# Hello, Uday!
```

---

## Concept 6: Common Decorator Use Cases

| Decorator | What it does | Real example |
|:----------|:-------------|:-------------|
| `@log_action` | Print when a function is called | Debugging, audit trail |
| `@validate_not_empty` | Check args before running | Input validation |
| `@timer` | Measure execution time | Performance testing |
| `@retry(n)` | Retry on failure | Network calls |
| `@app.route(...)` | Flask — map URL to function | Web APIs |
| `@property` | Python built-in — getter/setter | You already know this! |

---

## What You Are Building Today

| Task | What it does |
|:-----|:-------------|
| `@log_action` | Logs every call with timestamp |
| `@validate_not_empty` | Guards against empty string title |
| `Task` class with `__str__` + `__repr__` | Core data class for the todo app |
| `TaskManager` class with decorated methods | Manages a list of Task objects |
| `complete_task(task_list, title)` | Marks a task done — uses both decorators |

---

## 10-Minute Read Check

You now understand:
- [ ] A decorator is a function that wraps another function
- [ ] `@my_decorator` is shorthand for `func = my_decorator(func)`
- [ ] `*args, **kwargs` lets the wrapper accept and forward any arguments
- [ ] `@wraps(func)` preserves the original function's `__name__` and `__doc__`
- [ ] Stacked decorators apply bottom-to-top
- [ ] A 3-layer structure `outer(config) → decorator(func) → wrapper(args)` handles `@repeat(n)` style

**Now open `practice.py` and write the tasks!**
