import pygame  # Add this import at the top

class TaskList:
    def __init__(self, tasks, font, x, y, color=(255, 255, 255)):
        self.tasks = [{"text": task, "completed": False} for task in tasks]  # Task dictionary with completion state
        self.font = font
        self.x = x
        self.y = y
        self.color = color
        self.visible = True  # Add visibility flag
        # Add background parameters
        self.padding = 10  # Padding around text
        self.bg_color = (0, 0, 0, 128)  # Black with 50% transparency
        
        # Calculate background dimensions
        self.max_width = 0
        for task in self.tasks:
            text_surface = self.font.render(f"1. {task['text']}", True, color)
            self.max_width = max(self.max_width, text_surface.get_width())
        self.bg_height = (30 * len(self.tasks)) + (self.padding * 2)
        self.bg_width = self.max_width + (self.padding * 2)

    def toggle_task(self, index):
        if 0 <= index < len(self.tasks):
            self.tasks[index]["completed"] = not self.tasks[index]["completed"]

    def toggle_visibility(self):
        self.visible = not self.visible

    def draw(self, screen):
        if not self.visible:  # Only draw if visible
            return
            
        # Create a surface for the semi-transparent background
        bg_surface = pygame.Surface((self.bg_width, self.bg_height), pygame.SRCALPHA)
        pygame.draw.rect(bg_surface, self.bg_color, bg_surface.get_rect())
        screen.blit(bg_surface, (self.x - self.padding, self.y - self.padding))

        # Draw tasks
        for index, task in enumerate(self.tasks):
            text = f"{index + 1}. {task['text']}"
            color = (0, 255, 0) if task["completed"] else self.color  # Green for completed tasks
            task_surface = self.font.render(text, True, color)
            screen.blit(task_surface, (self.x, self.y + 30 * index))  # Added spacing between tasks
    
    def reset_tasks(self):
        # Reset all tasks to not completed
        for task in self.tasks:
            task["completed"] = False

    def is_completed(self, index):
        if 0 <= index < len(self.tasks):
            return self.tasks[index]["completed"]
        return False

    def can_attempt_task(self, index):
        # Check if the task index is valid and the task is not already completed
        if 0 <= index < len(self.tasks):
            return not self.tasks[index]["completed"]
        return False