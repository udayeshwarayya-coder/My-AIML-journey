# Day 19 Practice — Python Generators & yield
# Project 5: Task/Todo Manager (Part 3)
# Topic: Generators, yield, streaming data, and execution benchmarking with @timer
# Goal: Build @timer, task_id_generator, stream filters, batch generator, and Streaming TaskManager

import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import time
from functools import wraps
from datetime import datetime


# ============================================================
# TASK 1: @timer Decorator (Essential 2-Layer Decorator)
# ============================================================
# Write a 2-layer decorator that measures how long a function
# takes to execute using time.time().
#
# Requirements:
# - Use @wraps(func)
# - Record start_time = time.time() before running func
# - Call func(*args, **kwargs)
# - Calculate duration = time.time() - start_time
# - Print: "⏱ <function_name> took <duration:.5f>s"
# - Return the result of the function

def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # YOUR CODE HERE
        st=time.time()
        result=func(*args,**kwargs)
        stop=time.time()
        duration=stop-st
        print(f"⏱ {func.__name__} took {duration:.5f}s")

        return result
    return wrapper


# ============================================================
# TASK 2: task_id_generator(start=1, prefix="TASK-")
# ============================================================
# Write a generator function that produces sequential ID strings indefinitely.
#
# Example IDs produced:
#   "TASK-001", "TASK-002", "TASK-003", ...
#
# Requirements:
# - Use an infinite loop (`while True:`)
# - Yield formatted string: f"{prefix}{current_id:03d}"
# - Increment current_id after yielding

def task_id_generator(start=1, prefix="TASK-"):
    # YOUR CODE HERE
    count=start
    while True:
        yield f"{prefix}{count:03d}"
        count+=1
    


# ============================================================
# TASK 3: Stream Filtering Generators
# ============================================================
# Instead of building lists in memory, write two generator functions
# that stream matching tasks one by one using `yield`.
#
# 1. pending_tasks_generator(tasks)
#    - Loops through `tasks` list
#    - If not task.done: yield task
#
# 2. priority_tasks_generator(tasks, priority)
#    - Loops through `tasks` list
#    - If task.priority.lower() == priority.lower(): yield task

def pending_tasks_generator(tasks):
    # YOUR CODE HERE
    for t in tasks:
        if not t.done:
            yield t

def priority_tasks_generator(tasks, priority):
    # YOUR CODE HERE
    for t in tasks:
        if t.priority.lower()==priority.lower():
            yield t


# ============================================================
# TASK 4: batch_tasks(tasks, batch_size=2)
# ============================================================
# Write a generator that chunks a list of tasks into batches of size `batch_size`.
# This pattern is used across ML data loaders (e.g. PyTorch/TensorFlow).
#
# Requirements:
# - Loop with step: `range(0, len(tasks), batch_size)`
# - Yield the sub-list (slice) of tasks: `tasks[i : i + batch_size]`

def batch_tasks(tasks, batch_size=2):
    # YOUR CODE HERE
    for i in range(0,len(tasks),batch_size):
        yield tasks[i:i+batch_size]


# ============================================================
# TASK 5: Task and Streaming TaskManager Classes
# ============================================================
# Build the Task class and TaskManager class equipped with generator methods.

class Task:
    def __init__(self, task_id, title, priority="medium", done=False):
        self.task_id = task_id
        self.title = title
        self.priority = priority
        self.done = done

    def __str__(self):
        icon = "✅" if self.done else "⬜"
        status = "done" if self.done else "pending"
        return f"[{icon}] {self.task_id}: {self.title} ({self.priority}) — {status}"

    def __repr__(self):
        return f'Task(task_id="{self.task_id}", title="{self.title}", priority="{self.priority}", done={self.done})'


