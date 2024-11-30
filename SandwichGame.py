import pygame
import time
import random
from player import Player

# Initialize pygame
pygame.init()

# Screen dimensions and grid settings
SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
GRID_SIZE = 128  # Size of each grid cell
COLUMNS, ROWS = 10, 5  # Set based on kitchen_layout dimensions

# Colors
WHITE = (255, 255, 255)
GREY = (200, 200, 200)
COOKING_BAR_COLOR = (255, 69, 0)  # Progress bar color
FAIL_COLOR = (255, 0, 0)  # Color for failed message
SUCCESS_COLOR = (0, 255, 0)  # Color for success message

# Create screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Burger-Cooking Game Layout")

# Define kitchen layout and ingredient locations
kitchen_layout = [
    [' ', 'I', 'I', ' ', ' ', ' ', ' ', ' ', ' ', 'S'],  # I = Ingredient, C = Cooking, S = Serving
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    ['C', 'C', ' ', ' ', 'I', 'I', 'I', ' ', ' ', ' ']
]

# Ingredient types at specific locations
ingredient_locations = {
    (0, 1): "Cheese",
    (0, 2): "Bun",
    (4, 5): "Lettuce",
    (4, 6): "Patty",
    (4, 4): "Tomato"
}

# Burger titles with sorted tuples as keys
burger_titles = {
    tuple(sorted(["Cheese", "Bun", "Patty"])): "Cheeseburger",
    tuple(sorted(["Tomato", "Bun", "Patty"])): "Tomato Burger",
    tuple(sorted(["Lettuce", "Bun", "Patty"])): "Lettuce Burger",
    tuple(sorted(["Cheese", "Tomato", "Bun", "Patty"])): "Cheese Tomato Burger",
    tuple(sorted(["Cheese", "Lettuce", "Bun", "Patty"])): "Cheese Lettuce Burger",
    tuple(sorted(["Cheese", "Tomato", "Lettuce", "Bun", "Patty"])): "Ultimate Burger",
}

# List of required burger types
required_burgers = [
    "Cheeseburger",
    "Tomato Burger",
    "Lettuce Burger",
    "Cheese Tomato Burger",
    "Cheese Lettuce Burger",
    "Ultimate Burger"
]

# Player starting position
player_x, player_y = 3, 2  # Start in the middle of the layout
held_items = []  # List to track what the player is holding
is_cooking = False
cook_start_time = 0
COOK_TIME = 3  # Seconds to cook a burger
current_burger_type = random.choice(required_burgers)  # Randomly select a new burger type
game_failed = False  # Track game state

# Initialize sandwich counter
sandwich_counter = 0

# Load images for player, floor tiles, and stations
player_image = pygame.image.load("assets/player0.png")  # Player image
player_image = pygame.transform.scale(player_image, (GRID_SIZE, GRID_SIZE))

floor_tile_image = pygame.image.load("assets/Tile.png")  # Floor tile image
floor_tile_image = pygame.transform.scale(floor_tile_image, (GRID_SIZE, GRID_SIZE))

cooking_station_image = pygame.image.load("assets/Stove.png")  # Cooking station image
cooking_station_image = pygame.transform.scale(cooking_station_image, (GRID_SIZE, GRID_SIZE))

serving_station_image = pygame.image.load("assets/Table.png")  # Serving station image
serving_station_image = pygame.transform.scale(serving_station_image, (GRID_SIZE, GRID_SIZE))

# Load unique ingredient images
ingredient_images = {
    "Cheese": pygame.transform.scale(
        pygame.image.load("assets/Cheese.png"), (GRID_SIZE, GRID_SIZE)
    ),
    "Tomato": pygame.transform.scale(
        pygame.image.load("assets/Tomato.png"), (GRID_SIZE, GRID_SIZE)
    ),
    "Lettuce": pygame.transform.scale(
        pygame.image.load("assets/Lettuce.png"), (GRID_SIZE, GRID_SIZE)
    ),
    "Patty": pygame.transform.scale(
        pygame.image.load("assets/Meat.png"), (GRID_SIZE, GRID_SIZE)
    ),
    "Bun": pygame.transform.scale(
        pygame.image.load("assets/Bun.png"), (GRID_SIZE, GRID_SIZE)
    ),
}

