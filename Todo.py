import json
import os

FILE_NAME = "tasks.json"


def load_tasks():
    """Load tasks from the JSON file."""
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as file:
            return json.load(file)
    return []


def save_tasks(tasks):
    """Save tasks to the JSON file."""
    with open(FILE_NAME, "w") as file:
        json.dump(tasks, file, indent=4)


def add_task(task):
    tasks = load_tasks()
    tasks.append(task)
    save_tasks(tasks)
    print(f"✅ Task added: {task}")


def list_tasks():
    tasks = load_tasks()
    if not tasks:
        print("📭 No tasks found.")
    else:
        print("\n📌 Your Tasks:")
        for i, task in enumerate(tasks, 1):
            print(f"{i}. {task}")


def remove_task(index):
    tasks = load_tasks()
    if 0 < index <= len(tasks):
        removed = tasks.pop(index - 1)
        save_tasks(tasks)
        print(f"❌ Task removed: {removed}")
    else:
        print("⚠️ Invalid task number.")


def main():
    while True:
        print("\n--- To-Do List ---")
        print("1. Add task")
        print("2. List tasks")
        print("3. Remove task")
        print("4. Exit")

        choice = input("Enter your choice (1-4): ")

        if choice == "1":
            task = input("Enter a new task: ")
            add_task(task)

        elif choice == "2":
            list_tasks()

        elif choice == "3":
            list_tasks()
            try:
                index = int(input("Enter task number to remove: "))
                remove_task(index)
            except ValueError:
                print("⚠️ Please enter a valid number.")

        elif choice == "4":
            print("👋 Goodbye!")
            break

        else:
            print("⚠️ Invalid choice, try again.")


if __name__ == "__main__":
    main()
