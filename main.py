import pygame
from player import Player
from IntroScreen import IntroScreen

# Initialize Pygame
pygame.init()
FPS = 45
font_path = "./assets/pixel.ttf"
font_size = 36
game_font = pygame.font.Font(font_path, font_size)
text_color = (255, 255, 255)  # White text

# Create a resizable window
screen_info = pygame.display.Info()
SCREEN_WIDTH, SCREEN_HEIGHT = screen_info.current_w, screen_info.current_h
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE | pygame.SCALED)

# Sprite options
sprite_paths = [
    "./assets/player0.png",
    "./assets/player1.png",
    "./assets/player2.png"
]

# Create and display the intro screen
intro_screen = IntroScreen(screen, sprite_paths)
intro_running = True
selected_sprite = None

# Intro screen loop
while intro_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            intro_running = False
            pygame.quit()
            exit()

        # Update intro screen and check if a sprite is selected
        if intro_screen.update(event):
            selected_sprite = intro_screen.selected_sprite
            intro_running = False

    intro_screen.draw()

# Load the selected player sprite and scale it 
player = Player(selected_sprite, scale_factor=8, screen_width=SCREEN_WIDTH, screen_height=SCREEN_HEIGHT)  # Center player
player_group = pygame.sprite.Group()
player_group.add(player)

# Main game loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

    # Get key presses for player movement
    keys_pressed = pygame.key.get_pressed()

    # Update player position with boundary checks
    player_group.update(keys_pressed, SCREEN_WIDTH, SCREEN_HEIGHT)

    # Fill the screen with a color
    screen.fill((0, 0, 0))  # Black background

    # Draw the player
    player_group.draw(screen)

    # Update the display
    pygame.display.flip()

    # Limit the frame rate
    clock.tick(FPS)

# Quit Pygame
pygame.quit()

