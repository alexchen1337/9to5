import pygame
import random

class NPC(pygame.sprite.Sprite):
    def __init__(self, sprite_path, scale_factor, screen_width, screen_height, name, job_title):
        super().__init__()
        self.image = pygame.image.load(sprite_path)
        self.image = pygame.transform.scale(self.image, (self.image.get_width() * scale_factor, self.image.get_height() * scale_factor))
        self.rect = self.image.get_rect()

        # Set the NPC's starting position to a random location within the screen
        self.rect.x = random.randint(0, screen_width - self.rect.width)
        self.rect.y = random.randint(0, screen_height - self.rect.height)
        
        self.name = name
        self.job_title = job_title
        self.mood = random.choice(['happy', 'neutral', 'unhappy'])
        
        # Movement variables
        self.speed = 2
        self.direction = pygame.math.Vector2()
        self.change_direction_timer = 0
        self.change_direction_interval = 60  # frames until direction change

    def update(self, screen_width, screen_height):
        # Update direction timer
        self.change_direction_timer += 1
        if self.change_direction_timer >= self.change_direction_interval:
            # Choose new random direction
            self.direction.x = random.uniform(-1, 1)
            self.direction.y = random.uniform(-1, 1)
            self.direction = self.direction.normalize()
            self.change_direction_timer = 0
            self.change_direction_interval = random.randint(30, 90)  # Random interval

        # Move NPC
        self.rect.x += self.direction.x * self.speed
        self.rect.y += self.direction.y * self.speed

        # Keep NPC in bounds
        if self.rect.left < 0:
            self.rect.left = 0
            self.direction.x *= -1
        if self.rect.right > screen_width:
            self.rect.right = screen_width
            self.direction.x *= -1
        if self.rect.top < 0:
            self.rect.top = 0
            self.direction.y *= -1
        if self.rect.bottom > screen_height:
            self.rect.bottom = screen_height
            self.direction.y *= -1

    def chat(self):
        chat_responses = {
            'happy': f"{self.name}: I'm having a great day!",
            'neutral': f"{self.name}: Just another day at the office.",
            'unhappy': f"{self.name}: Don't speak to me."
        }
        print(chat_responses[self.mood])

    def change_mood(self, new_mood):
        if new_mood in ['happy', 'neutral', 'unhappy']:
            self.mood = new_mood
        else:
            print("Invalid mood!")

    def __str__(self):
        return f"{self.name} - {self.job_title}, Mood: {self.mood}"

    def draw_minibar(self, screen, relationship_graph, target):
        # Get the relationship weight for this NPC
        weight = relationship_graph.get_relationship("player", target)

        # Determine the color based on the weight
        if weight > 60:
            color = (0, 255, 0)  # Green
        elif 30 <= weight <= 60:
            color = (255, 255, 0)  # Yellow
        else:
            color = (255, 0, 0)  # Red

        # Calculate the position and size of the minibar
        bar_width = 50
        bar_height = 5
        bar_x = self.rect.centerx - bar_width // 2
        bar_y = self.rect.bottom + 5  # Place it below the NPC

        # Background of the bar
        pygame.draw.rect(screen, (100, 100, 100), (bar_x, bar_y, bar_width, bar_height))

        # Filled portion of the bar
        filled_width = int((weight / 100) * bar_width)
        pygame.draw.rect(screen, color, (bar_x, bar_y, filled_width, bar_height))
    
    def draw_name(self, screen):
        # Define the font for the NPC's name
        font = pygame.font.Font(None, 24)  # Default font, size 24
        text_surface = font.render(self.name, True, (255, 255, 255))  # White color

        # Position the name just above the NPC
        text_rect = text_surface.get_rect(midbottom=(self.rect.centerx, self.rect.top - 5))
        screen.blit(text_surface, text_rect)