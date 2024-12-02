import pygame
import time
import random
from Relationships import RelationshipGraph

class CoffeeGame:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.relationship_graph = RelationshipGraph()
        self.held_items = []
        self.is_cooking = False
        self.cook_start_time = 0
        self.current_coffee_type = None
        self.coffees_made = 0
        self.game_failed = False
        self.finished = False
        self.success = False
        self.player_x, self.player_y = 3, 2  # Start in the middle of the layout
        self.required_coffees = [
            "Black Coffee", "Creamy Black Coffee", "Latte", "Sweet Coffee",
            "Creamy Latte", "Sweet Creamy Coffee", "Sweet Latte", "Ultimate Latte"
        ]
        self.brew_titles = {
            tuple(sorted(["Coffee Beans"])): "Black Coffee",
            tuple(sorted(["Coffee Beans", "Creamer"])): "Creamy Black Coffee",
            tuple(sorted(["Coffee Beans", "Milk"])): "Latte",
            tuple(sorted(["Coffee Beans", "Sugar"])): "Sweet Coffee",
            tuple(sorted(["Coffee Beans", "Creamer", "Milk"])): "Creamy Latte",
            tuple(sorted(["Coffee Beans", "Sugar", "Creamer"])): "Sweet Creamy Coffee",
            tuple(sorted(["Coffee Beans", "Sugar", "Milk"])): "Sweet Latte",
            tuple(sorted(["Coffee Beans", "Creamer", "Sugar", "Milk"])): "Ultimate Latte",
        }
        self.kitchen_layout = [
            [' ', 'I', 'I', ' ', ' ', ' ', ' ', ' ', 'I', 'I'],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', 'C', 'C', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'S']
        ]
        self.ingredient_locations = {
            (0, 1): "Creamer",
            (0, 2): "Sugar",
            (0, 8): "Coffee Beans",
            (0, 9): "Milk"
        }
        self.COOK_TIME = 3  # Seconds to brew an item
        self.GRID_SIZE = 128
        self.load_images()
        self.coffee_recipes = {
            "Black Coffee": ["Coffee Beans"],
            "Creamy Black Coffee": ["Coffee Beans", "Creamer"],
            "Latte": ["Coffee Beans", "Milk"],
            "Sweet Coffee": ["Coffee Beans", "Sugar"],
            "Creamy Latte": ["Coffee Beans", "Creamer", "Milk"],
            "Sweet Creamy Coffee": ["Coffee Beans", "Sugar", "Creamer"],
            "Sweet Latte": ["Coffee Beans", "Sugar", "Milk"],
            "Ultimate Latte": ["Coffee Beans", "Creamer", "Sugar", "Milk"]
        }
        self.start_time = None
        self.time_limit = 30  # Base time limit of 45 seconds
        self.coffees_to_make = 3  # Number of coffees to make
        self.time_remaining = self.time_limit

    def load_images(self):
        self.player_image = pygame.image.load("assets/player0.png")
        self.player_image = pygame.transform.scale(self.player_image, (self.GRID_SIZE, self.GRID_SIZE))
        self.cooking_station_image = pygame.image.load("assets/Stove.png")
        self.cooking_station_image = pygame.transform.scale(self.cooking_station_image, (self.GRID_SIZE, self.GRID_SIZE))
        self.serving_station_image = pygame.image.load("assets/Table.png")
        self.serving_station_image = pygame.transform.scale(self.serving_station_image, (self.GRID_SIZE, self.GRID_SIZE))
        self.ingredient_images = {
            "Coffee Beans": pygame.transform.scale(pygame.image.load("assets/CoffeeBean.png"), (self.GRID_SIZE, self.GRID_SIZE)),
            "Sugar": pygame.transform.scale(pygame.image.load("assets/Sugar.png"), (self.GRID_SIZE, self.GRID_SIZE)),
            "Milk": pygame.transform.scale(pygame.image.load("assets/Milk.png"), (self.GRID_SIZE, self.GRID_SIZE)),
            "Creamer": pygame.transform.scale(pygame.image.load("assets/Greek Yogurt.png"), (self.GRID_SIZE, self.GRID_SIZE)),
        }

    def start_game(self):
        self.reset_game()
        self.finished = False
        self.success = False
        self.start_time = time.time()
        self.time_remaining = self.time_limit
        self.coffees_made = 0

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
                
                # Brew coffee at cooking station
                elif self.kitchen_layout[self.player_y][self.player_x] == 'C' and "Coffee Beans" in self.held_items:
                    if not self.is_cooking:
                        brewed_items_tuple = tuple(sorted(self.held_items))
                        if brewed_items_tuple in self.brew_titles:
                            self.is_cooking = True
                            self.cook_start_time = time.time()
                            print(f"Starting to brew: {self.brew_titles[brewed_items_tuple]}")
                        else:
                            self.show_result_message("The coffee you are trying to make does not exist!", (255, 165, 0))
                            pygame.time.wait(1000)
                            self.held_items = []
                
                # Serve brewed coffee
                elif self.kitchen_layout[self.player_y][self.player_x] == 'S' and self.held_items:
                    if len(self.held_items) == 1:  # Only allow serving if holding one item (a brewed coffee)
                        current_coffee = self.held_items[0]
                        if current_coffee in self.coffee_recipes:  # Check if it's a brewed coffee
                            print(f"Serving coffee: {current_coffee}")
                            print(f"Required coffee: {self.current_coffee_type}")
                            if current_coffee == self.current_coffee_type:
                                self.show_result_message("Success!", (0, 255, 0))
                                pygame.time.wait(1000)
                                self.coffees_made += 1
                                self.reset_game()
                            else:
                                self.show_result_message("Wrong Recipe!", (255, 0, 0))
                                pygame.time.wait(1000)
                                self.game_failed = True
                        else:
                            self.show_result_message("You need to brew the ingredients first!", (255, 165, 0))
                            pygame.time.wait(1000)

    def update(self):
        self.screen.fill((173, 216, 230))
        self.draw_grid()
        
        # Update brewing process
        if self.is_cooking and time.time() - self.cook_start_time >= self.COOK_TIME:
            self.is_cooking = False
            brewed_items_tuple = tuple(sorted(self.held_items))
            title = self.brew_titles.get(brewed_items_tuple)
            print(f"Finished brewing: {title}")
            self.held_items = [title]  # Replace ingredients with brewed coffee
            self.show_result_message("Coffee brewed!", (0, 255, 0))
            pygame.time.wait(1000)
        
        # Update time remaining
        if not self.finished:
            self.time_remaining = max(0, self.time_limit - (time.time() - self.start_time))
            if self.time_remaining <= 0:
                self.finished = True
                self.success = False
        
        if self.coffees_made >= self.coffees_to_make:
            self.finished = True
            self.success = True

    def draw_grid(self):
        for row in range(len(self.kitchen_layout)):
            for col in range(len(self.kitchen_layout[0])):
                x, y = col * self.GRID_SIZE, row * self.GRID_SIZE
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
        time_surface = self.font.render(time_text, True, (0, 0, 0))
        time_rect = time_surface.get_rect(midtop=(self.screen.get_width() // 2, 10))
        self.screen.blit(time_surface, time_rect)
        
        # Draw UI elements at the bottom left of the screen
        bottom_margin = 120  # Height from bottom
        x_position = 10  # 10px padding from left
        
        # Progress
        progress_text = f"Coffees Made: {self.coffees_made}/{self.coffees_to_make}"
        progress_surface = self.font.render(progress_text, True, (0, 0, 0))
        self.screen.blit(progress_surface, (x_position, self.screen.get_height() - bottom_margin))
        
        # Required coffee
        required_text = f"Required Coffee: {self.current_coffee_type}"
        required_surface = self.font.render(required_text, True, (0, 0, 0))
        self.screen.blit(required_surface, (x_position, self.screen.get_height() - bottom_margin + 30))
        
        # Held items
        item_text = f"Held Items: {', '.join(self.held_items) if self.held_items else 'None'}"
        text = self.font.render(item_text, True, (0, 0, 0))
        self.screen.blit(text, (x_position, self.screen.get_height() - bottom_margin + 60))
        
        # Recipe ingredients
        ingredients = self.coffee_recipes[self.current_coffee_type]
        ingredients_text = f"Required Ingredients: {', '.join(ingredients)}"
        ingredients_surface = self.font.render(ingredients_text, True, (0, 0, 0))
        self.screen.blit(ingredients_surface, (x_position, self.screen.get_height() - bottom_margin + 90))

    def reset_game(self):
        self.held_items = []
        self.is_cooking = False
        self.cook_start_time = 0
        self.current_coffee_type = random.choice(self.required_coffees)
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