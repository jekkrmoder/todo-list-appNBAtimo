import tkinter as tk
import os
from threading import Thread
from flask import Flask, request, jsonify, render_template_string

TASKS_FILE = "tasks4.txt"

app = Flask(__name__)
tasks = []

def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, "r") as f:
        lines = f.readlines()
        loaded_tasks = [
            (description.strip(), status.strip())  # Tuple usage for task representation
            for line in lines if " | " in line.strip()
            for description, status in [line.strip().split(" | ", 1)]
        ]
        return [
            {"description": description, "status": status}
            for description, status in loaded_tasks
        ]


def save_tasks(tasks):
    with open(TASKS_FILE, "w") as f:
        for task in tasks:
            f.write(f"{task['description']} | {task['status']}\n")

def fix_tasks_file():
    with open(TASKS_FILE, "r") as file:
        lines = file.readlines()
    with open(TASKS_FILE, "w") as file:
        for line in lines:
            if "|" in line:
                fixed_line = " | ".join(part.strip() for part in line.split("|"))
                file.write(f"{fixed_line}\n")
            else:
                file.write(line)


def update_gui():
    listbox.delete(0, tk.END)
    for i, task in enumerate(tasks):
        text = task["description"]
        listbox.insert(tk.END, text)
        if task["status"] == "Completed":
            listbox.itemconfig(i, {'fg': 'green'})

def add_task_gui(description="Untitled Task"):
    if description:
        tasks.append({"description": description, "status": "Pending"})
        save_tasks(tasks)
        entry.delete(0, tk.END)
        update_gui()

@app.route("/exit", methods=["POST"])
def exit_app():
    os._exit(0)

@app.route("/")
def home():
    return render_template_string('''
        <html>
        <head>
            <title>My Todo App</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; }
                .completed { color: green; font-weight: bold; }
                .pending { color: black; }
                button { margin-left: 10px; padding: 5px 10px; }
            </style>
        </head>
        <body>
            <h1>My Todo App</h1>
            <ul>
                {% for index, task in enumerate(tasks) %}
                    <li class="{{ 'completed' if task['status'] == 'Completed' else 'pending' }}">
                        {{ task['description'] }} - {{ task['status'] }}
                        {% if task['status'] == 'Pending' %}
                            <button onclick="completeTask({{ index }})">Complete</button>
                        {% endif %}
                        <button onclick="deleteTask({{ index }})">Delete</button>
                    </li>
                {% endfor %}
            </ul>
            <input type="text" id="newTask" placeholder="New task">
            <button onclick="addTask()">Add Task</button>
            <button onclick="exitApp()">Exit</button>

            <script>
                function addTask() {
                    let desc = document.getElementById("newTask").value;
                    fetch("/tasks", {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify({ description: desc })
                    }).then(() => location.reload());
                }

                function completeTask(index) {
                    fetch(`/tasks/${index}`, { method: "PUT" }).then(() => location.reload());
                }

                function deleteTask(index) {
                    fetch(`/tasks/${index}`, { method: "DELETE" }).then(() => location.reload());
                }

                function exitApp() {
                    fetch("/exit", { method: "POST" }).then(() => alert("Server shutting down..."));
                }
            </script>
        </body>
        </html>
    ''', tasks=tasks, enumerate=enumerate)

@app.route("/tasks", methods=["POST"])
def add_task():
    data = request.json
    new_task = {"description": data.get("description", "Untitled Task"), "status": "Pending"}
    tasks.append(new_task)
    save_tasks(tasks)
    update_gui()
    return jsonify({"message": "Task added"}), 201

@app.route("/tasks/<int:task_id>", methods=["PUT"])
def complete_task(task_id):
    if 0 <= task_id < len(tasks):
        tasks[task_id]["status"] = "Completed"
        save_tasks(tasks)
        update_gui()
        return jsonify({"message": "Task completed"}), 200
    return jsonify({"error": "Task not found"}), 404

