import json
import os
from datetime import datetime
from enum import Enum

FILE_NAME = "tasks.json"

class Priority(Enum):
    LOW = "🟢 Low"
    MEDIUM = "🟡 Medium" 
    HIGH = "🔴 High"

class Status(Enum):
    PENDING = "⏳ Pending"
    COMPLETED = "✅ Completed"
    IN_PROGRESS = "🔄 In Progress"

def load_tasks():
    """Load tasks from the JSON file with error handling."""
    try:
        if os.path.exists(FILE_NAME):
            with open(FILE_NAME, "r", encoding="utf-8") as file:
                return json.load(file)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"⚠️ Error loading tasks: {e}")
        print("📝 Starting with empty task list.")
    return []

def save_tasks(tasks):
    """Save tasks to the JSON file with error handling."""
    try:
        with open(FILE_NAME, "w", encoding="utf-8") as file:
            json.dump(tasks, file, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"❌ Error saving tasks: {e}")

def add_task():
    """Add a new task with enhanced features."""
    print("\n➕ Add New Task")
    task_text = input("Enter task description: ").strip()
    
    if not task_text:
        print("⚠️ Task description cannot be empty.")
        return
    
    print("\nSelect Priority:")
    for i, priority in enumerate(Priority, 1):
        print(f"{i}. {priority.value}")
    
    try:
        priority_choice = int(input("Enter priority (1-3, default: 2): ") or "2")
        priority = list(Priority)[priority_choice - 1]
    except (ValueError, IndexError):
        priority = Priority.MEDIUM
        print(f"⚠️ Invalid choice, using default: {priority.value}")
    
    # Optional category
    category = input("Enter category (optional): ").strip() or "General"
    
    # Optional due date
    due_date = input("Enter due date (YYYY-MM-DD, optional): ").strip()
    if due_date:
        try:
            datetime.strptime(due_date, "%Y-%m-%d")
        except ValueError:
            print("⚠️ Invalid date format, ignoring due date.")
            due_date = None
    
    task_data = {
        "id": len(load_tasks()) + 1,
        "task": task_text,
        "priority": priority.name,
        "status": Status.PENDING.name,
        "category": category,
        "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "due_date": due_date,
        "completed_date": None
    }
    
    tasks = load_tasks()
    tasks.append(task_data)
    save_tasks(tasks)
    print(f"✅ Task added successfully: {task_text}")

def list_tasks(filter_status=None, filter_category=None):
    """List tasks with optional filtering and enhanced display."""
    tasks = load_tasks()
    
    if filter_status:
        tasks = [t for t in tasks if t.get("status") == filter_status]
    if filter_category:
        tasks = [t for t in tasks if t.get("category", "").lower() == filter_category.lower()]
    
    if not tasks:
        print("📭 No tasks found.")
        return
    
    print(f"\n📌 Tasks Found: {len(tasks)}")
    print("=" * 80)
    
    # Sort by priority (High -> Medium -> Low) and then by creation date
    priority_order = {Priority.HIGH.name: 0, Priority.MEDIUM.name: 1, Priority.LOW.name: 2}
    tasks.sort(key=lambda x: (priority_order.get(x.get("priority", Priority.MEDIUM.name), 1), x.get("created", "")))
    
    for i, task in enumerate(tasks, 1):
        priority = Priority[task.get("priority", "MEDIUM")].value
        status = Status[task.get("status", "PENDING")].value
        category = task.get("category", "General")
        created = task.get("created", "Unknown")
        due_date = task.get("due_date", "No due date")
        
        print(f"{i:2d}. [{task.get('id', i):2d}] {priority} | {status}")
        print(f"    📝 {task['task']}")
        print(f"    🏷️  Category: {category} | 📅 Created: {created[:10]}")
        if due_date != "No due date":
            print(f"    ⏰ Due: {due_date}")
        
        if task.get("completed_date"):
            print(f"    ✅ Completed: {task['completed_date']}")
        print()