def draw_grid():
    for row in range(ROWS):
        for col in range(COLUMNS):
            x, y = col * GRID_SIZE, row * GRID_SIZE

            # Draw floor tile for every cell
            screen.blit(floor_tile_image, (x, y))
            
            # Draw kitchen stations based on layout
            if kitchen_layout[row][col] == 'I':  # Ingredient station
                ingredient = ingredient_locations.get((row, col), None)
                if ingredient and ingredient in ingredient_images:
                    screen.blit(ingredient_images[ingredient], (x, y))
            elif kitchen_layout[row][col] == 'C':  # Cooking station
                screen.blit(cooking_station_image, (x, y))
            elif kitchen_layout[row][col] == 'S':  # Serving station
                screen.blit(serving_station_image, (x, y))

    # Draw the player
    screen.blit(player_image, (player_x * GRID_SIZE, player_y * GRID_SIZE))

    # Display held items text
    font = pygame.font.Font(None, 36)
    item_text = f"Held Items: {', '.join(held_items) if held_items else 'None'}"
    text = font.render(item_text, True, (0, 0, 0))
    screen.blit(text, (10, SCREEN_HEIGHT - 40))

    # Draw required burger type
    required_text = f"Required Burger: {current_burger_type}"
    required_surface = font.render(required_text, True, (0, 0, 0))
    screen.blit(required_surface, (10, SCREEN_HEIGHT - 70))

    # Draw sandwich counter
    counter_text = f"Sandwiches Made (6): {sandwich_counter}"
    counter_surface = font.render(counter_text, True, (200, 100, 100))
    screen.blit(counter_surface, (10, SCREEN_HEIGHT - 100))

    # Draw cooking progress bar if cooking
    if is_cooking:
        elapsed_time = time.time() - cook_start_time
        progress = min(1, elapsed_time / COOK_TIME)
        pygame.draw.rect(screen, COOKING_BAR_COLOR, (player_x * GRID_SIZE, player_y * GRID_SIZE + GRID_SIZE - 10, int(GRID_SIZE * progress), 10))

    # Draw failed message if applicable
    if game_failed:
        font = pygame.font.Font(None, 72)
        failed_text = font.render("FAILED", True, FAIL_COLOR)
        text_rect = failed_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(failed_text, text_rect)

def reset_game():
    global held_items, is_cooking, cook_start_time, current_burger_type, player_x, player_y, game_failed
    held_items = []
    is_cooking = False
    cook_start_time = 0
    current_burger_type = random.choice(required_burgers)  # Randomly select a new burger type
    player_x, player_y = 3, 2  # Reset player position
    game_failed = False  # Reset failure state

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if not is_cooking and not game_failed:  # Prevent movement while cooking or after failure
                # Move with arrow keys
                if event.key == pygame.K_LEFT and player_x > 0:
                    player_x -= 1
                elif event.key == pygame.K_RIGHT and player_x < COLUMNS - 1:
                    player_x += 1
                elif event.key == pygame.K_UP and player_y > 0:
                    player_y -= 1
                elif event.key == pygame.K_DOWN and player_y < ROWS - 1:
                    player_y += 1
            
            if event.key == pygame.K_SPACE:
                # Check if player is on an ingredient station to pick up
                if kitchen_layout[player_y][player_x] == 'I':
                    item = ingredient_locations.get((player_y, player_x), None)
                    if item and item not in held_items:  # Avoid duplicates
                        held_items.append(item)
                
                # Start cooking if on a cooking station and holding necessary ingredients
                elif kitchen_layout[player_y][player_x] == 'C' and not is_cooking:
                    if tuple(sorted(held_items)) in burger_titles:
                        is_cooking = True
                        cook_start_time = time.time()
                
                # Serve burger if on a serving station
                elif kitchen_layout[player_y][player_x] == 'S' and not is_cooking:
                    if tuple(sorted(held_items)) in burger_titles:
                        if burger_titles[tuple(sorted(held_items))] == current_burger_type:
                            sandwich_counter += 1
                            held_items.clear()
                            current_burger_type = random.choice(required_burgers)  # Randomly select a new burger type

    # Update game state
    if is_cooking:
        elapsed_time = time.time() - cook_start_time
        if elapsed_time >= COOK_TIME:
            is_cooking = False
            if tuple(sorted(held_items)) not in burger_titles:
                game_failed = True  # Fail if the burger is not correct

    if sandwich_counter == len(required_burgers):  # Win condition: all required burgers made
        print("Congratulations! You've made all the required burgers!")
        break

    # Redraw everything
    screen.fill(WHITE)
    draw_grid()

    # Update the screen
    pygame.display.update()

    # Frame rate control
    pygame.time.Clock().tick(30)

pygame.quit()