@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    if 0 <= task_id < len(tasks):
        del tasks[task_id]
        save_tasks(tasks)
        update_gui()
        return jsonify({"message": "Task deleted"}), 200
    return jsonify({"error": "Task not found"}), 404


root = tk.Tk()
root.title("My To-Do App")
root.geometry("400x500")
root.configure(bg="#f4f4f4")

title_label = tk.Label(root, text="My To-Do List", font=("Arial", 16, "bold"), bg="#f4f4f4")
title_label.pack(pady=10)

frame = tk.Frame(root, bg="#f4f4f4")
frame.pack(pady=10)

entry = tk.Entry(frame, width=30, font=("Arial", 12))
entry.pack(side=tk.LEFT, padx=5)
add_button = tk.Button(frame, text="Add", font=("Arial", 12), bg="#007BFF", fg="white", command=lambda: add_task_gui(entry.get() or "Untitled Task"))
add_button.pack(side=tk.LEFT)

listbox = tk.Listbox(root, width=50, height=12, font=("Arial", 12))
listbox.pack(pady=10)

button_frame = tk.Frame(root, bg="#f4f4f4")
button_frame.pack()

complete_button = tk.Button(button_frame, text="Complete", font=("Arial", 12), bg="#28A745", fg="white", command=lambda: match_action("complete"))
complete_button.grid(row=0, column=0, padx=5)

delete_button = tk.Button(button_frame, text="Delete", font=("Arial", 12), bg="#DC3545", fg="white", command=lambda: match_action("delete"))
delete_button.grid(row=0, column=1, padx=5)

exit_button = tk.Button(button_frame, text="Exit", font=("Arial", 12), bg="#6C757D", fg="white", command=exit_app)
exit_button.grid(row=0, column=2, padx=5)

def match_action(action):
    selected = listbox.curselection()
    if selected:
        index = selected[0]
        match action:
            case "complete":
                tasks[index]["status"] = "Completed"
                save_tasks(tasks)
                update_gui()
            case "delete":
                del tasks[index]
                save_tasks(tasks)
                update_gui()
            case _:
                print("[WARNING] Unknown action")

# Useful while loop for batch task management
while True:
    print("\n--- Task Manager ---")
    print("Commands: add | complete | delete | view | exit")
    command = input("Enter task action: ").strip().lower()

    if command == "exit":
        print("Exiting task manager...")
        break

    match command:
        case "add":
            desc = input("Task description: ").strip()
            if desc:
                add_task_gui(desc)
                print(f"[INFO] Task '{desc}' added.")
            else:
                print("[WARNING] Empty task description ignored.")
                
        case "complete":
            try:
                index = int(input("Task index to complete: "))
                if 0 <= index < len(tasks):
                    tasks[index]["status"] = "Completed"
                    save_tasks(tasks)
                    update_gui()
                    print(f"[INFO] Task '{tasks[index]['description']}' marked as completed.")
                else:
                    print("[ERROR] Invalid task index.")
            except ValueError:
                print("[ERROR] Please enter a valid integer.")
        
        case "delete":
            try:
                index = int(input("Task index to delete: "))
                if 0 <= index < len(tasks):
                    deleted_task = tasks.pop(index)
                    save_tasks(tasks)
                    update_gui()
                    print(f"[INFO] Task '{deleted_task['description']}' deleted.")
                else:
                    print("[ERROR] Invalid task index.")
            except ValueError:
                print("[ERROR] Please enter a valid integer.")
        
        case "view":
            if tasks:
                for i, task in enumerate(tasks):
                    status = "✔️" if task["status"] == "Completed" else "❌"
                    print(f"{i}: {task['description']} [{status}]")
            else:
                print("[INFO] No tasks available.")
        
        case _:
            print("[WARNING] Invalid command. Please try again.")


update_gui()

Thread(target=app.run, kwargs={'port': 5000, 'debug': False, 'use_reloader': False}).start()
root.mainloop()
