from datetime import datetime, date
from pathlib import Path
import os
import sqlite3

from flask import Flask, jsonify, request, render_template

app = Flask(__name__)
DB_PATH = Path(os.environ.get("DATABASE_PATH", Path(__file__).with_name("tasks.db")))

CATEGORIES = ["AWS", "Jenkins", "Docker", "Kubernetes", "Linux", "CI/CD", "Monitoring", "Terraform"]
STATUSES = ["todo", "in_progress", "completed"]
PRIORITIES = ["low", "medium", "high", "critical"]


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT NOT NULL DEFAULT '',
                category TEXT NOT NULL DEFAULT 'General',
                priority TEXT NOT NULL DEFAULT 'medium',
                status TEXT NOT NULL DEFAULT 'todo',
                due_date TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        """)
        count = conn.execute("SELECT COUNT(*) FROM tasks").fetchone()[0]
        if count == 0:
            now = datetime.now().isoformat(timespec="seconds")
            samples = [
                ("Configure Jenkins pipeline for Flask application", "Create a declarative pipeline with checkout, test, build and deploy stages.", "Jenkins", "high", "in_progress", date.today().isoformat()),
                ("Create an ECR repository", "Create a private container registry for application images.", "AWS", "medium", "todo", None),
                ("Dockerize the Flask application", "Build and test a production-ready Docker image.", "Docker", "high", "todo", None),
                ("Configure EC2 security groups", "Allow only required inbound traffic and restrict SSH access.", "AWS", "critical", "todo", None),
                ("Write unit tests for health endpoint", "Validate the application health API and response codes.", "CI/CD", "medium", "completed", None),
                ("Configure CloudWatch log monitoring", "Review application logs and create a basic metric filter.", "Monitoring", "low", "todo", None),
            ]
            conn.executemany("""
                INSERT INTO tasks (title, description, category, priority, status, due_date, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, [(*task, now, now) for task in samples])


def task_dict(row):
    return dict(row)


@app.get("/")
def home():
    return render_template("index.html", categories=CATEGORIES)


@app.get("/health")
def health():
    try:
        with get_db() as conn:
            conn.execute("SELECT 1")
        return jsonify(status="healthy", application="devops-operations-dashboard", database="connected"), 200
    except sqlite3.Error:
        return jsonify(status="unhealthy", database="disconnected"), 503


@app.get("/api/tasks")
def get_tasks():
    status = request.args.get("status", "").strip()
    category = request.args.get("category", "").strip()
    search = request.args.get("search", "").strip()

    query = "SELECT * FROM tasks WHERE 1=1"
    params = []
    if status and status in STATUSES:
        query += " AND status = ?"
        params.append(status)
    if category and category in CATEGORIES:
        query += " AND category = ?"
        params.append(category)
    if search:
        query += " AND (title LIKE ? OR description LIKE ?)"
        params.extend([f"%{search}%", f"%{search}%"])
    query += """
        ORDER BY CASE priority
            WHEN 'critical' THEN 1 WHEN 'high' THEN 2
            WHEN 'medium' THEN 3 ELSE 4 END,
            CASE WHEN due_date IS NULL THEN 1 ELSE 0 END,
            due_date ASC, created_at DESC
    """
    with get_db() as conn:
        rows = conn.execute(query, params).fetchall()
    return jsonify([task_dict(row) for row in rows])


@app.get("/api/stats")
def get_stats():
    today = date.today().isoformat()
    with get_db() as conn:
        total = conn.execute("SELECT COUNT(*) FROM tasks").fetchone()[0]
        todo = conn.execute("SELECT COUNT(*) FROM tasks WHERE status='todo'").fetchone()[0]
        progress = conn.execute("SELECT COUNT(*) FROM tasks WHERE status='in_progress'").fetchone()[0]
        completed = conn.execute("SELECT COUNT(*) FROM tasks WHERE status='completed'").fetchone()[0]
        overdue = conn.execute("""
            SELECT COUNT(*) FROM tasks
            WHERE due_date IS NOT NULL AND due_date < ? AND status != 'completed'
        """, (today,)).fetchone()[0]
    return jsonify(total=total, todo=todo, in_progress=progress,
                   completed=completed, overdue=overdue,
                   completion_rate=round((completed / total) * 100) if total else 0)


@app.post("/api/tasks")
def create_task():
    data = request.get_json(silent=True) or {}
    title = (data.get("title") or "").strip()
    if not title:
        return jsonify(error="Task title is required"), 400
    category = data.get("category", "AWS")
    priority = data.get("priority", "medium")
    due_date = data.get("due_date") or None
    if category not in CATEGORIES:
        return jsonify(error="Invalid category"), 400
    if priority not in PRIORITIES:
        return jsonify(error="Invalid priority"), 400
    if due_date:
        try:
            date.fromisoformat(due_date)
        except ValueError:
            return jsonify(error="Due date must use YYYY-MM-DD format"), 400

    now = datetime.now().isoformat(timespec="seconds")
    with get_db() as conn:
        cursor = conn.execute("""
            INSERT INTO tasks (title, description, category, priority, status, due_date, created_at, updated_at)
            VALUES (?, ?, ?, ?, 'todo', ?, ?, ?)
        """, (title, (data.get("description") or "").strip(), category, priority, due_date, now, now))
        task = conn.execute("SELECT * FROM tasks WHERE id=?", (cursor.lastrowid,)).fetchone()
    return jsonify(task_dict(task)), 201


@app.patch("/api/tasks/<int:task_id>")
def update_task(task_id):
    data = request.get_json(silent=True) or {}
    allowed = {"title", "description", "category", "priority", "status", "due_date"}
    updates = {key: value for key, value in data.items() if key in allowed}
    if not updates:
        return jsonify(error="No valid fields supplied"), 400
    if "title" in updates:
        updates["title"] = (updates["title"] or "").strip()
        if not updates["title"]:
            return jsonify(error="Task title cannot be empty"), 400
    if "category" in updates and updates["category"] not in CATEGORIES:
        return jsonify(error="Invalid category"), 400
    if "priority" in updates and updates["priority"] not in PRIORITIES:
        return jsonify(error="Invalid priority"), 400
    if "status" in updates and updates["status"] not in STATUSES:
        return jsonify(error="Invalid status"), 400
    if "due_date" in updates and updates["due_date"]:
        try:
            date.fromisoformat(updates["due_date"])
        except ValueError:
            return jsonify(error="Due date must use YYYY-MM-DD format"), 400

    updates["updated_at"] = datetime.now().isoformat(timespec="seconds")
    assignments = ", ".join(f"{key}=?" for key in updates)
    values = list(updates.values()) + [task_id]
    with get_db() as conn:
        cursor = conn.execute(f"UPDATE tasks SET {assignments} WHERE id=?", values)
        if cursor.rowcount == 0:
            return jsonify(error="Task not found"), 404
        task = conn.execute("SELECT * FROM tasks WHERE id=?", (task_id,)).fetchone()
    return jsonify(task_dict(task))


@app.delete("/api/tasks/<int:task_id>")
def delete_task(task_id):
    with get_db() as conn:
        cursor = conn.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    if cursor.rowcount == 0:
        return jsonify(error="Task not found"), 404
    return jsonify(message="Task deleted")


init_db()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False)
