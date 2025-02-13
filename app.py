import streamlit as st
import json
import os

# Name of the file where tasks are stored
TASKS_FILE = "tasks.json"

def load_tasks():
    """Load tasks from a JSON file, or return an empty list if the file doesn't exist."""
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "r") as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    """Save tasks to a JSON file."""
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=4)

def initialize_session_state():
    """Load tasks into session state if not already loaded."""
    if "tasks" not in st.session_state:
        st.session_state.tasks = load_tasks()

def add_task(task_text):
    """Add a new task to the session state and save."""
    if task_text:
        st.session_state.tasks.append({"task": task_text, "completed": False})
        save_tasks(st.session_state.tasks)

def delete_task(index):
    """Delete task by index and save changes."""
    st.session_state.tasks.pop(index)
    save_tasks(st.session_state.tasks)

def toggle_completion(index):
    """Toggle the completion status of the task and save."""
    st.session_state.tasks[index]["completed"] = not st.session_state.tasks[index]["completed"]
    save_tasks(st.session_state.tasks)

def main():
    st.title("Simple To-Do List Manager")
    st.write("Add tasks, mark them as complete, or delete them.")

    # Initialize session_state with tasks
    initialize_session_state()

    # Form for adding a new task
    with st.form("add_task_form", clear_on_submit=True):
        new_task_text = st.text_input("Enter a new task:")
        submitted = st.form_submit_button("Add Task")
        if submitted:
            add_task(new_task_text)
            st.success(f"Added task: {new_task_text}")

    # Display existing tasks
    st.subheader("Your Tasks:")
    if st.session_state.tasks:
        for i, task_data in enumerate(st.session_state.tasks):
            col1, col2, col3 = st.columns([0.7, 0.15, 0.15])
            task_description = task_data["task"]
            completed = task_data["completed"]

            # Display task description and a "Complete" button
            with col1:
                st.write(f"**{'~~' if completed else ''}{task_description}{'~~' if completed else ''}**")
            
            # Button to toggle completion
            with col2:
                if st.button("Complete" if not completed else "Uncomplete", key=f"complete_{i}"):
                    toggle_completion(i)
                    st.experimental_rerun()
            
            # Button to delete the task
            with col3:
                if st.button("Delete", key=f"delete_{i}"):
                    delete_task(i)
                    st.experimental_rerun()
    else:
        st.info("No tasks yet! Add a task above.")

if __name__ == "__main__":
    main()
