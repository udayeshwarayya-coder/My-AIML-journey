# Project 5: Task/Todo Manager — Flask Backend
# Day 20 Build Day
# 
# Concepts covered: Decorators, Generators, stats_dashboard, overdue_tasks, productivity_score
# Run: python app.py  (from this directory)

from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import date, datetime
import uuid
from datetime import timedelta

app = Flask(__name__)
CORS(app)

# ─── In-memory task store ──────────────────────────────────────────────────────
tasks: list[dict] = []

# Seed with some example tasks so the UI isn't empty on first load
def _seed():
    today_str = date.today().isoformat()
    yesterday = (date.today() - timedelta(days=1)).isoformat()
    tasks.extend([
        {"id": str(uuid.uuid4()), "title": "Design the database schema",     "priority": "high",   "status": "done",    "due_date": yesterday, "created_at": today_str},
        {"id": str(uuid.uuid4()), "title": "Write unit tests for API",        "priority": "medium", "status": "done",    "due_date": today_str, "created_at": today_str},
        {"id": str(uuid.uuid4()), "title": "Review pull requests",            "priority": "high",   "status": "pending", "due_date": yesterday, "created_at": today_str},
        {"id": str(uuid.uuid4()), "title": "Update project documentation",    "priority": "low",    "status": "pending", "due_date": today_str, "created_at": today_str},
        {"id": str(uuid.uuid4()), "title": "Fix login page validation bug",   "priority": "high",   "status": "pending", "due_date": today_str, "created_at": today_str},
        {"id": str(uuid.uuid4()), "title": "Team standup meeting",            "priority": "medium", "status": "done",    "due_date": today_str, "created_at": today_str},
    ])

_seed()


# ─── Day 20 Logic Functions ───────────────────────────────────────────────────

def stats_dashboard(task_list: list[dict]) -> dict:
    """
    Returns a statistics summary for the task list.
    Concept: generator expression inside sum() for efficient counting.
    """
    total = len(task_list)
    completed = sum(1 for t in task_list if t["status"] == "done")
    pending = total - completed
    completion_rate = round((completed / total * 100), 1) if total else 0.0

    by_priority = {"high": 0, "medium": 0, "low": 0}
    for t in task_list:
        p = t.get("priority", "medium")
        by_priority[p] = by_priority.get(p, 0) + 1

    return {
        "total": total,
        "completed": completed,
        "pending": pending,
        "completion_rate": completion_rate,
        "by_priority": by_priority,
    }


def overdue_tasks(task_list: list[dict]) -> list[dict]:
    """
    Returns tasks that are past their due_date and still pending.
    Concept: date.fromisoformat() + guard clause (continue) pattern.
    """
    today = date.today()
    overdue = []
    for task in task_list:
        if task.get("status") == "done":
            continue
        due_str = task.get("due_date")
        if due_str:
            due = date.fromisoformat(due_str)
            if due < today:
                overdue.append(task)
    return sorted(overdue, key=lambda t: t["due_date"])


def productivity_score(task_list: list[dict]) -> float:
    """
    Calculates a weighted productivity score (0–100).
    Weights: high=3, medium=2, low=1.
    Concept: weighted scoring algorithm (mirrors ML loss weighting).
    """
    WEIGHTS = {"high": 3, "medium": 2, "low": 1}
    max_points = sum(WEIGHTS.get(t["priority"], 1) for t in task_list)
    if max_points == 0:
        return 0.0
    earned = sum(
        WEIGHTS.get(t["priority"], 1)
        for t in task_list
        if t["status"] == "done"
    )
    return round((earned / max_points) * 100, 1)


# ─── API Routes ───────────────────────────────────────────────────────────────

@app.route("/api/tasks", methods=["GET"])
def get_tasks():
    """Return tasks, optionally filtered by priority or status."""
    priority = request.args.get("priority")
    status   = request.args.get("status")
    result = tasks
    if priority:
        result = [t for t in result if t["priority"] == priority]
    if status:
        result = [t for t in result if t["status"] == status]
    # Sort: high → medium → low, then by created_at desc
    order = {"high": 0, "medium": 1, "low": 2}
    result = sorted(result, key=lambda t: (order.get(t["priority"], 1), t["created_at"]), reverse=False)
    return jsonify(result)


@app.route("/api/tasks", methods=["POST"])
def add_task():
    """Create a new task."""
    data = request.get_json()
    if not data or not data.get("title"):
        return jsonify({"error": "title is required"}), 400
    task = {
        "id":         str(uuid.uuid4()),
        "title":      data["title"].strip(),
        "priority":   data.get("priority", "medium"),
        "status":     "pending",
        "due_date":   data.get("due_date", ""),
        "created_at": date.today().isoformat(),
    }
    tasks.append(task)
    return jsonify(task), 201


@app.route("/api/tasks/<task_id>", methods=["PATCH"])
def update_task(task_id):
    """Toggle done/pending status or update fields."""
    task = next((t for t in tasks if t["id"] == task_id), None)
    if not task:
        return jsonify({"error": "Task not found"}), 404
    data = request.get_json() or {}
    if "status" in data:
        task["status"] = data["status"]
    if "priority" in data:
        task["priority"] = data["priority"]
    if "title" in data:
        task["title"] = data["title"]
    return jsonify(task)


@app.route("/api/tasks/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    """Delete a task by ID."""
    global tasks
    before = len(tasks)
    tasks = [t for t in tasks if t["id"] != task_id]
    if len(tasks) == before:
        return jsonify({"error": "Task not found"}), 404
    return jsonify({"deleted": task_id})


@app.route("/api/stats", methods=["GET"])
def get_stats():
    """Dashboard statistics — uses stats_dashboard() logic function."""
    return jsonify(stats_dashboard(tasks))


@app.route("/api/overdue", methods=["GET"])
def get_overdue():
    """Overdue tasks — uses overdue_tasks() logic function."""
    return jsonify(overdue_tasks(tasks))


@app.route("/api/score", methods=["GET"])
def get_score():
    """Productivity score — uses productivity_score() logic function."""
    score = productivity_score(tasks)
    return jsonify({"score": score})


@app.route("/api/daily-report", methods=["GET"])
def daily_report():
    """Full daily report combining all three logic functions."""
    stats  = stats_dashboard(tasks)
    overdue = overdue_tasks(tasks)
    score  = productivity_score(tasks)
    return jsonify({
        "date":              date.today().isoformat(),
        "stats":             stats,
        "overdue_count":     len(overdue),
        "overdue_tasks":     overdue,
        "productivity_score": score,
    })


# ─── Run ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("Task Manager API running at http://localhost:5000")
    app.run(debug=True, port=5000)
