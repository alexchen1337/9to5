class TaskList:
    def __init__(self, tasks, font, x, y, color=(255, 255, 255)):
        self.tasks = [{"text": task, "completed": False} for task in tasks]  # Task dictionary with completion state
        self.font = font
        self.x = x
        self.y = y
        self.color = color

    def toggle_task(self, index):
        if 0 <= index < len(self.tasks):
            self.tasks[index]["completed"] = not self.tasks[index]["completed"]

    def draw(self, screen):
        for index, task in enumerate(self.tasks):
            text = f"{index + 1}. {task['text']}"
            color = (0, 255, 0) if task["completed"] else self.color  # Green for completed tasks
            task_surface = self.font.render(text, True, color)
            screen.blit(task_surface, (self.x, self.y + index * self.font.get_height()))
    
    def reset_tasks(self):
        # Reset all tasks to not completed
        for task in self.tasks:
            task["completed"] = False