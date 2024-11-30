import pygame
import time
import random
from IntroScreen import IntroScreen 
from player import Player
from Relationships import RelationshipGraph

# Initialize pygame
pygame.init()
relationship_graph = RelationshipGraph()

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
pygame.display.set_caption("Overcooked-style Game Layout")

# Define kitchen layout and ingredient locations
kitchen_layout = [
    [' ', 'I', 'I', ' ', ' ', ' ', ' ', ' ', ' ', 'S'],  # I = Ingredient, C = Cooking, S = Serving
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    ['C', 'C', ' ', ' ', ' ', 'I', 'I', ' ', ' ', ' ']
]

# Ingredient types at specific locations
ingredient_locations = {
    (0, 1): "Creamer",
    (0, 2): "Sugar",
    (4, 5): "Coffee Beans",
    (4, 6): "Milk"
}

# Brewed item titles based on combinations
brew_titles = {
    tuple(sorted(["Coffee Beans"])): "Black Coffee",
    tuple(sorted(["Coffee Beans", "Creamer"])): "Creamy Black Coffee",
    tuple(sorted(["Coffee Beans", "Milk"])): "Latte",
    tuple(sorted(["Coffee Beans", "Sugar"])): "Sweet Coffee",
    tuple(sorted(["Coffee Beans", "Creamer", "Milk"])): "Creamy Latte",
    tuple(sorted(["Coffee Beans", "Sugar", "Creamer"])): "Sweet Creamy Coffee",
    tuple(sorted(["Coffee Beans", "Sugar", "Milk"])): "Sweet Latte",
    tuple(sorted(["Coffee Beans", "Creamer", "Sugar", "Milk"])): "Ultimate Latte",
}

# List of required coffee types
required_coffees = [
    "Black Coffee",
    "Creamy Black Coffee",
    "Latte",
    "Sweet Coffee",
    "Creamy Latte",
    "Sweet Creamy Coffee",
    "Sweet Latte",
    "Ultimate Latte"
]

# Player starting position
player_x, player_y = 3, 2  # Start in the middle of the layout
held_items = []  # List to track what the player is holding
is_cooking = False
cook_start_time = 0
COOK_TIME = 3  # Seconds to brew an item
current_coffee_type = random.choice(required_coffees)  # Randomly select a new coffee type
game_failed = False  # Track game state

# Add a new global variable to track the number of coffees made
coffees_made = 0  # Initialize counter for brewed coffees

# Load images for player, floor tiles, and stations
# sprite_paths = [
#     "./assets/player0.png",
#     "./assets/player1.png",
#     "./assets/player2.png"
# ]
# intro_screen = IntroScreen(screen, sprite_paths)
# selected_sprite = intro_screen.selected_sprite
# player = selected_sprite
# player_image = Player(selected_sprite, scale_factor=8, screen_width=SCREEN_WIDTH, screen_height=SCREEN_HEIGHT)

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
    "Coffee Beans": pygame.transform.scale(
        pygame.image.load("assets/CoffeeBean.png"), (GRID_SIZE, GRID_SIZE)
    ),
    "Sugar": pygame.transform.scale(
        pygame.image.load("assets/Sugar.png"), (GRID_SIZE, GRID_SIZE)
    ),
    "Milk": pygame.transform.scale(
        pygame.image.load("assets/Milk.png"), (GRID_SIZE, GRID_SIZE)
    ),
    "Creamer": pygame.transform.scale(
        pygame.image.load("assets/Greek Yogurt.png"), (GRID_SIZE, GRID_SIZE)
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

    # Draw required coffee type
    required_text = f"Required Coffee: {current_coffee_type}"
    required_surface = font.render(required_text, True, (0, 0, 0))
    screen.blit(required_surface, (10, SCREEN_HEIGHT - 70))

    # Draw brewing progress bar if brewing
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
    global held_items, is_cooking, cook_start_time, current_coffee_type, player_x, player_y, game_failed
    held_items = []
    is_cooking = False
    cook_start_time = 0
    current_coffee_type = random.choice(required_coffees)  # Randomly select a new coffee type
    player_x, player_y = 3, 2  # Reset player position
    game_failed = False  # Reset failure state

def evaluate_performance():
    if coffees_made >= 6:
        relationship_graph.increase_relationship("player", "boss", 20)
        print("Boss happiness increased due to good performance!")
    elif game_failed:
        relationship_graph.decrease_relationship("player", "boss", 20)
        print("Boss happiness decreased due to poor performance!")
    else:
        relationship_graph.increase_relationship("player", "boss", 5)
        print("Boss happiness increased due to good performance!")
    relationship_graph.check_thresholds()

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if not is_cooking and not game_failed:  # Prevent movement while brewing or after failure
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

                # Start brewing if on a cooking station and holding "Coffee Beans"
                elif kitchen_layout[player_y][player_x] == 'C' and "Coffee Beans" in held_items and not is_cooking:
                    is_cooking = True
                    cook_start_time = time.time()

                elif kitchen_layout[player_y][player_x] == 'S' and held_items and not is_cooking:
                    # Convert held items to a sorted tuple for lookup
                    brewed_items_tuple = tuple(sorted(held_items))
                    title = brew_titles.get(brewed_items_tuple, "Brewed Unknown")  # Default to "Unknown"

                    # Check if the brewed item matches the required coffee type
                    if title == current_coffee_type:
                        print(f"Served: {title} - SUCCESS!")
                        held_items = [title]  # Update held items with the brewed title
                        coffees_made += 1  # Increment the number of successfully brewed coffees
                        reset_game()  # Restart the game with a new coffee requirement
                    else:
                        game_failed = True  # Set game failed state
                        print(f"Served: {title} - FAILED! Required: {current_coffee_type}")

    # Check if brewing time has finished
    if is_cooking:
        if time.time() - cook_start_time >= COOK_TIME:
            is_cooking = False
            print("Brewing complete!")

    if coffees_made >= 5:
        print("5 Coffees Made! Hopefully you don't get fired!")
        evaluate_performance()
        running = False  # End the game

    # Check if time is up and show the failed message
    if game_failed:
        pygame.time.delay(2000)  # Wait for 2 seconds before reset
        evaluate_performance()
        reset_game()

    # Redraw everything
    screen.fill(WHITE)
    draw_grid()

    # Update the screen
    pygame.display.update()

    # Frame rate control
    pygame.time.Clock().tick(30)

pygame.quit()