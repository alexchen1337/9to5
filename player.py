import pygame
import Meter
import time

class Player(pygame.sprite.Sprite):
    def __init__(self, sprite_path, scale_factor, screen_width, screen_height):
        super().__init__()
        self.image = pygame.image.load(sprite_path)
        self.image = pygame.transform.scale(self.image, (self.image.get_width() * scale_factor, self.image.get_height() * scale_factor))
        self.rect = self.image.get_rect()
        
        # Set the player's starting position to the center of the screen
        self.rect.center = (screen_width // 2, screen_height // 2)
        
        self.speed = 8  # Player speed
        
        # Set players meters to default 100
        self.health = Meter("Health", 100)
        self.energy = Meter("Energy", 100)
    
    def update(self, keys_pressed, screen_width, screen_height):
        # Horizontal movement
        if keys_pressed[pygame.K_LEFT]:
            self.rect.x -= self.speed
            self.energy.decrease(.1)
        if keys_pressed[pygame.K_RIGHT]:
            self.rect.x += self.speed
            self.energy.decrease(.1)

        # Vertical movement
        if keys_pressed[pygame.K_UP]:
            self.rect.y -= self.speed
            self.energy.decrease(.1)
        if keys_pressed[pygame.K_DOWN]:
            self.rect.y += self.speed
            self.energy.decrease(.1)

        # Boundary checks to prevent moving off-screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > screen_width:
            self.rect.right = screen_width
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > screen_height:
            self.rect.bottom = screen_height
    def check_meters(self):
        """Checks meter levels and displays warnings if any are low"""
        self.health.level_warning()
        self.energy.level_warning()
        
    def display_meters(self):
        #print for debugging
        print(self.health)
        print(self.energy)

