# Day 20 — Project 5 Build Day: Task/Todo Manager Website
## Project 5: Task/Todo Manager (Part 4: Build & Ship 🚀)

> **Revisits from Days 1–19:** `class`, `__init__`, `@property`, Decorators (`@timer`, `@wraps`), Generators (`yield`), `__str__`, `__repr__`

---

## What You Are Building Today

Today is **Build Day** for Project 5. You have already built all the core logic across Days 17–19:
- **Day 17:** `log_action` decorator, `create_task()`, `complete_task()`
- **Day 18:** `timer_decorator`, `priority_sort()`, `filter_by_status()`
- **Day 19:** `task_generator()`, `pending_tasks()`, `daily_summary()`

Today you add the final **3 logic functions** that power the website's dashboard and reporting, then the website goes live.

---

## Concept 1: `stats_dashboard()` — Aggregating Task Metrics

This function computes a **summary snapshot** of the entire task list — total count, completed, pending, and breakdown by priority.

```python
def stats_dashboard(tasks: list[dict]) -> dict:
    """
    Returns a statistics summary for the task list.
    
    Args:
        tasks: List of task dicts with keys: id, title, priority, status, due_date
    
    Returns:
        {
          "total": int,
          "completed": int,
          "pending": int,
          "completion_rate": float,   # 0.0 – 100.0
          "by_priority": {"high": int, "medium": int, "low": int}
        }
    """
    total = len(tasks)
    completed = sum(1 for t in tasks if t["status"] == "done")
    pending = total - completed
    completion_rate = round((completed / total * 100), 1) if total else 0.0

    by_priority = {"high": 0, "medium": 0, "low": 0}
    for t in tasks:
        priority = t.get("priority", "medium")
        by_priority[priority] = by_priority.get(priority, 0) + 1

    return {
        "total": total,
        "completed": completed,
        "pending": pending,
        "completion_rate": completion_rate,
        "by_priority": by_priority,
    }
```

**Key Pattern:** Use `sum(1 for t in tasks if condition)` — a generator expression inside `sum()` — to count items matching a condition in O(n) time without building an intermediate list.

---

## Concept 2: `overdue_tasks()` — Date Comparison & Filtering

This function identifies tasks that have **passed their due date** and are not yet completed. It introduces working with Python's `datetime` module.

```python
from datetime import date

def overdue_tasks(tasks: list[dict]) -> list[dict]:
    """
    Returns tasks that are past their due_date and still pending.
    
    Args:
        tasks: List of task dicts. Each task may have a 'due_date' key (ISO string "YYYY-MM-DD")
    
    Returns:
        List of overdue task dicts, sorted by due_date ascending (oldest first)
    """
    today = date.today()
    overdue = []
    for task in tasks:
        if task.get("status") == "done":
            continue
        due_str = task.get("due_date")
        if due_str:
            due = date.fromisoformat(due_str)  # "2025-07-15" → date object
            if due < today:
                overdue.append(task)
    
    return sorted(overdue, key=lambda t: t["due_date"])
```

**Key Patterns:**
- `date.today()` — returns current date as a `date` object
- `date.fromisoformat("YYYY-MM-DD")` — parses ISO date strings
- `continue` in a loop — skip items that don't qualify early (guard clause pattern)

---

## Concept 3: `productivity_score()` — Weighted Scoring Algorithm

This function produces a **0–100 score** that reflects the quality of work done, not just the quantity. Completing high-priority tasks matters more than completing low-priority ones.

```python
def productivity_score(tasks: list[dict]) -> float:
    """
    Calculates a weighted productivity score (0–100).
    
    Weights:
        high priority done   → 3 points
        medium priority done → 2 points
        low priority done    → 1 point
    
    Score = (points_earned / max_possible_points) × 100
    
    Returns:
        float: score between 0.0 and 100.0
    """
    WEIGHTS = {"high": 3, "medium": 2, "low": 1}

    max_points = sum(WEIGHTS.get(t["priority"], 1) for t in tasks)
    if max_points == 0:
        return 0.0

    earned_points = sum(
        WEIGHTS.get(t["priority"], 1)
        for t in tasks
        if t["status"] == "done"
    )

    return round((earned_points / max_points) * 100, 1)
```

**Key Pattern:** **Weighted scoring** — assign different weights to items based on their importance. This pattern appears constantly in ML (loss functions, class weights, feature importance).

---

## The Full Data Flow (How the Website Works)

```
Browser (Frontend)          Flask API (Backend)          Python Logic
─────────────────           ──────────────────           ─────────────
User adds task       →   POST /api/tasks          →   append to tasks list
User views stats     →   GET  /api/stats          →   stats_dashboard(tasks)
User sees overdue    →   GET  /api/overdue         →   overdue_tasks(tasks)
User sees score      →   GET  /api/score           →   productivity_score(tasks)
User sorts by prio   →   GET  /api/tasks?priority=high  → filter_by_status + priority_sort
User marks done      →   PATCH /api/tasks/<id>    →   update task["status"] = "done"
```

---

## Quick Reference Checklist

- [ ] `stats_dashboard()` aggregates total, completed, pending, and priority breakdown
- [ ] `overdue_tasks()` uses `date.fromisoformat()` to compare dates and find late tasks
- [ ] `productivity_score()` applies weighted scoring (high=3, medium=2, low=1)
- [ ] All three functions take `tasks` (a list of dicts) — the same format as the JSON store
- [ ] The website is in `project/` — backend (`app.py`) + frontend (`index.html`)
