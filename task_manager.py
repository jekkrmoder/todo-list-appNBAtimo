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
        json.dump(tasks, f, indent=4)
    print(f"[INFO] Tasks saved to {TASKS_FILE}.")
    commit_changes()


def commit_changes():
    """Minimal manual commit."""
    os.system('git add tasks.json')
    os.system('git commit -m "Updated tasks.json"')
    print("[INFO] Changes committed manually.")


def add_task(description):
    tasks = load_tasks()
    tasks.append({"description": description, "status": "Pending"})
    save_tasks(tasks)


def complete_task(task_index):
    tasks = load_tasks()
    if 0 <= task_index < len(tasks):
        tasks[task_index]["status"] = "Completed"
        save_tasks(tasks)
    else:
        print("[ERROR] Task not found.")


def delete_task(task_index):
    tasks = load_tasks()
    if 0 <= task_index < len(tasks):
        del tasks[task_index]
        save_tasks(tasks)
    else:
        print("[ERROR] Task not found.")
