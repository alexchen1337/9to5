import pygame
import time
import random

# Initialize pygame
pygame.init()

# Screen dimensions and grid settings
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
GRID_SIZE = 100  # Size of each grid cell
COLUMNS, ROWS = 8, 5  # Set based on kitchen_layout dimensions

# Colors
WHITE = (255, 255, 255)
GREY = (200, 200, 200)
COOKING_BAR_COLOR = (255, 69, 0)  # Progress bar color
FAIL_COLOR = (255, 0, 0)  # Color for failed message
SUCCESS_COLOR = (0, 255, 0)  # Color for success message

# Create screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Overcooked-style Game Layout")

# Define kitchen layout and ingredient locations
kitchen_layout = [
    [' ', 'I', 'I', ' ', ' ', ' ', ' ', 'S'],  # I = Ingredient, C = Cooking, S = Serving
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    ['C', 'C', ' ', ' ', 'I', 'I', 'I', ' ']
]

# Ingredient types at specific locations
ingredient_locations = {
    (0, 1): "Cheese",
    (0, 2): "Bun",
    (4, 5): "Lettuce",
    (4, 6): "Patty",
    (4, 4): "Tomato"
}

# Burger titles based on combinations

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
                # move with arrow keys
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
                elif kitchen_layout[player_y][player_x] == 'C' and all(ingredient in held_items for ingredient in ["Bun", "Patty"]) and not is_cooking:
                    is_cooking = True
                    cook_start_time = time.time()
                
                # Check if the player is serving the correct burger
                elif kitchen_layout[player_y][player_x] == 'S' and held_items and not is_cooking:
                    # Get the title based on the held items
                    held_items_tuple = tuple(sorted(held_items))  # Convert held items to sorted tuple
                    title = burger_titles.get(held_items_tuple, "Made Unknown")  # Default title if not found

                    # Check if the cooked burger matches the required burger type
                    if title == current_burger_type:
                        print(f"Success! You made a {title}.")
                        held_items = []
                        current_burger_type = random.choice(required_burgers)  # Pick a new required burger
                    else:
                        game_failed = True
                        print("Game Over - Incorrect burger")


    # Update the game screen
    screen.fill(WHITE)
    draw_grid()

    pygame.display.update()

    # Game timeout condition (you can change the logic to your desired timeout)
    if time.time() - cook_start_time > COOK_TIME and is_cooking:
        is_cooking = False  # Automatically stop cooking after the time is up

    # Check if time is up and show the failed message
    if game_failed:
        pygame.time.delay(3000)  # Wait for 3 seconds before reset
        reset_game()

    time.sleep(0.1)  # Control frame rate

# Close pygame

pygame.quit()