# Day 18 Practice — Advanced Decorators (Decorator Factories)
# Project 5: Task/Todo Manager (Part 2)
# Topic: Decorators with arguments, Stateful/Method decorators, Tagging & Filtering
# Goal: Build @min_length, @require_priority, @track_history, enhanced Task & TaskManager

import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from functools import wraps
from datetime import datetime


# ============================================================
# TASK 1: @min_length(n) Decorator Factory
# ============================================================
# Write a decorator that takes an integer `n` as an argument.
# It checks if the task title has at least `n` characters (excluding leading/trailing whitespace).
#
# Requirements:
# - 3-layer structure: min_length(n) -> decorator(func) -> wrapper(*args, **kwargs)
# - Use @wraps(func)
# - If len(str(title).strip()) < n:
#     Print: "❌ Error: <function_name> — title must be at least <n> characters."
#     Return None (do not call the original function)
# - Otherwise: call func(*args, **kwargs) and return the result
#
# Hint: In standalone functions, title is args[0].
# In class methods, title is args[1] (since args[0] is self).

def min_length(n):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            title = kwargs.get('title') if 'title' in kwargs else (
                args[1] if (len(args) > 1 and not isinstance(args[0], str)) else (args[0] if args else "")
            )
            if len(str(title).strip()) < n:
                print(f"❌ Error: {func.__name__} — title must be at least {n} characters.")
                return None
            return func(*args, **kwargs)
        return wrapper
    return decorator


# ============================================================
# TASK 2: @require_priority(*allowed_priorities) Decorator Factory
# ============================================================
# Write a decorator that takes valid priority strings as arguments
# (e.g. @require_priority("low", "medium", "high")).
#
# Requirements:
# - Case-insensitive check: "HIGH", "High", "high" are all valid if "high" is allowed.
# - If priority is passed via kwargs: kwargs.get('priority')
# - If priority is passed positionally:
#     - Standalone function: args[1] if len(args) >= 2
#     - Class method: args[2] if len(args) >= 3
#     - Default to "medium" if not specified.
# - If invalid priority:
#     Print: "❌ Error: Invalid priority '<priority>'. Allowed: <list(allowed_priorities)>"
#     Return None
# - Otherwise: call func(*args, **kwargs) and return the result

def require_priority(*allowed_priorities):
    allowed_lower = [str(p).lower() for p in allowed_priorities]
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            priority = kwargs.get('priority')
            if priority is None:
                if len(args) >= 3 and not isinstance(args[0], str):
                    priority = args[2]
                elif len(args) >= 2 and isinstance(args[0], str):
                    priority = args[1]
                else:
                    priority = "medium"

            if str(priority).lower() not in allowed_lower:
                print(f"❌ Error: Invalid priority '{priority}'. Allowed: {list(allowed_priorities)}")
                return None
            return func(*args, **kwargs)
        return wrapper
    return decorator


# ============================================================
# TASK 3: @track_history Method Decorator
# ============================================================
# Write a decorator applied to TaskManager methods.
# Every time the decorated method runs successfully:
# - If the manager object has a `history` attribute (list):
#   Record an entry in the format: "[HH:MM:SS] <function_name> — <action_detail>"
#
# Example entries in manager.history:
#   "[14:30:15] add_task — Added: 'Study OOP'"
#   "[14:30:20] complete_task — Completed: 'Study OOP'"
#
# Hint:
# wrapper(self, *args, **kwargs)
# result = func(self, *args, **kwargs)
# After calling func, append to self.history if self has attribute 'history'

