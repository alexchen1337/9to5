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
        self.sandwich_counter = 0
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
            [' ', 'I', 'I', ' ', ' ', ' ', ' ', ' ', ' ', 'S'],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            ['C', 'C', ' ', ' ', 'I', 'I', 'I', ' ', ' ', ' ']
        ]
        self.ingredient_locations = {
            (0, 1): "Cheese",
            (0, 2): "Bun",
            (4, 5): "Lettuce",
            (4, 6): "Patty",
            (4, 4): "Tomato"
        }
        self.COOK_TIME = 3  # Seconds to cook a burger
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

    def load_images(self):
        self.player_image = pygame.image.load("assets/player0.png")
        self.player_image = pygame.transform.scale(self.player_image, (self.GRID_SIZE, self.GRID_SIZE))
        self.floor_tile_image = pygame.image.load("assets/Tile.png")
        self.floor_tile_image = pygame.transform.scale(self.floor_tile_image, (self.GRID_SIZE, self.GRID_SIZE))
        self.cooking_station_image = pygame.image.load("assets/Stove.png")
        self.cooking_station_image = pygame.transform.scale(self.cooking_station_image, (self.GRID_SIZE, self.GRID_SIZE))
        self.serving_station_image = pygame.image.load("assets/Table.png")
        self.serving_station_image = pygame.transform.scale(self.serving_station_image, (self.GRID_SIZE, self.GRID_SIZE))
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

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if not self.is_cooking and not self.game_failed:
                if event.key == pygame.K_LEFT and self.player_x > 0:
                    self.player_x -= 1
                elif event.key == pygame.K_RIGHT and self.player_x < len(self.kitchen_layout[0]) - 1:
                    self.player_x += 1
                elif event.key == pygame.K_UP and self.player_y > 0:
                    self.player_y -= 1
                elif event.key == pygame.K_DOWN and self.player_y < len(self.kitchen_layout) - 1:
                    self.player_y += 1

            if event.key == pygame.K_SPACE:
                if self.kitchen_layout[self.player_y][self.player_x] == 'I':
                    item = self.ingredient_locations.get((self.player_y, self.player_x), None)
                    if item and item not in self.held_items:
                        self.held_items.append(item)
                elif self.kitchen_layout[self.player_y][self.player_x] == 'C' and "Patty" in self.held_items and not self.is_cooking:
                    self.is_cooking = True
                    self.cook_start_time = time.time()
                elif self.kitchen_layout[self.player_y][self.player_x] == 'S' and self.held_items and not self.is_cooking:
                    brewed_items_tuple = tuple(sorted(self.held_items))
                    title = self.burger_titles.get(brewed_items_tuple, "Brewed Unknown")
                    if title == self.current_burger_type:
                        # Show success message
                        self.show_result_message("Success!", (0, 255, 0))  # Green text
                        pygame.time.wait(1000)  # Wait 1 second
                        self.sandwich_counter += 1
                        self.reset_game()
                    else:
                        # Show failure message
                        self.show_result_message("Wrong Recipe!", (255, 0, 0))  # Red text
                        pygame.time.wait(1000)  # Wait 1 second
                        self.game_failed = True

    def update(self):
        # Change from white to light blue background
        self.screen.fill((173, 216, 230))  # Light blue RGB
        self.draw_grid()
        if self.is_cooking and time.time() - self.cook_start_time >= self.COOK_TIME:
            self.is_cooking = False
        if self.sandwich_counter >= 5:
            self.finished = True
            self.success = True
        if self.game_failed:
            self.finished = True
            self.success = False

    def draw_grid(self):
        for row in range(len(self.kitchen_layout)):
            for col in range(len(self.kitchen_layout[0])):
                x, y = col * self.GRID_SIZE, row * self.GRID_SIZE
                self.screen.blit(self.floor_tile_image, (x, y))
                if self.kitchen_layout[row][col] == 'I':
                    ingredient = self.ingredient_locations.get((row, col), None)
                    if ingredient and ingredient in self.ingredient_images:
                        self.screen.blit(self.ingredient_images[ingredient], (x, y))
                elif self.kitchen_layout[row][col] == 'C':
                    self.screen.blit(self.cooking_station_image, (x, y))
                elif self.kitchen_layout[row][col] == 'S':
                    self.screen.blit(self.serving_station_image, (x, y))
        self.screen.blit(self.player_image, (self.player_x * self.GRID_SIZE, self.player_y * self.GRID_SIZE))
        item_text = f"Held Items: {', '.join(self.held_items) if self.held_items else 'None'}"
        text = self.font.render(item_text, True, (0, 0, 0))
        self.screen.blit(text, (10, self.screen.get_height() - 40))
        required_text = f"Required Burger: {self.current_burger_type}"
        required_surface = self.font.render(required_text, True, (0, 0, 0))
        self.screen.blit(required_surface, (10, self.screen.get_height() - 100))
        ingredients = self.burger_recipes[self.current_burger_type]
        ingredients_text = f"Required Ingredients: {', '.join(ingredients)}"
        ingredients_surface = self.font.render(ingredients_text, True, (0, 0, 0))
        self.screen.blit(ingredients_surface, (10, self.screen.get_height() - 70))

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
        # Create large text for the message
        large_font = pygame.font.Font(None, 74)  # Larger font size
        text_surface = large_font.render(message, True, color)
        text_rect = text_surface.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
        
        # Draw the message
        self.screen.blit(text_surface, text_rect)
        pygame.display.flip()