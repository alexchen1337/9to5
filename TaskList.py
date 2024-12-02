import pygame  # Add this import at the top

class TaskList:
    def __init__(self, tasks, font, x=10, y=10, color=(255, 255, 255)):
        self.tasks = tasks
        self.completed = [False] * len(tasks)
        self.font = font
        self.x = x
        self.y = y
        self.color = color
        self.visible = True
        self.current_task_index = 0  # Track the current task

    def toggle_task(self, index):
        # Only allow completing tasks in order
        if index == self.current_task_index:
            self.completed[index] = True
            self.current_task_index += 1
            return True
        return False

    def is_completed(self, index):
        return self.completed[index]

    def can_attempt_task(self, index):
        return index == self.current_task_index

    def reset_tasks(self):
        self.completed = [False] * len(self.tasks)
        self.current_task_index = 0

    def draw(self, screen):
        if not self.visible:
            return

        for i, task in enumerate(self.tasks):
            # Different colors for different task states
            if self.completed[i]:
                color = (0, 255, 0)  # Green for completed
            elif i == self.current_task_index:
                color = (255, 255, 255)  # White for current task
            else:
                color = (128, 128, 128)  # Gray for locked tasks
            
            text = self.font.render(f"{i+1}. {task}", True, color)
            screen.blit(text, (self.x, self.y + i * 30))

    def toggle_visibility(self):
        self.visible = not self.visible

    def all_tasks_completed(self):
        return all(self.completed)