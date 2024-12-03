import pygame
import time
import random
from Relationships import RelationshipGraph

class SandwichGame:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.relationship_graph = RelationshipGraph()
        self.held_items = []
        self.is_cooking = False
        self.cook_start_time = 0
        self.current_burger_type = None
        self.burgers_made_made = 0
        self.game_failed = False
        self.finished = False
        self.success = False
        self.player_x, self.player_y = 3, 2  # Start in the middle of the layout

        self.required_burgers = [
            "Cheeseburger", "Tomato Burger", "Lettuce Burger",
            "Cheese Tomato Burger", "Cheese Lettuce Burger", "Ultimate Burger"
        ]

        self.burger_titles = {
            tuple(sorted(["Cheese", "Bun", "Patty"])): "Cheeseburger",
            tuple(sorted(["Tomato", "Bun", "Patty"])): "Tomato Burger",
            tuple(sorted(["Lettuce", "Bun", "Patty"])): "Lettuce Burger",
            tuple(sorted(["Cheese", "Tomato", "Bun", "Patty"])): "Cheese Tomato Burger",
            tuple(sorted(["Cheese", "Lettuce", "Bun", "Patty"])): "Cheese Lettuce Burger",
            tuple(sorted(["Cheese", "Tomato", "Lettuce", "Bun", "Patty"])): "Ultimate Burger",
        }

        self.kitchen_layout = [
            [' ', 'I', 'I', ' ', ' ', ' ', ' ', 'I', 'I', 'I'],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', 'C', 'C', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'S']
        ]

        self.ingredient_locations = {
            (0, 1): "Patty",
            (0, 2): "Bun",
            (0, 7): "Cheese",
            (0, 8): "Lettuce",
            (0, 9): "Tomato"
        }

        self.COOK_TIME = 3  # Seconds to cook an item
        self.GRID_SIZE = 128
        self.load_images()

        self.burger_recipes = {
            "Cheeseburger": ["Cheese", "Bun", "Patty"],
            "Tomato Burger": ["Tomato", "Bun", "Patty"],
            "Lettuce Burger": ["Lettuce", "Bun", "Patty"],
            "Cheese Tomato Burger": ["Cheese", "Tomato", "Bun", "Patty"],
            "Cheese Lettuce Burger": ["Cheese", "Lettuce", "Bun", "Patty"],
            "Ultimate Burger": ["Cheese", "Tomato", "Lettuce", "Bun", "Patty"]
        }
        self.time_limit = 60  # Base time limit of 60 seconds

        self.start_time = None
        self.time_limit = 45  # 45 seconds
        self.burgers_to_make = 3  # Number of burgers to make
        self.time_remaining = self.time_limit

    def load_images(self):
        self.player_image = pygame.image.load("assets/player0.png")
        self.player_image = pygame.transform.scale(self.player_image, (self.GRID_SIZE, self.GRID_SIZE))
        # self.floor_tile_image = pygame.image.load("assets/Tile.png")
        # self.floor_tile_image = pygame.transform.scale(self.floor_tile_image, (self.GRID_SIZE, self.GRID_SIZE))
        self.cooking_station_image = pygame.image.load("assets/Stove.png")
        self.cooking_station_image = pygame.transform.scale(self.cooking_station_image, (self.GRID_SIZE, self.GRID_SIZE))
        self.serving_station_image = pygame.image.load("assets/plate.png")
        self.serving_station_image = pygame.transform.scale(self.serving_station_image, (self.GRID_SIZE, self.GRID_SIZE))
        self.wood_flooring_image = pygame.image.load("assets/wood_flooring.png")
        self.wood_flooring_image = pygame.transform.scale(self.wood_flooring_image, (self.GRID_SIZE, self.GRID_SIZE))

        self.ingredient_images = {
            "Cheese": pygame.transform.scale(pygame.image.load("assets/Cheese.png"), (self.GRID_SIZE, self.GRID_SIZE)),
            "Tomato": pygame.transform.scale(pygame.image.load("assets/Tomato.png"), (self.GRID_SIZE, self.GRID_SIZE)),
            "Lettuce": pygame.transform.scale(pygame.image.load("assets/Lettuce.png"), (self.GRID_SIZE, self.GRID_SIZE)),
            "Patty": pygame.transform.scale(pygame.image.load("assets/Meat.png"), (self.GRID_SIZE, self.GRID_SIZE)),
            "Bun": pygame.transform.scale(pygame.image.load("assets/Bun.png"), (self.GRID_SIZE, self.GRID_SIZE)),
        }

    def start_game(self):
        self.reset_game()
        self.finished = False
        self.success = False
        self.start_time = time.time()
        self.time_remaining = self.time_limit
        self.burgers_made = 0

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            # Handle movement - always allow if not game_failed
            if not self.game_failed:
                if event.key == pygame.K_LEFT and self.player_x > 0:
                    self.player_x -= 1
                elif event.key == pygame.K_RIGHT and self.player_x < len(self.kitchen_layout[0]) - 1:
                    self.player_x += 1
                elif event.key == pygame.K_UP and self.player_y > 0:
                    self.player_y -= 1
                elif event.key == pygame.K_DOWN and self.player_y < len(self.kitchen_layout) - 1:
                    self.player_y += 1

            # Handle space bar actions separately
            if event.key == pygame.K_SPACE and not self.game_failed:
                # Collect ingredients
                if self.kitchen_layout[self.player_y][self.player_x] == 'I':
                    item = self.ingredient_locations.get((self.player_y, self.player_x), None)
                    if item and item not in self.held_items:
                        self.held_items.append(item)
                        self.held_items.sort()
                
                # cook a burger at cooking station
                elif self.kitchen_layout[self.player_y][self.player_x] == 'C' and "Patty" in self.held_items:
                    if not self.is_cooking:
                        cooked_items_tuple = tuple(sorted(self.held_items))
                        if cooked_items_tuple in self.cook_titles:
                            self.is_cooking = True
                            self.cook_start_time = time.time()
                            print(f"Starting to cook: {self.cook_titles[cooked_items_tuple]}")
                        else:
                            self.show_result_message("The burger you are trying to make does not exist!", (255, 165, 0))
                            pygame.time.wait(1000)
                            self.held_items = []
                
                # Serve cooked burger
                elif self.kitchen_layout[self.player_y][self.player_x] == 'S' and self.held_items:
                    if len(self.held_items) == 1:  # Only allow serving if holding one item (a cooked burger)
                        current_burger = self.held_items[0]
                        if current_burger in self.burger_recipes:  # Check if it's a cooked burger
                            print(f"Serving burger: {current_burger}")
                            print(f"Required burger: {self.current_burger_type}")
                            if current_burger == self.current_burger_type:
                                self.show_result_message("Success!", (0, 255, 0))
                                pygame.time.wait(1000)
                                self.burgers_made += 1
                                self.reset_game()
                            else:
                                self.show_result_message("Wrong Recipe!", (255, 0, 0))
                                pygame.time.wait(1000)
                                self.game_failed = True
                        else:
                            self.show_result_message("You need to cook the ingredients first!", (255, 165, 0))
                            pygame.time.wait(1000)

    def update(self):
        self.screen.fill((0, 0, 0))
        self.draw_grid()
        
        # Update cooking process
        if self.is_cooking and time.time() - self.cook_start_time >= self.COOK_TIME:
            self.is_cooking = False
            cooked_items_tuple = tuple(sorted(self.held_items))
            title = self.cook_titles.get(cooked_items_tuple)
            print(f"Finished cooking: {title}")
            self.held_items = [title]  # Replace ingredients with cooked burger
            self.show_result_message("Burger cooked!", (0, 255, 0))
            pygame.time.wait(1000)
        
        # Update time remaining
        if not self.finished:
            self.time_remaining = max(0, self.time_limit - (time.time() - self.start_time))
            if self.time_remaining <= 0:
                self.finished = True
                self.success = False
        
        if self.burgers_made >= self.burgers_to_make:
            self.finished = True
            self.success = True

    def draw_grid(self):
        for row in range(len(self.kitchen_layout)):
            for col in range(len(self.kitchen_layout[0])):
                x, y = col * self.GRID_SIZE, row * self.GRID_SIZE
                self.screen.blit(self.wood_flooring_image, (x, y))
                if self.kitchen_layout[row][col] == 'I':
                    ingredient = self.ingredient_locations.get((row, col), None)
                    if ingredient and ingredient in self.ingredient_images:
                        self.screen.blit(self.ingredient_images[ingredient], (x, y))
                elif self.kitchen_layout[row][col] == 'C':
                    self.screen.blit(self.cooking_station_image, (x, y))
                elif self.kitchen_layout[row][col] == 'S':
                    self.screen.blit(self.serving_station_image, (x, y))
        self.screen.blit(self.player_image, (self.player_x * self.GRID_SIZE, self.player_y * self.GRID_SIZE))
        
        # Draw timer at the top center
        time_text = f"Time: {int(self.time_remaining)}s"
        time_surface = self.font.render(time_text, True, (255, 255, 255))
        time_rect = time_surface.get_rect(midtop=(self.screen.get_width() // 2, 10))
        self.screen.blit(time_surface, time_rect)
        
        # Draw UI elements at the bottom left of the screen
        bottom_margin = 120  # Height from bottom
        x_position = 10  # 10px padding from left
        
        # Progress
        progress_text = f" Burgers Made: {self.burgers_made}/{self.burgers_to_make}"
        progress_surface = self.font.render(progress_text, True, (255, 255, 255))
        self.screen.blit(progress_surface, (x_position, self.screen.get_height() - bottom_margin))
        
        # Required burger
        required_text = f"Required Burger: {self.current_burger_type}"
        required_surface = self.font.render(required_text, True, (255, 255, 255))
        self.screen.blit(required_surface, (x_position, self.screen.get_height() - bottom_margin + 30))
        
        # Held items
        item_text = f"Held Items: {', '.join(self.held_items) if self.held_items else 'None'}"
        text = self.font.render(item_text, True, (255, 255, 255))
        self.screen.blit(text, (x_position, self.screen.get_height() - bottom_margin + 60))
        
        # Recipe ingredients
        ingredients = self.burger_recipes[self.current_burger_type]
        ingredients_text = f"Required Ingredients: {', '.join(ingredients)}"
        ingredients_surface = self.font.render(ingredients_text, True, (255, 255, 255))
        self.screen.blit(ingredients_surface, (x_position, self.screen.get_height() - bottom_margin + 90))

    def reset_game(self):
        self.held_items = []
        self.is_cooking = False
        self.cook_start_time = 0
        self.current_burger_type = random.choice(self.required_burgers)
        self.player_x, self.player_y = 3, 2
        self.game_failed = False

    def is_finished(self):
        return self.finished

    def is_successful(self):
        return self.success

    def show_result_message(self, message, color):
        # Create semi-transparent overlay
        overlay = pygame.Surface((self.screen.get_width(), self.screen.get_height()))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(128)
        self.screen.blit(overlay, (0, 0))
        
        # Create large text for the message
        large_font = pygame.font.Font(None, 74)
        text_surface = large_font.render(message, True, color)
        text_rect = text_surface.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
        
        # Draw the message
        self.screen.blit(text_surface, text_rect)
        pygame.display.flip()