class TaskManager:
    def __init__(self):
        self.tasks = []
        self._id_gen = task_id_generator(start=1, prefix="TASK-")

    def add_task(self, title, priority="medium"):
        """Generates next task ID, creates Task, and appends to self.tasks."""
        task_id = next(self._id_gen)
        task = Task(task_id, title, priority)
        self.tasks.append(task)
        print(f"Task '{task.title}' added with ID: {task.task_id}")
        return task

    def complete_task(self, task_id_or_title):
        """Marks a task complete by ID or title (case-insensitive)."""
        for t in self.tasks:
            if t.task_id.lower() == task_id_or_title.lower() or t.title.lower() == task_id_or_title.lower():
                t.done = True
                print(f"Task {t.task_id} marked complete! ✅")
                return True
        print(f"Task '{task_id_or_title}' not found.")
        return False

    def iter_pending(self):
        """Generator method: yields pending tasks one by one."""
        # YOUR CODE HERE
        for t in pending_tasks_generator(self.tasks):
            yield t

    def iter_by_priority(self, priority):
        """Generator method: yields tasks matching priority."""
        # YOUR CODE HERE
        for t in priority_tasks_generator(self.tasks,priority):
            yield t

    def stream_batches(self, batch_size=2):
        """Generator method: yields task batches of size batch_size."""
        # YOUR CODE HERE
        for t in batch_tasks(self.tasks,batch_size):
            yield t

    @timer
    def process_all_tasks(self):
        """Simulates processing all tasks and measures time with @timer."""
        completed_count = 0
        for task in self.tasks:
            # Simulate a quick operation
            time.sleep(0.01)
            completed_count += 1
        return completed_count


# ============================================================
# TEST YOUR CODE — run: python practice.py
# ============================================================

if __name__ == "__main__":

    # ── Test 1: @timer Decorator ─────────────────────────────
    print("=== Test 1: @timer Decorator ===")

    @timer
    def simulate_work(duration):
        time.sleep(duration)
        return "Work finished"

    res = simulate_work(0.05)
    print("Result:", res)


    # ── Test 2: task_id_generator ────────────────────────────
    print("\n=== Test 2: task_id_generator ===")
    id_gen = task_id_generator(start=1, prefix="TASK-")
    print(next(id_gen))  # TASK-001
    print(next(id_gen))  # TASK-002
    print(next(id_gen))  # TASK-003


    # ── Test 3: Stream Filtering Generators ──────────────────
    print("\n=== Test 3: Stream Filtering Generators ===")
    sample_tasks = [
        Task("TASK-001", "Learn Generators", "high", done=False),
        Task("TASK-002", "Buy groceries", "low", done=True),
        Task("TASK-003", "Build ML Pipeline", "high", done=False),
        Task("TASK-004", "Workout", "medium", done=False),
    ]

    print("-- Pending Tasks (Streamed via yield) --")
    for t in pending_tasks_generator(sample_tasks):
        print("Streamed:", t)

    print("\n-- High Priority Tasks (Streamed via yield) --")
    for t in priority_tasks_generator(sample_tasks, "high"):
        print("Streamed:", t)


    # ── Test 4: Batch Task Generator (ML Pattern) ────────────
    print("\n=== Test 4: Batch Task Generator ===")
    for batch_num, batch in enumerate(batch_tasks(sample_tasks, batch_size=2), start=1):
        print(f"Batch #{batch_num} ({len(batch)} tasks): {[t.task_id for t in batch]}")


    # ── Test 5: TaskManager Integration ──────────────────────
    print("\n=== Test 5: Streaming TaskManager ===")
    mgr = TaskManager()
    mgr.add_task("Review OOP Principles", "high")
    mgr.add_task("Solve LeetCode Problem", "medium")
    mgr.add_task("Read PyTorch Docs", "high")
    mgr.add_task("Fix Bug in App", "low")

    # Complete one task
    mgr.complete_task("TASK-002")

    print("\n-- Iterating Pending Tasks from Manager --")
    for task in mgr.iter_pending():
        print(task)

    print("\n-- Streaming Batches from Manager --")
    for batch in mgr.stream_batches(batch_size=2):
        print("Manager Batch:", [t.title for t in batch])

    print("\n-- Benchmarking with @timer --")
    count = mgr.process_all_tasks()
    print(f"Processed {count} tasks.")
