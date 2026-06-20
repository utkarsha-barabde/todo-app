from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)
TASKS_FILE = "tasks.json"


def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, "r") as f:
        return json.load(f)


def save_tasks(tasks):
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=2)


@app.route("/")
def index():
    tasks = load_tasks()
    return render_template("index.html", tasks=tasks)


@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title", "").strip()
    if title:
        tasks = load_tasks()
        tasks.append({"title": title, "done": False, "subtasks": []})
        save_tasks(tasks)
    return redirect(url_for("index"))


@app.route("/done/<int:index>")
def done(index):
    tasks = load_tasks()
    if 0 <= index < len(tasks):
        tasks[index]["done"] = True
        save_tasks(tasks)
    return redirect(url_for("index"))


@app.route("/delete/<int:index>")
def delete(index):
    tasks = load_tasks()
    if 0 <= index < len(tasks):
        tasks.pop(index)
        save_tasks(tasks)
    return redirect(url_for("index"))


@app.route("/add_subtask/<int:task_index>", methods=["POST"])
def add_subtask(task_index):
    title = request.form.get("subtask_title", "").strip()
    tasks = load_tasks()
    if title and 0 <= task_index < len(tasks):
        if "subtasks" not in tasks[task_index]:
            tasks[task_index]["subtasks"] = []
        tasks[task_index]["subtasks"].append({"title": title, "done": False})
        save_tasks(tasks)
    return redirect(url_for("index"))


@app.route("/done_subtask/<int:task_index>/<int:sub_index>")
def done_subtask(task_index, sub_index):
    tasks = load_tasks()
    if 0 <= task_index < len(tasks):
        subtasks = tasks[task_index].get("subtasks", [])
        if 0 <= sub_index < len(subtasks):
            subtasks[sub_index]["done"] = True
            save_tasks(tasks)
    return redirect(url_for("index"))


@app.route("/delete_subtask/<int:task_index>/<int:sub_index>")
def delete_subtask(task_index, sub_index):
    tasks = load_tasks()
    if 0 <= task_index < len(tasks):
        subtasks = tasks[task_index].get("subtasks", [])
        if 0 <= sub_index < len(subtasks):
            subtasks.pop(sub_index)
            save_tasks(tasks)
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
