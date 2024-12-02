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
        self.all_tasks = [
            "Complete Typing Test",
            "Handle Email Inbox",
            "Make Coffee",
            "Make Burgers"
        ]

    def get_daily_tasks(self, num_tasks=2):
        """Returns 2-3 random tasks for the day"""
        num_tasks = random.randint(2, 3) if num_tasks == 2 else num_tasks
        return random.sample(self.all_tasks, num_tasks)

    