def track_history(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        result = func(self, *args, **kwargs)
        if result and hasattr(self, 'history') and isinstance(self.history, list):
            timestamp = datetime.now().strftime("%H:%M:%S")
            title = kwargs.get('title') if 'title' in kwargs else (args[0] if args else "")
            if func.__name__ == "add_task":
                action_detail = f"Added: '{title}'"
            elif func.__name__ == "complete_task":
                action_detail = f"Completed: '{title}'"
            elif func.__name__ == "delete_task":
                action_detail = f"Deleted: '{title}'"
            else:
                action_detail = f"Executed on '{title}'" if title else "Executed"
            self.history.append(f"[{timestamp}] {func.__name__} — {action_detail}")
        return result
    return wrapper


# ============================================================
# TASK 4: Enhanced Task Class
# ============================================================
# Build the enhanced Task class with tags support.
#
# Attributes:
#   self.title      (str)        — task description
#   self.priority   (str)        — "low", "medium", or "high" (default: "medium")
#   self.tags       (list)       — list of strings, e.g. ["study", "python"] (default: empty list)
#   self.done       (bool)       — False by default
#   self.created_at (datetime)   — datetime.now()
#
# Methods:
#   add_tag(tag)    → add a lowercased tag string if not already present
#   has_tag(tag)    → returns True if tag (case-insensitive) is in self.tags
#
# __str__:
#   Format with tags: "[⬜] Study Decorators (high) [study, python] — pending"
#   Format without tags: "[⬜] Buy groceries (medium) — pending"
#
# __repr__:
#   Task(title="Study Decorators", priority="high", tags=['study'], done=False)
#
# __eq__:
#   Equal if titles match case-insensitively.

class Task:
    def __init__(self, title, priority="medium", tags=None, done=False):
        self.title = title
        self.priority = priority
        self.tags = [t.lower() for t in tags] if tags else []
        self.done = done
        self.created_at = datetime.now()

    def add_tag(self, tag):
        tag_lower = tag.lower()
        if tag_lower not in self.tags:
            self.tags.append(tag_lower)

    def has_tag(self, tag):
        return tag.lower() in self.tags

    def __str__(self):
        icon = "✅" if self.done else "⬜"
        status = "done" if self.done else "pending"
        if self.tags:
            tags_str = ", ".join(self.tags)
            return f"[{icon}] {self.title} ({self.priority}) [{tags_str}] — {status}"
        return f"[{icon}] {self.title} ({self.priority}) — {status}"

    def __repr__(self):
        return f'Task(title="{self.title}", priority="{self.priority}", tags={self.tags}, done={self.done})'

    def __eq__(self, other):
        if isinstance(other, Task):
            return self.title.lower() == other.title.lower()
        return False


# ============================================================
# TASK 5: Enhanced TaskManager Class
# ============================================================
# Build the enhanced TaskManager class with decorators and filtering.
#
# Attributes:
#   self.tasks   (list of Task)
#   self.history (list of str) — audit log populated by @track_history
#
# Methods:
#
# add_task(self, title, priority="medium", tags=None)
#   → Decorated with:
#       @track_history
#       @min_length(3)
#       @require_priority("low", "medium", "high")
#   → If title already exists (case-insensitive):
#       Print: "⚠ Task '<title>' already exists."
#       Return False
#   → Otherwise:
#       Create Task, append to self.tasks, print: "Task '<title>' added."
#       Return True
#
# complete_task(self, title)
#   → Decorated with @track_history
#   → If found: set done = True, print: "Task '<title>' marked complete! ✅", return True
#   → If not found: print: "Task '<title>' not found.", return False
#
# filter_by_priority(self, priority)
#   → Return list of tasks matching priority (case-insensitive)
#
# filter_by_tag(self, tag)
#   → Return list of tasks having matching tag (case-insensitive)
#
# show_history(self)
#   → Print all entries in self.history
#   → If empty, print "No history recorded yet."

class TaskManager:
    def __init__(self):
        self.tasks = []
        self.history = []

    # Apply @track_history, @min_length(3), @require_priority("low", "medium", "high")
    @track_history
    @min_length(3)
    @require_priority("low", "medium", "high")
    def add_task(self, title, priority="medium", tags=None):
        for t in self.tasks:
            if t.title.lower() == title.lower():
                print(f"⚠ Task '{title}' already exists.")
                return False
        self.tasks.append(Task(title, priority, tags))
        print(f"Task '{title}' added.")
        return True

    # Apply @track_history
    @track_history
    def complete_task(self, title):
        for t in self.tasks:
            if t.title.lower() == title.lower():
                t.done = True
                print(f"Task '{title}' marked complete! ✅")
                return True
        print(f"Task '{title}' not found.")
        return False

    def filter_by_priority(self, priority):
        return [t for t in self.tasks if t.priority.lower() == priority.lower()]

    def filter_by_tag(self, tag):
        return [t for t in self.tasks if t.has_tag(tag)]

    def show_history(self):
        if self.history:
            for entry in self.history:
                print(entry)
        else:
            print("No history recorded yet.")


# ============================================================
# TEST YOUR CODE — run: python practice.py
# ============================================================

if __name__ == "__main__":

    # ── Test 1: @min_length ──────────────────────────────────
    print("=== Test 1: @min_length ===")

    @min_length(5)
    def create_note(title):
        print(f"Note '{title}' created successfully.")

    create_note("Hi")          # ❌ Error: create_note — title must be at least 5 characters.
    create_note("Study OOP")   # Note 'Study OOP' created successfully.


    # ── Test 2: @require_priority ────────────────────────────
    print("\n=== Test 2: @require_priority ===")

    @require_priority("low", "medium", "high")
    def set_alert(message, priority="medium"):
        print(f"Alert [{priority.upper()}]: {message}")

    set_alert("Server warming up", priority="low")     # Alert [LOW]: Server warming up
    set_alert("Crash", priority="urgent")              # ❌ Error: Invalid priority 'urgent'. Allowed: ['low', 'medium', 'high']


    # ── Test 3: Enhanced Task Class ──────────────────────────
    print("\n=== Test 3: Enhanced Task Class ===")
    t1 = Task("Study Decorators", "high", ["python", "oop"])
    t2 = Task("Buy groceries", "medium")

    print(t1)  # [⬜] Study Decorators (high) [python, oop] — pending
    print(t2)  # [⬜] Buy groceries (medium) — pending

    t1.add_tag("advanced")
    print(f"Has 'python' tag? {t1.has_tag('python')}")       # True
    print(f"Has 'fitness' tag? {t1.has_tag('fitness')}")     # False


    # ── Test 4: TaskManager with History & Decorators ────────
    print("\n=== Test 4: TaskManager Integration ===")
    mgr = TaskManager()

    # Valid task additions
    mgr.add_task("Learn Python Decorators", "high", ["python", "study"])
    mgr.add_task("Buy coffee beans", "low", ["errands"])
    mgr.add_task("Gym Workout", "medium", ["health"])

    # Invalid: Too short (< 3 chars)
    mgr.add_task("Go")   # ❌ Error: add_task — title must be at least 3 characters.

    # Invalid: Priority not allowed
    mgr.add_task("Fix production bug", "critical") # ❌ Error: Invalid priority 'critical'. Allowed: ['low', 'medium', 'high']

    # Complete a task
    mgr.complete_task("Buy coffee beans")

    # Filter tests
    print("\n-- Filter by priority: 'high' --")
    high_tasks = mgr.filter_by_priority("high")
    for t in high_tasks:
        print(t)

    print("\n-- Filter by tag: 'study' --")
    study_tasks = mgr.filter_by_tag("study")
    for t in study_tasks:
        print(t)

    # History audit check
    print("\n-- TaskManager History --")
    mgr.show_history()
