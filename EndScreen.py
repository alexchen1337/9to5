import pygame

font_path = "./assets/pixel.ttf"
font_size = 64
text_color = (255, 255, 255)


class EndScreen:
    def __init__(self, screen, selected_sprite_path):
        self.screen = screen
        self.sprite_path = selected_sprite_path
        self.game_Over_txt = "GAME OVER"

        # Font loading with error handling
        try:
            self.font = pygame.font.Font(font_path, 64)
            self.small_font = pygame.font.Font(font_path, 32)
            self.credit_font = pygame.font.Font(font_path, 28)  # Smaller font for credits
        except FileNotFoundError:
            print(f"Font file not found: {font_path}")
            pygame.quit()
            exit()


    def draw(self, text, balance):
        #load background
        background_image = pygame.image.load('./assets/EndScreen.png')
        background_image = pygame.transform.scale(background_image, (1280, 720))

        self.screen.blit(background_image, (0,0))
        #pygame.display.update()

        # Render selected sprite
        sprite_image = pygame.image.load(self.sprite_path).convert_alpha()
        sprite_image = pygame.transform.scale(sprite_image, (128, 128))  # Scale the sprite
        sprite_rect = sprite_image.get_rect(center=(self.screen.get_width() / 2, self.screen.get_height() -200))
        self.screen.blit(sprite_image, sprite_rect)

        # Render Game Over
        gameOver_surface = self.font.render(self.game_Over_txt, True, (255, 0, 0))
        gameOver_rect = gameOver_surface.get_rect(center=(self.screen.get_width() / 2, 125))
        self.screen.blit(gameOver_surface, gameOver_rect)

        # Render end message
        endText_surface = self.small_font.render(text, True, (255, 255, 255))
        endText_rect = endText_surface.get_rect(center=(self.screen.get_width() / 2, 250))
        self.screen.blit(endText_surface, endText_rect)

        # Render Score
        score_surface = self.small_font.render(f"Your final balance was: ${balance}", True, (0, 150, 0))
        score_rect = score_surface.get_rect(center=(self.screen.get_width() / 2, 300))
        self.screen.blit(score_surface, score_rect)

        # Render the credits
        credits = "Made by: Alex Chen, Eric Chtilianov, Ethan Dietrich, William Armentrout"
        credits_surface = self.credit_font.render(credits, True, (255, 255, 255))
        credits_rect = credits_surface.get_rect(center=(self.screen.get_width() / 2, self.screen.get_height() - 50))
        self.screen.blit(credits_surface, credits_rect)

        pygame.display.update()

    def update(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return True  # End end screen
        return False
