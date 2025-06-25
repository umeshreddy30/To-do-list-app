import tkinter as tk
from tkinter import messagebox, simpledialog
from datetime import datetime
import json
import os

FILENAME = "tasks.json"

# Load tasks from file
def load_tasks():
    if os.path.exists(FILENAME):
        with open(FILENAME, 'r') as file:
            return json.load(file)
    return []

# Save tasks to file
def save_tasks():
    with open(FILENAME, 'w') as file:
        json.dump(tasks, file, indent=4)

# Update task list display with filters
def update_listbox():
    task_listbox.delete(0, tk.END)
    now = datetime.now()
    keyword = search_var.get().lower()
    status = status_var.get()

    for idx, task in enumerate(tasks):
        title = task['title']
        deadline_str = task['deadline']
        completed = task.get('completed', False)

        # Filter by search keyword
        if keyword and keyword not in title.lower():
            continue

        # Filter by status
        if status == "Completed" and not completed:
            continue
        if status == "Incomplete" and completed:
            continue

        display = f"{title} - {deadline_str}"
        if completed:
            display += " ✔️"

        task_listbox.insert(tk.END, display)
        try:
            deadline = datetime.strptime(deadline_str, "%Y-%m-%d %H:%M")
        except ValueError:
            deadline = now

        # Set color based on status
        listbox_index = task_listbox.size() - 1
        if completed:
            task_listbox.itemconfig(listbox_index, {'fg': 'green'})
        elif deadline < now:
            task_listbox.itemconfig(listbox_index, {'fg': 'red'})
        else:
            task_listbox.itemconfig(listbox_index, {'fg': 'black'})

# Add new task
def add_task():
    title = simpledialog.askstring("Add Task", "Enter task title:")
    if not title:
        return
    deadline = simpledialog.askstring("Deadline", "Enter deadline (YYYY-MM-DD HH:MM):")
    try:
        datetime.strptime(deadline, "%Y-%m-%d %H:%M")
    except (ValueError, TypeError):
        messagebox.showerror("Invalid Deadline", "Deadline must be in format YYYY-MM-DD HH:MM")
        return
    tasks.append({"title": title, "deadline": deadline, "completed": False})
    save_tasks()
    update_listbox()

# Delete selected task
def delete_task():
    selected = task_listbox.curselection()
    if selected:
        task_index = get_real_index(selected[0])
        del tasks[task_index]
        save_tasks()
        update_listbox()
    else:
        messagebox.showwarning("No Selection", "Please select a task to delete.")

# Mark as complete
def mark_complete():
    selected = task_listbox.curselection()
    if selected:
        task_index = get_real_index(selected[0])
        tasks[task_index]["completed"] = True
        save_tasks()
        update_listbox()
    else:
        messagebox.showwarning("No Selection", "Please select a task to mark as complete.")

# Unmark task
def unmark_complete():
    selected = task_listbox.curselection()
    if selected:
        task_index = get_real_index(selected[0])
        tasks[task_index]["completed"] = False
        save_tasks()
        update_listbox()
    else:
        messagebox.showwarning("No Selection", "Please select a task to unmark.")

# Edit task
def edit_task():
    selected = task_listbox.curselection()
    if selected:
        task_index = get_real_index(selected[0])
        task = tasks[task_index]

        new_title = simpledialog.askstring("Edit Title", "Enter new title (leave blank to keep current):", initialvalue=task['title'])
        new_deadline = simpledialog.askstring("Edit Deadline", "Enter new deadline (YYYY-MM-DD HH:MM):", initialvalue=task['deadline'])

        if new_deadline:
            try:
                datetime.strptime(new_deadline, "%Y-%m-%d %H:%M")
            except ValueError:
                messagebox.showerror("Invalid Deadline", "Deadline must be in format YYYY-MM-DD HH:MM")
                return

        if new_title:
            task['title'] = new_title
        if new_deadline:
            task['deadline'] = new_deadline

        save_tasks()
        update_listbox()
    else:
        messagebox.showwarning("No Selection", "Please select a task to edit.")

# Get actual index in original tasks list
def get_real_index(display_index):
    filtered = []
    keyword = search_var.get().lower()
    status = status_var.get()
    for i, task in enumerate(tasks):
        title = task['title']
        completed = task.get('completed', False)
        if keyword and keyword not in title.lower():
            continue
        if status == "Completed" and not completed:
            continue
        if status == "Incomplete" and completed:
            continue
        filtered.append(i)
    return filtered[display_index]

# ---------------- GUI Setup ----------------
root = tk.Tk()
root.title("🗓️ To-Do List with Deadline + Filter")
root.geometry("650x520")

tasks = load_tasks()

# Search/filter frame
filter_frame = tk.Frame(root)
filter_frame.pack(pady=5)

tk.Label(filter_frame, text="Search Title:").grid(row=0, column=0, padx=5)
search_var = tk.StringVar()
search_entry = tk.Entry(filter_frame, textvariable=search_var, width=30)
search_entry.grid(row=0, column=1, padx=5)
search_entry.bind("<KeyRelease>", lambda e: update_listbox())

tk.Label(filter_frame, text="Status:").grid(row=0, column=2, padx=5)
status_var = tk.StringVar(value="All")
status_menu = tk.OptionMenu(filter_frame, status_var, "All", "Completed", "Incomplete", command=lambda _: update_listbox())
status_menu.grid(row=0, column=3, padx=5)

# Task list display
task_listbox = tk.Listbox(root, font=("Arial", 12), width=80, height=15)
task_listbox.pack(pady=10)

# Button frame
btn_frame = tk.Frame(root)
btn_frame.pack(pady=5)

tk.Button(btn_frame, text="Add Task", width=18, command=add_task).grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="Mark as Complete", width=18, command=mark_complete).grid(row=0, column=1, padx=5)
tk.Button(btn_frame, text="Unmark as Complete", width=18, command=unmark_complete).grid(row=0, column=2, padx=5)
tk.Button(btn_frame, text="Delete Task", width=18, command=delete_task).grid(row=0, column=3, padx=5)
tk.Button(btn_frame, text="✏️ Edit Task", width=18, command=edit_task).grid(row=1, column=1, columnspan=2, pady=10)

update_listbox()
root.mainloop()
