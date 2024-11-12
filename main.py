import pygame
from Player import Player
from IntroScreen import IntroScreen
from Meter import Meter  # Import your Meter class
from StoreRunner import runStore

# Initialize Pygame
pygame.init()
FPS = 45
font_path = "./assets/pixel.ttf"
font_size = 36
game_font = pygame.font.Font(font_path, font_size)
text_color = (255, 255, 255)  # White text

# Create a resizable window
screen_info = pygame.display.Info()
SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
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


# Function to draw a bar on the screen
def draw_meter(screen, meter, x, y, width=200, height=20, color=(0, 255, 0)):
    # Calculate the fill ratio based on the meter's value
    fill_ratio = meter.get_value() / meter.max_value
    fill_width = int(width * fill_ratio)
    
    # Bar background
    pygame.draw.rect(screen, (50, 50, 50), (x, y, width, height))  # Gray background
    # Bar fill
    pygame.draw.rect(screen, color, (x, y, fill_width, height))  # Customizable fill color
    # Text label
    text_surface = game_font.render(f"{meter.name}: {meter.value}/{meter.max_value}", True, text_color)
    screen.blit(text_surface, (x, y - font_size))  # Position text above bar

# Main game loop
running = True
clock = pygame.time.Clock()

# Main game loop
running = True
clock = pygame.time.Clock()
storeRunning = False

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

    if keys_pressed[pygame.K_e]:  # Enter the store
        storeRunning = runStore(screen, game_font)
        if storeRunning == False:  # Exited the store, return to the game
            storeRunning = False

    
# Quit Pygame
pygame.quit()
