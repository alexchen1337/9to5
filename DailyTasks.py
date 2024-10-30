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

    