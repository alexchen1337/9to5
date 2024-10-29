# import pygame, heapq, random

# class DailyTasks():
import heapq
import random

class Task:
    def __init__(self, name):
        self.name = name
        self.priority = random.randint(1, 10)  # Random priority between 1 (highest) and 10 (lowest)

    def __lt__(self, other):
        return self.priority < other.priority  # Lower priority number means higher importance

class DailyTasks:
    def __init__(self):
        self.tasks = [
            Task("Check Emails"),
            Task("Make Coffee"),
            Task("Taking Notes"),
            Task("Sorting Emails"),
            Task("Proofreading Documents"),
        ]
        self.priority_queue = []
        self.completed_tasks = []

    def select_prioritized_tasks(self):
        # Randomly select a few tasks to be more important
        important_tasks = random.sample(self.tasks, k=min(3, len(self.tasks)))
        for task in important_tasks:
            # Set higher priority for selected tasks
            task.priority = 1  # Higher priority
            heapq.heappush(self.priority_queue, task)

        # Add the rest of the tasks with lower priority
        for task in self.tasks:
            if task not in important_tasks:
                heapq.heappush(self.priority_queue, task)

    def check_emails(self, player):
        # Simulate a list of emails with a mix of starred and non-starred
        emails = [
            {"subject": "Project Update", "starred": True},
            {"subject": "Meeting Reminder", "starred": False},
            {"subject": "Team Outing Invitation", "starred": True},
            {"subject": "Spam Offer", "starred": False},
        ]

        print("\n--- Checking Emails ---")
        for i, email in enumerate(emails):
            print(f"{i + 1}. {email['subject']} {'(Starred)' if email['starred'] else ''}")

        # Player selects an email to check
        try:
            selection = int(input("Select an email to check (1-4): ")) - 1
            
            if selection < 0 or selection >= len(emails):
                print("Invalid selection. No emails checked.")
                return False

            selected_email = emails[selection]
            if selected_email["starred"]:
                print(f"You opened the email: {selected_email['subject']}.")
                print("Good job! This was an important email.")
                return True  # Successful completion
            else:
                print(f"You opened the email: {selected_email['subject']}.")
                print("Oops! This email wasn't important.")
                player.salary -= 5  # Penalty for missing important emails
                print(f"Salary decreased by $5. Current salary: ${player.salary}.")
                return False  # Failed completion

        except ValueError:
            print("Invalid input. You failed to check any emails.")
            player.salary -= 5  # Penalty for invalid input
            print(f"Salary decreased by $5. Current salary: ${player.salary}.")
            return False

    def make_coffee(self):
        print("Making coffee... Done!")

    def take_notes(self):
        print("Taking notes... Done!")

    def sort_emails(self, player):
        print("Sorting emails... Done!")

    def proofread_documents(self):
        print("Proofreading documents... Done!")

    def execute_tasks(self, player):
        print("\n--- Executing Daily Tasks ---")
        while self.priority_queue:
            task = heapq.heappop(self.priority_queue)
            print(f"Executing task: {task.name} (Priority: {task.priority})")
            # Call the corresponding method based on the task name
            if task.name == "Check Emails":
                self.check_emails(player)
            elif task.name == "Make Coffee":
                self.make_coffee()
            elif task.name == "Taking Notes":
                self.take_notes()
            elif task.name == "Sorting Emails":
                self.sort_emails(player)
            elif task.name == "Proofreading Documents":
                self.proofread_documents()
            self.completed_tasks.append(task.name)

    def display_completed_tasks(self):
        print("Completed Tasks:", ", ".join(self.completed_tasks) if self.completed_tasks else "None")