def remove_task():
    """Remove a task by ID."""
    list_tasks()
    if not load_tasks():
        return
    
    try:
        task_id = int(input("Enter task ID to remove: "))
        tasks = load_tasks()
        
        task_to_remove = None
        for i, task in enumerate(tasks):
            if task.get("id") == task_id:
                task_to_remove = i
                break
        
        if task_to_remove is not None:
            removed = tasks.pop(task_to_remove)
            save_tasks(tasks)
            print(f"❌ Task removed: {removed['task']}")
        else:
            print("⚠️ Task not found.")
            
    except ValueError:
        print("⚠️ Please enter a valid task ID.")

def update_task_status():
    """Update task status."""
    list_tasks()
    if not load_tasks():
        return
    
    try:
        task_id = int(input("Enter task ID to update: "))
        tasks = load_tasks()
        
        task_index = None
        for i, task in enumerate(tasks):
            if task.get("id") == task_id:
                task_index = i
                break
        
        if task_index is None:
            print("⚠️ Task not found.")
            return
        
        print("\nSelect new status:")
        for i, status in enumerate(Status, 1):
            print(f"{i}. {status.value}")
        
        status_choice = int(input("Enter status (1-3): "))
        new_status = list(Status)[status_choice - 1]
        
        tasks[task_index]["status"] = new_status.name
        
        if new_status == Status.COMPLETED:
            tasks[task_index]["completed_date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        else:
            tasks[task_index]["completed_date"] = None
        
        save_tasks(tasks)
        print(f"✅ Task status updated to: {new_status.value}")
        
    except (ValueError, IndexError):
        print("⚠️ Invalid input.")

def edit_task():
    """Edit an existing task."""
    list_tasks()
    if not load_tasks():
        return
    
    try:
        task_id = int(input("Enter task ID to edit: "))
        tasks = load_tasks()
        
        task_index = None
        for i, task in enumerate(tasks):
            if task.get("id") == task_id:
                task_index = i
                break
        
        if task_index is None:
            print("⚠️ Task not found.")
            return
        
        current_task = tasks[task_index]
        print(f"\nCurrent task: {current_task['task']}")
        
        new_description = input("Enter new description (press Enter to keep current): ").strip()
        if new_description:
            tasks[task_index]["task"] = new_description
        
        print("\nSelect new priority:")
        for i, priority in enumerate(Priority, 1):
            print(f"{i}. {priority.value}")
        
        priority_input = input("Enter priority (1-3, press Enter to keep current): ").strip()
        if priority_input:
            try:
                priority_choice = int(priority_input)
                new_priority = list(Priority)[priority_choice - 1]
                tasks[task_index]["priority"] = new_priority.name
            except (ValueError, IndexError):
                print("⚠️ Invalid priority, keeping current.")
        
        new_category = input("Enter new category (press Enter to keep current): ").strip()
        if new_category:
            tasks[task_index]["category"] = new_category
        
        save_tasks(tasks)
        print("✅ Task updated successfully!")
        
    except ValueError:
        print("⚠️ Please enter a valid task ID.")

def search_tasks():
    """Search tasks by keyword."""
    keyword = input("Enter search keyword: ").strip().lower()
    if not keyword:
        print("⚠️ Please enter a search keyword.")
        return
    
    tasks = load_tasks()
    matching_tasks = []
    
    for task in tasks:
        if (keyword in task.get("task", "").lower() or 
            keyword in task.get("category", "").lower()):
            matching_tasks.append(task)
    
    if not matching_tasks:
        print(f"🔍 No tasks found containing '{keyword}'")
        return
    
    print(f"\n🔍 Search Results for '{keyword}': {len(matching_tasks)} tasks")
    print("=" * 80)
    
    for i, task in enumerate(matching_tasks, 1):
        priority = Priority[task.get("priority", "MEDIUM")].value
        status = Status[task.get("status", "PENDING")].value
        print(f"{i}. [{task.get('id'):2d}] {priority} | {status}")
        print(f"   📝 {task['task']}")
        print(f"   🏷️ Category: {task.get('category', 'General')}")
        print()

def show_statistics():
    """Show task statistics."""
    tasks = load_tasks()
    if not tasks:
        print("📭 No tasks to analyze.")
        return
    
    total = len(tasks)
    completed = len([t for t in tasks if t.get("status") == Status.COMPLETED.name])
    pending = len([t for t in tasks if t.get("status") == Status.PENDING.name])
    in_progress = len([t for t in tasks if t.get("status") == Status.IN_PROGRESS.name])
    
    # Priority breakdown
    high_priority = len([t for t in tasks if t.get("priority") == Priority.HIGH.name])
    medium_priority = len([t for t in tasks if t.get("priority") == Priority.MEDIUM.name])
    low_priority = len([t for t in tasks if t.get("priority") == Priority.LOW.name])
    
    # Category breakdown
    categories = {}
    for task in tasks:
        cat = task.get("category", "General")
        categories[cat] = categories.get(cat, 0) + 1
    
    print("\n📊 Task Statistics")
    print("=" * 40)
    print(f"📝 Total Tasks: {total}")
    print(f"✅ Completed: {completed} ({completed/total*100:.1f}%)")
    print(f"⏳ Pending: {pending} ({pending/total*100:.1f}%)")
    print(f"🔄 In Progress: {in_progress} ({in_progress/total*100:.1f}%)")
    print()
    print("🎯 Priority Breakdown:")
    print(f"   🔴 High: {high_priority}")
    print(f"   🟡 Medium: {medium_priority}")
    print(f"   🟢 Low: {low_priority}")
    print()
    print("🏷️ Categories:")
    for cat, count in sorted(categories.items()):
        print(f"   {cat}: {count}")

def filter_menu():
    """Show filtering options."""
    while True:
        print("\n🔍 Filter Tasks")
        print("1. Show all tasks")
        print("2. Show by status")
        print("3. Show by category")
        print("4. Back to main menu")
        
        choice = input("Enter your choice (1-4): ")
        
        if choice == "1":
            list_tasks()
        elif choice == "2":
            print("\nSelect status to filter:")
            for i, status in enumerate(Status, 1):
                print(f"{i}. {status.value}")
            try:
                status_choice = int(input("Enter choice (1-3): "))
                filter_status = list(Status)[status_choice - 1].name
                list_tasks(filter_status=filter_status)
            except (ValueError, IndexError):
                print("⚠️ Invalid choice.")
        elif choice == "3":
            category = input("Enter category to filter: ").strip()
            if category:
                list_tasks(filter_category=category)
            else:
                print("⚠️ Please enter a category name.")
        elif choice == "4":
            break
        else:
            print("⚠️ Invalid choice, try again.")

def main():
    """Main program loop with enhanced menu."""
    print("🎯 Welcome to Enhanced Todo List Manager!")
    
    while True:
        print("\n" + "="*50)
        print("📋 ENHANCED TODO LIST MANAGER")
        print("="*50)
        print("1. ➕ Add task")
        print("2. 📝 List all tasks")
        print("3. 🔍 Filter/Search tasks")
        print("4. 🔍 Search tasks")
        print("5. ✏️  Edit task")
        print("6. 🔄 Update task status")
        print("7. ❌ Remove task")
        print("8. 📊 Show statistics")
        print("9. 🚪 Exit")
        
        choice = input("\nEnter your choice (1-9): ").strip()
        
        if choice == "1":
            add_task()
        elif choice == "2":
            list_tasks()
        elif choice == "3":
            filter_menu()
        elif choice == "4":
            search_tasks()
        elif choice == "5":
            edit_task()
        elif choice == "6":
            update_task_status()
        elif choice == "7":
            remove_task()
        elif choice == "8":
            show_statistics()
        elif choice == "9":
            print("👋 Thank you for using Enhanced Todo List Manager!")
            print("🎯 Stay productive!")
            break
        else:
            print("⚠️ Invalid choice, please try again.")
        
        # Pause before showing menu again
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye! Task manager closed.")
    except Exception as e:
        print(f"\n❌ An unexpected error occurred: {e}")
        print("Please restart the program.")
