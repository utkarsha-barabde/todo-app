import json
import os

TASKS_FILE = "tasks.json"


def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, "r") as f:
        return json.load(f)


def save_tasks(tasks):
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=2)


def add_task(title):
    tasks = load_tasks()
    task = {"title": title, "done": False}
    tasks.append(task)
    save_tasks(tasks)
    print(f"Task added: {title}")


def view_tasks():
    tasks = load_tasks()
    if not tasks:
        print("No tasks yet.")
        return
    for i, task in enumerate(tasks, start=1):
        status = "x" if task["done"] else " "
        print(f"{i}. [{status}] {task['title']}")


def delete_task(number):
    tasks = load_tasks()
    if number < 1 or number > len(tasks):
        print("Invalid task number.")
        return
    removed = tasks.pop(number - 1)
    save_tasks(tasks)
    print(f"Deleted: {removed['title']}")


def complete_task(number):
    tasks = load_tasks()
    if number < 1 or number > len(tasks):
        print("Invalid task number.")
        return
    tasks[number - 1]["done"] = True
    save_tasks(tasks)
    print(f"Marked as done: {tasks[number - 1]['title']}")


def print_help():
    print("Usage:")
    print("  python3 todo.py add <task>       Add a new task")
    print("  python3 todo.py list             View all tasks")
    print("  python3 todo.py done <number>    Mark a task as done")
    print("  python3 todo.py delete <number>  Delete a task")


import sys

if __name__ == "__main__":
    args = sys.argv[1:]

    if not args:
        print_help()
    elif args[0] == "add" and len(args) > 1:
        add_task(" ".join(args[1:]))
    elif args[0] == "list":
        view_tasks()
    elif args[0] == "done" and len(args) > 1:
        complete_task(int(args[1]))
    elif args[0] == "delete" and len(args) > 1:
        delete_task(int(args[1]))
    else:
        print("Unknown command.")
        print_help()
