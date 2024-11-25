import pygame
import time

class DayTransitionScreen:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font("./assets/pixel.ttf", 48)
        self.alpha = 0
        self.fade_speed = 12
        self.surface = pygame.Surface((screen.get_width(), screen.get_height()))
        self.start_time = time.time()
        self.duration = 1.75  # Store duration as a property
        
        # Progress bar settings
        self.bar_width = 400
        self.bar_height = 20
        self.bar_color = (100, 200, 100)
        self.bar_bg_color = (50, 50, 50)
        
    def draw(self, current_day, going_to_work=True):
        # Fill with black
        self.surface.fill((0, 0, 0))
        
        # Calculate elapsed time and progress
        elapsed_time = time.time() - self.start_time
        progress = min(elapsed_time / (self.duration - 0.1), 1.0)  # Adjust timing to ensure bar completes
        
        # Render text
        text = "Going to Work..." if going_to_work else "Going Home..."
        transition_text = self.font.render(text, True, (255, 255, 255))
        day_text = self.font.render(f"Day {current_day}", True, (255, 255, 255))
        
        # Center the text
        transition_rect = transition_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 - 50))
        day_rect = day_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 - 110))
        
        # Draw text
        self.surface.blit(transition_text, transition_rect)
        self.surface.blit(day_text, day_rect)
        
        # Draw progress bar
        bar_x = (self.screen.get_width() - self.bar_width) // 2
        bar_y = self.screen.get_height() // 2 + 30
        
        # Background bar
        pygame.draw.rect(self.surface, self.bar_bg_color, 
                        (bar_x, bar_y, self.bar_width, self.bar_height))
        
        # Progress fill
        fill_width = int(self.bar_width * progress)
        pygame.draw.rect(self.surface, self.bar_color,
                        (bar_x, bar_y, fill_width, self.bar_height))
        
        # Handle fade animation
        if elapsed_time < self.duration/2:
            self.alpha = min(255, self.alpha + self.fade_speed)
        elif elapsed_time >= self.duration/2:
            self.alpha = max(0, self.alpha - self.fade_speed)
        
        # Set transparency and draw
        self.surface.set_alpha(self.alpha)
        self.screen.blit(self.surface, (0, 0))
        pygame.display.flip()
        
        # Return True when transition is complete
        return elapsed_time >= self.duration
    
    def handle_input(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and self.alpha >= 255:
            self.fading_in = False
            return False
        return not self.fading_in and self.alpha <= 0