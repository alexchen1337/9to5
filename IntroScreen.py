import pygame

font_path = "./assets/pixel.ttf"
font_size = 64
text_color = (255, 255, 255)

class IntroScreen:
    def __init__(self, screen, sprite_paths):
        self.screen = screen
        self.sprite_paths = sprite_paths
        self.current_index = 0  # Track the current sprite
        
        # Font loading with error handling
        try:
            self.font = pygame.font.Font(font_path, 64)
            self.small_font = pygame.font.Font(font_path, 32)
            self.credit_font = pygame.font.Font(font_path, 28)  # Smaller font for credits
        except FileNotFoundError:
            print(f"Font file not found: {font_path}")
            pygame.quit()
            exit()

        self.title = "9-5 Simulator: Mundane Living Circumstances"
        self.selected_sprite = None

    def draw(self):
        # Fill the screen with a background color
        self.screen.fill((30, 30, 30))  # Dark grey background

        # Render and display the title
        title_surface = self.font.render(self.title, True, (255, 255, 255))
        title_rect = title_surface.get_rect(center=(self.screen.get_width() / 2, 100))
        self.screen.blit(title_surface, title_rect)

        # Load and display the current sprite for selection
        sprite_path = self.sprite_paths[self.current_index]
        try:
            sprite_image = pygame.image.load(sprite_path).convert_alpha()
            sprite_image = pygame.transform.scale(sprite_image, (128, 128))  # Scale the sprite
            sprite_rect = sprite_image.get_rect(center=(self.screen.get_width() / 2, self.screen.get_height() / 2))
            self.screen.blit(sprite_image, sprite_rect)
        except pygame.error as e:
            print(f"Error loading sprite: {sprite_path}, {e}")
            pygame.quit()
            exit()

        # Render instructions
        instructions = "Use LEFT/RIGHT to choose, ENTER to confirm"
        instructions_surface = self.small_font.render(instructions, True, (255, 255, 255))
        instructions_rect = instructions_surface.get_rect(center=(self.screen.get_width() / 2, self.screen.get_height() - 250))
        self.screen.blit(instructions_surface, instructions_rect)

        # Render the credits
        credits = "Made by: Alex Chen, Eric Chtilianov, Ethan Dietrich, William Armentrout"
        credits_surface = self.credit_font.render(credits, True, (255, 255, 255))
        credits_rect = credits_surface.get_rect(center=(self.screen.get_width() / 2, self.screen.get_height() - 50))
        self.screen.blit(credits_surface, credits_rect)

        # Update the display
        pygame.display.flip()

    def update(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                # Scroll left through sprites
                self.current_index = (self.current_index - 1) % len(self.sprite_paths)
            elif event.key == pygame.K_RIGHT:
                # Scroll right through sprites
                self.current_index = (self.current_index + 1) % len(self.sprite_paths)
            elif event.key == pygame.K_RETURN:
                # Confirm selection
                self.selected_sprite = self.sprite_paths[self.current_index]
                return True  # End intro screen and proceed to the game
        return False
