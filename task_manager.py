import os

TASKS_FILE = "tasks5.txt"

def ensure_tasks_file_exists():
    """Ensure the tasks file exists."""
    if not os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "w") as f:
            f.write("")

ensure_tasks_file_exists()

def load_tasks():
    """Load tasks from the text file."""
    tasks = []
    try:
        with open(TASKS_FILE, "r") as f:
            lines = f.readlines()
            for line in lines:
                parts = line.strip().split(" | ")
                if len(parts) == 2:
                    tasks.append({"description": parts[0], "status": parts[1]})
                else:
                    print(f"[WARNING] Skipping invalid entry: {line.strip()}")
    except Exception as e:
        print(f"[ERROR] Failed to load tasks: {e}")
    return tasks

def save_tasks(tasks):
    """Save tasks to the text file."""
    try:
        with open(TASKS_FILE, "w") as f:
            for task in tasks:
                f.write(f"{task['description']} | {task['status']}\n")
        print("[INFO] Tasks saved.")
        commit_changes()
    except Exception as e:
        print(f"[ERROR] Failed to save tasks: {e}")

def commit_changes():
    """Commit changes using Git."""
    try:
        os.system(f'git add {TASKS_FILE}')
        os.system('git commit -m "Updated tasks file"')
        print("[INFO] Changes committed to Git.")
    except Exception as e:
        print(f"[ERROR] Git commit failed: {e}")

def add_task(description):
    """Add a new task."""
    tasks = load_tasks()
    tasks.append({"description": description, "status": "Pending"})
    save_tasks(tasks)

def complete_task(task_index):
    """Mark a task as completed."""
    tasks = load_tasks()
    try:
        tasks[task_index]["status"] = "Completed"
        save_tasks(tasks)
    except IndexError:
        print("[ERROR] Task not found.")
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")

def delete_task(task_index):
    """Delete a task."""
    tasks = load_tasks()
    try:
        del tasks[task_index]
        save_tasks(tasks)
    except IndexError:
        print("[ERROR] Task not found.")
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")

def filter_tasks(status):
    """Filter tasks based on status using match-case."""
    tasks = load_tasks()
    match status.lower():
        case "pending":
            return [task for task in tasks if task["status"] == "Pending"]
        case "completed":
            return [task for task in tasks if task["status"] == "Completed"]
        case _:  # Default case
            print("[WARNING] Invalid status. Use 'pending' or 'completed'.")
            return []
