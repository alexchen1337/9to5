import pygame
from player import Player
from IntroScreen import IntroScreen
from EndScreen import EndScreen
from Meter import Meter  # Import your Meter class
from StoreRunner import runStore
from TaskList import TaskList

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
storeRunning = False

# Screen managment
current_screen = 1

# Day managment
current_day = 1
last_day = 30
end_text = ""

# Define the tasks for the office
tasks = [
    "Check email responses",
    "Prepare the presentation",
    "Call the client",
    "Complete the report",
    "Attend the team meeting"
]

# Initialize the TaskList
task_list = TaskList(tasks, game_font, x=10, y=160, color=(255, 255, 255))

while running:

    if(current_day > last_day):
        running = False
        end_text = "You survived 30 days."  

    if(player.energy.is_depleted()):
        running = False
        end_text = "You should have taken a sabbatical. You ran out of energy."

    if(player.health.is_depleted()):
        running = False
        end_text = "You became too stressed, had a heart attack, and put on leave."

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
        
        if current_screen == 1 and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:  # Press '1' to toggle task 1
                task_list.toggle_task(0)
            elif event.key == pygame.K_2:  # Press '2' to toggle task 2
                task_list.toggle_task(1)
            elif event.key == pygame.K_3:  # Press '2' to toggle task 2
                task_list.toggle_task(2)

    # Get key presses for player movement
    keys_pressed = pygame.key.get_pressed()

    # Update player position with boundary checks
    player_group.update(keys_pressed, SCREEN_WIDTH, SCREEN_HEIGHT)

    # Screen transition logic
    if (current_screen == 1 and player.rect.right >= SCREEN_WIDTH):
        current_screen = 2
        player.rect.left = 0 + 10
        player.health.decrease(10) # going to work slowly kills you
        task_list.reset_tasks()  # Reset tasks when transitioning to home

    elif (current_screen == 2 and player.rect.left <= 0):
        current_screen = 1
        player.rect.right = SCREEN_WIDTH - 10
        current_day += 1

    # Fill the screen with a color
    if (current_screen == 1):
        background_image = pygame.image.load('./assets/HomeScreen.png')
        background_image = pygame.transform.scale(background_image, (1280, 720))
        screen.blit(background_image, (0,0))
        task_list.draw(screen)  # Draw the task list
    elif (current_screen == 2):

        screen.fill((50, 50, 150)) # Dark Blue

    # Draw the player
    player_group.draw(screen)

    # Update the display
    pygame.display.flip()

    # Limit the frame rate
    clock.tick(FPS)

    if keys_pressed[pygame.K_e]:  # Enter the store
        storeRunning = runStore(screen, game_font, player)
        if storeRunning == False:  # Exited the store, return to the game
            storeRunning = False


# Create and display the intro screen
end_screen = EndScreen(screen, selected_sprite)
end_running = True

# End screen loop
while end_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            end_running = False
            pygame.quit()
            exit()
        if end_screen.update(event):
            #selected_sprite = intro_screen.selected_sprite
            end_running = False

    end_screen.draw(end_text, player.checkings.get_value())

# Quit Pygame
pygame.quit()
