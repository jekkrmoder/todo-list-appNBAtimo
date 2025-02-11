import os

TASKS_FILE = "tasks.txt"

# Load tasks from the file
def load_tasks():
    try:
        with open(TASKS_FILE, "r") as f:
            lines = f.readlines()
    except FileNotFoundError:
        return []

    def parse_task_line(line):
        parts = line.split("|")
        return {"description": parts[0], "status": parts[1]}

    return [parse_task_line(line.strip()) for line in lines if line.strip()]

# Save tasks to the file
def save_tasks(tasks):
    with open(TASKS_FILE, "w") as f:
        for task in tasks:
            f.write(f"{task['description']}|{task['status']}\n")

# Utility function to create a task
def create_task(description="Untitled Task", status="Pending"):
    return {"description": description, "status": status}
