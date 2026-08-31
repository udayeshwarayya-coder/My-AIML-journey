# Day 18 — Advanced Decorators (Decorator Factories)
## Project 5: Task/Todo Manager (Part 2)

> **Revisits from Days 1–17:** `class`, `__init__`, `self`, `@property`, `__str__`, `__repr__`, `__eq__`, `*args, **kwargs`, `@wraps`, Basic Decorators (`@log_action`, `@validate_not_empty`)

---

## What You Already Know (Quick Recap)

Yesterday in Day 17, you built decorators that took only the target function:

```python
@log_action           # No parentheses, no arguments
def add_task(title):
    ...
```

**Today**: What if you want to pass parameters into your decorator itself?
- `@min_length(5)` — enforce a minimum character length on titles
- `@require_priority("low", "medium", "high")` — restrict priorities to allowed values
- `@track_history` — record every task action into an audit trail directly inside `TaskManager.history`

---

## Concept 1: The 3-Layer Structure (Decorator Factory)

To create a decorator that accepts arguments like `@min_length(5)`, you need **3 nested functions**:

```
Layer 1: Factory (accepts your configuration arguments, e.g., min_chars)
  └── Layer 2: Decorator (accepts the function being decorated, `func`)
        └── Layer 3: Wrapper (accepts the function arguments at runtime, `*args, **kwargs`)
```

### Pattern Blueprint:

```python
from functools import wraps

def min_length(n):                           # Layer 1: Config
    def decorator(func):                     # Layer 2: Receives func
        @wraps(func)
        def wrapper(*args, **kwargs):        # Layer 3: Runtime execution
            # Inspect argument (handling both standalone functions & methods)
            title = args[1] if (len(args) > 1 and not isinstance(args[0], str)) else (args[0] if args else "")
            
            if len(str(title).strip()) < n:
                print(f"❌ Error: {func.__name__} — title must be at least {n} characters.")
                return None
            return func(*args, **kwargs)
        return wrapper
    return decorator
```

### How Python Evaluates It:
When you write:
```python
@min_length(5)
def add_task(title):
    ...
```
Python actually does:
```python
# 1. Calls min_length(5) -> returns decorator
# 2. Calls decorator(add_task) -> returns wrapper
add_task = min_length(5)(add_task)
```

---

## Concept 2: Decorator with Parameterized Validation (`@require_priority`)

You can validate keyword arguments or positional arguments against an allowed list:

```python
def require_priority(*allowed_priorities):
    allowed_lower = [p.lower() for p in allowed_priorities]
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Check kwargs first, then args
            priority = kwargs.get('priority')
            if priority is None:
                # In a method: args = (self, title, priority, ...)
                if len(args) >= 3:
                    priority = args[2]
                # In a standalone function: args = (title, priority, ...)
                elif len(args) >= 2 and isinstance(args[0], str):
                    priority = args[1]
                else:
                    priority = "medium" # default if not supplied
            
            if priority and priority.lower() not in allowed_lower:
                print(f"❌ Error: Invalid priority '{priority}'. Allowed: {list(allowed_priorities)}")
                return None
            return func(*args, **kwargs)
        return wrapper
    return decorator
```

---

## Concept 3: Stateful / Method Decorators (`@track_history`)

Decorators applied to class methods receive `self` as `args[0]`. This allows decorators to record audit logs directly onto the instance!

```python
def track_history(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        result = func(self, *args, **kwargs)
        if hasattr(self, 'history'):
            timestamp = datetime.now().strftime("%H:%M:%S")
            self.history.append(f"[{timestamp}] {func.__name__} executed")
        return result
    return wrapper
```

---

## What You Are Building Today

| Component | Description |
|:----------|:------------|
| `@min_length(min_chars)` | Decorator factory guarding minimum string length |
| `@require_priority(*allowed)` | Decorator factory validating priority values |
| `@track_history` | Method decorator recording action logs on `TaskManager.history` |
| `Task` (Enhanced) | Supports `title`, `priority`, `tags` (list of strings), `done`, and `created_at` |
| `TaskManager` (Enhanced) | Manages tasks with tag filtering, priority filtering, and history log inspection |

---

## 10-Minute Read Check

You now understand:
- [x] Decorator with arguments requires 3 layers: `factory(config) -> decorator(func) -> wrapper(*args, **kwargs)`
- [x] `@min_length(5)` evaluates to `func = min_length(5)(func)`
- [x] Method decorators receive `self` as the first argument (`args[0]`)
- [x] Decorators can safely validate inputs before functions execute and update object history

**Now open `practice.py` and write your Day 18 tasks!**
