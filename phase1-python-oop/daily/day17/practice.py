# Day 17 Practice — Python Decorators
# Project 5: Task/Todo Manager (Part 1)
# Topic: Writing your own decorators, @wraps, stacking decorators
# Goal: Build @log_action, @validate_not_empty, Task class, TaskManager class

import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from functools import wraps
from datetime import datetime


# ============================================================
# TASK 1: @log_action decorator
# ============================================================
# Write a decorator that prints a log line every time the
# decorated function is called.
#
# Log format:  [LOG] <function_name> called at HH:MM:SS
#
# Requirements:
# - Use @wraps(func) to preserve the function's name
# - Use datetime.now().strftime("%H:%M:%S") for the time
# - Must forward all args and kwargs to the original function
# - Must return whatever the original function returns
#
# Expected output when @log_action is applied to add_task():
#   [LOG] add_task called at 13:07:42
#   Task 'Study OOP' added.

def log_action(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        time_str = datetime.now().strftime("%H:%M:%S")
        print(f"[LOG] {func.__name__} called at {time_str}")
        return func(*args, **kwargs)
    return wrapper


# ============================================================
# TASK 2: @validate_not_empty decorator
# ============================================================
# Write a decorator that checks the FIRST positional argument.
# If it is an empty string or only whitespace:
#   → Print: "❌ Error: <function_name> — title cannot be empty."
#   → Do NOT call the original function, return None.
# If it is valid, call the original function normally.
#
# Hint: args[0] is the first positional argument.
# Use str(args[0]).strip() == "" to detect empty/whitespace.
#
# Expected:
#   add_task(tasks, "")       → ❌ Error: add_task — title cannot be empty.
#   add_task(tasks, "   ")    → ❌ Error: add_task — title cannot be empty.
#   add_task(tasks, "Study")  → Task 'Study' added.

def validate_not_empty(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # In a method, args[0] is self and title is args[1]
        # In a standalone function, title is args[0]
        arg_to_check = args[1] if (len(args) > 1 and not isinstance(args[0], str)) else (args[0] if args else "")
        if str(arg_to_check).strip() == "":
            print(f"❌ Error: {func.__name__} — title cannot be empty.")
            return None
        return func(*args, **kwargs)
    return wrapper


# ============================================================
# TASK 3: Task class
# ============================================================
# Build a Task class to represent one to-do item.
#
# Attributes:
#   self.title      (str)  — task description
#   self.priority   (str)  — "low", "medium", or "high"   default: "medium"
#   self.done       (bool) — False by default
#   self.created_at (datetime) — datetime.now() at creation
#
# __str__  → human-friendly one-liner, example:
#   "[✅] Study OOP (high) — done"
#   "[⬜] Buy groceries (medium) — pending"
#
# __repr__ → developer string that could recreate the object, example:
#   Task(title="Study OOP", priority="high", done=True)
#
# __eq__   → two Tasks are equal if they have the same title (case-insensitive)

class Task:
    def __init__(self, title, priority="medium", done=False):
        self.title = title
        self.priority = priority
        self.done = done
        self.created_at = datetime.now()

    def __str__(self):
        icon = "✅" if self.done else "⬜"
        status = "done" if self.done else "pending"
        return f"[{icon}] {self.title} ({self.priority}) — {status}"

    def __repr__(self):
        return f'Task(title="{self.title}", priority="{self.priority}", done={self.done})'

    def __eq__(self, other):
        if isinstance(other, Task):
            return self.title.lower() == other.title.lower()
        return False


# ============================================================
# TASK 4: TaskManager class
# ============================================================
# Build a TaskManager class that holds a list of Task objects
# and provides methods to manage them.
#
# Attributes:
#   self.tasks  (list of Task)
#
# Methods:
#
# add_task(self, title, priority="medium")
#   → Decorated with @log_action AND @validate_not_empty
#   → If a task with the same title already exists: print a warning, don't add
#   → Otherwise: create a Task and append to self.tasks
#   → Print: "Task '<title>' added."
#
# complete_task(self, title)
#   → Decorated with @log_action
#   → Find the task by title (case-insensitive)
#   → If found: set task.done = True, print: "Task '<title>' marked complete! ✅"
#   → If not found: print: "Task '<title>' not found."
#
# delete_task(self, title)
#   → Decorated with @log_action
#   → Remove the task with matching title (case-insensitive)
#   → If found: print: "Task '<title>' deleted."
#   → If not found: print: "Task '<title>' not found."
#
# show_all(self)
#   → Print all tasks using their __str__
#   → If list is empty: print "No tasks yet."
#
# show_pending(self)
#   → Print only tasks where done == False
#   → If none: print "All tasks are done! 🎉"
#
# summary(self)
#   → Print: "Total: X | Done: Y | Pending: Z"

class TaskManager:
    def __init__(self):
        self.tasks = []

    @log_action
    @validate_not_empty
    def add_task(self, title, priority="medium"):
        for t in self.tasks:
            if t.title.lower() == title.lower():
                print(f"⚠ Task '{title}' already exists.")
                return
        self.tasks.append(Task(title, priority))
        print(f"Task '{title}' added.")

    @log_action
    def complete_task(self, title):
        for t in self.tasks:
            if t.title.lower() == title.lower():
                t.done = True
                print(f"Task '{title}' marked complete! ✅")
                return
        print(f"Task '{title}' not found.")

    @log_action
    def delete_task(self, title):
        for t in self.tasks:
            if t.title.lower() == title.lower():
                self.tasks.remove(t)
                print(f"Task '{title}' deleted.")
                return
        print(f"Task '{title}' not found.")

    def show_all(self):
        if self.tasks:
            for t in self.tasks:
                print(t)
        else:
            print("No tasks yet.")

    def show_pending(self):
        pending = [t for t in self.tasks if not t.done]
        if pending:
            for t in pending:
                print(t)
        else:
            print("All tasks are done! 🎉")

    def summary(self):
        total = len(self.tasks)
        done = sum(1 for t in self.tasks if t.done)
        pending = total - done
        print(f"Total: {total} | Done: {done} | Pending: {pending}")



# ============================================================
# BONUS TASK: @timer decorator
# ============================================================
# Write a decorator that measures and prints how long the
# decorated function takes to run.
#
# Print format:  ⏱ <function_name> took 0.0003s
#
# Hint: use time.time() before and after calling the function.

import time

def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        duration = time.time() - start
        print(f"⏱ {func.__name__} took {duration:.4f}s")
        return result
    return wrapper


# ============================================================
# TEST YOUR CODE — run: python practice.py
# ============================================================

if __name__ == "__main__":

    # ── Test @log_action ─────────────────────────────────────
    print("=== @log_action ===")

    @log_action
    def greet(name):
        print(f"Hello, {name}!")

    greet("Uday")
    # Expected:
    # [LOG] greet called at HH:MM:SS
    # Hello, Uday!

    # ── Test @validate_not_empty ─────────────────────────────
    print("\n=== @validate_not_empty ===")

    tasks_raw = []

    @log_action
    @validate_not_empty
    def add_task_raw(title):
        tasks_raw.append(title)
        print(f"Task '{title}' added.")

    add_task_raw("")          # ❌ Error: add_task_raw — title cannot be empty.
    add_task_raw("   ")       # ❌ Error: add_task_raw — title cannot be empty.
    add_task_raw("Study OOP") # [LOG] ... then → Task 'Study OOP' added.
    print(f"Tasks in list: {len(tasks_raw)}")   # 1

    # ── Test Task class ──────────────────────────────────────
    print("\n=== Task class ===")
    t1 = Task("Study decorators", "high")
    t2 = Task("Buy groceries")
    t3 = Task("Read chapter 5", "low")

    print(t1)   # [⬜] Study decorators (high) — pending
    print(t2)   # [⬜] Buy groceries (medium) — pending
    print(repr(t1))
    # Task(title="Study decorators", priority="high", done=False)

    t1.done = True
    print(t1)   # [✅] Study decorators (high) — done

    print(t1 == Task("STUDY DECORATORS", "low"))  # True  (case-insensitive)
    print(t1 == t2)                                # False

    # ── Test TaskManager ─────────────────────────────────────
    print("\n=== TaskManager ===")
    manager = TaskManager()

    manager.add_task("Study decorators", "high")
    # [LOG] add_task called at HH:MM:SS
    # Task 'Study decorators' added.

    manager.add_task("Buy groceries")
    # [LOG] add_task called at HH:MM:SS
    # Task 'Buy groceries' added.

    manager.add_task("")
    # ❌ Error: add_task — title cannot be empty.

    manager.add_task("Study decorators")
    # ⚠ Task 'Study decorators' already exists.

    print("\n-- show_all --")
    manager.show_all()
    # [⬜] Study decorators (high) — pending
    # [⬜] Buy groceries (medium) — pending

    print("\n-- complete_task --")
    manager.complete_task("Study decorators")
    # [LOG] complete_task called at HH:MM:SS
    # Task 'Study decorators' marked complete! ✅

    manager.complete_task("Nonexistent task")
    # [LOG] complete_task called at HH:MM:SS
    # Task 'Nonexistent task' not found.

    print("\n-- show_pending --")
    manager.show_pending()
    # [⬜] Buy groceries (medium) — pending

    print("\n-- delete_task --")
    manager.delete_task("Buy groceries")
    # [LOG] delete_task called at HH:MM:SS
    # Task 'Buy groceries' deleted.

    print("\n-- summary --")
    manager.summary()
    # Total: 1 | Done: 1 | Pending: 0

    print("\n-- show_pending after all done --")
    manager.show_pending()
    # All tasks are done! 🎉

    # ── Test __wraps__ preserved ─────────────────────────────
    print("\n=== @wraps check ===")
    print(manager.add_task.__name__)      # add_task  (not 'wrapper')
    print(manager.complete_task.__name__) # complete_task
