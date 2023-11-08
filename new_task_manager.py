import json
from datetime import datetime

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

class Task:
    def __init__(self, name, priority, due_date):
        self.name = name
        self.priority = priority
        self.due_date = datetime.strptime(due_date, "%Y-%m-%d").date()
        self.completed = False

class TaskManager:
    def __init__(self):
        self.users = []
        self.current_user = None

    def register(self, username, password):
        user = User(username, password)
        self.users.append(user)

    def login(self, username, password):
        for user in self.users:
            if user.username == username and user.password == password:
                self.current_user = user
                return True
        return False

    def add_task(self, name, priority, due_date):
        task = Task(name, priority, due_date)
        self.current_user.tasks.append(task)

    def delete_task(self, task):
        self.current_user.tasks.remove(task)

    def mark_task_completed(self, task):
        task.completed = True

    def get_tasks_today(self):
        today = datetime.today().date()
        tasks_today = []
        for task in self.current_user.tasks:
            if task.due_date == today:
                tasks_today.append(task)
        return tasks_today

    def sort_tasks_by_date(self):
        sorted_tasks = sorted(self.current_user.tasks, key=lambda task: task.due_date)
        return sorted_tasks

    def sort_tasks_by_priority(self):
        sorted_tasks = sorted(self.current_user.tasks, key=lambda task: task.priority, reverse=True)
        return sorted_tasks

    def save_data(self):
        data = {"users": []}
        for user in self.users:
            user_data = {
                "username": user.username,
                "password": user.password,
                "tasks": []
            }
            for task in user.tasks:
                task_data = {
                    "name": task.name,
                    "priority": task.priority,
                    "due_date": task.due_date.strftime("%Y-%m-%d"),
                    "completed": task.completed
                }
                user_data["tasks"].append(task_data)
            data["users"].append(user_data)

        with open("data.json", "w") as f:
            json.dump(data, f)

    def load_data(self):
        try:
            with open("data.json", "r") as f:
                data = json.load(f)
                for user_data in data["users"]:
                    user = User(user_data["username"], user_data["password"])
                    for task_data in user_data["tasks"]:
                        task = Task(task_data["name"], task_data["priority"], task_data["due_date"])
                        task.completed = task_data["completed"]
                        user.tasks.append(task)
                    self.users.append(user)
        except FileNotFoundError:
            pass

task_manager = TaskManager()
task_manager.load_data()

while True:
    print("1. Register")
    print("2. Login")
    print("3. Exit")
    choice = input("Enter your choice: ")

    if choice == "1":
        username = input("Enter username: ")
        password = input("Enter password: ")
        task_manager.register(username, password)
        print("Registration successful.\n")
    elif choice == "2":
        username = input("Enter username: ")
        password = input("Enter password: ")
        if task_manager.login(username, password):
            print("Login successful.\n")
            while True:
                print("1. Add task")
                print("2. Delete task")
                print("3. Mark task as completed")
                print("4. Today's tasks")
                print("5. Sort tasks by date")
                print("6. Sort tasks by priority")
                print("7. Change password")
                print("8. Logout")
                sub_choice = input("Enter your choice: ")

                if sub_choice == "1":
                    name = input("Enter task name: ")
                    priority = input("Enter task priority: ")
                    due_date = input("Enter task due date (YYYY-MM-DD): ")
                    task_manager.add_task(name, priority, due_date)
                    print("Task added.\n")
                elif sub_choice == "2":
                    print("Your tasks: ")
                    for i, task in enumerate(task_manager.current_user.tasks, start=1):
                        print(f"{i}. {task.name}")
                    choice = int(input("Enter the number of the task to delete: "))
                    task = task_manager.current_user.tasks[choice - 1]
                    task_manager.delete_task(task)
                    print("Task deleted.\n")
                elif sub_choice == "3":
                    print("Your tasks: ")
                    for i, task in enumerate(task_manager.current_user.tasks, start=1):
                        print(f"{i}. {task.name}")
                    choice = int(input("Enter the number of the task to mark as completed: "))
                    task = task_manager.current_user.tasks[choice - 1]
                    task_manager.mark_task_completed(task)
                    print("Task marked as completed.\n")
                elif sub_choice == "4":
                    tasks_today = task_manager.get_tasks_today()
                    if len(tasks_today) > 0:
                        print("Tasks for today: ")
                        for i, task in enumerate(tasks_today, start=1):
                            print(f"{i}. {task.name}")
                    else:
                        print("No tasks for today.\n")
                elif sub_choice == "5":
                    sorted_tasks = task_manager.sort_tasks_by_date()
                    print("Sorted tasks: ")
                    for i, task in enumerate(sorted_tasks, start=1):
                        print(f"{i}. {task.name}: {task.due_date.strftime('%Y-%m-%d')}")
                elif sub_choice == "6":
                    sorted_tasks = task_manager.sort_tasks_by_priority()
                    print("Sorted tasks: ")
                    for i, task in enumerate(sorted_tasks, start=1):
                        print(f"{i}. {task.name}: {task.priority}")
                elif sub_choice == "7":
                    new_password = input("Enter new password: ")
                    task_manager.current_user.password = new_password
                    task_manager.save_data()
                    print("Password changed.\n")
                elif sub_choice == "8":
                    task_manager.current_user = None
                    task_manager.save_data()
                    break
    elif choice == "3":
        task_manager.save_data()
        break