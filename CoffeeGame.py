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
            [' ', 'I', 'I', ' ', ' ', ' ', ' ', ' ', ' ', 'S'],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            ['C', 'C', ' ', ' ', ' ', 'I', 'I', ' ', ' ', ' ']
        ]
        self.ingredient_locations = {
            (0, 1): "Creamer",
            (0, 2): "Sugar",
            (4, 5): "Coffee Beans",
            (4, 6): "Milk"
        }
        self.COOK_TIME = 3  # Seconds to brew an item
        self.GRID_SIZE = 128
        self.load_images()

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
            "Coffee Beans": pygame.transform.scale(pygame.image.load("assets/CoffeeBean.png"), (self.GRID_SIZE, self.GRID_SIZE)),
            "Sugar": pygame.transform.scale(pygame.image.load("assets/Sugar.png"), (self.GRID_SIZE, self.GRID_SIZE)),
            "Milk": pygame.transform.scale(pygame.image.load("assets/Milk.png"), (self.GRID_SIZE, self.GRID_SIZE)),
            "Creamer": pygame.transform.scale(pygame.image.load("assets/Greek Yogurt.png"), (self.GRID_SIZE, self.GRID_SIZE)),
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
                elif self.kitchen_layout[self.player_y][self.player_x] == 'C' and "Coffee Beans" in self.held_items and not self.is_cooking:
                    self.is_cooking = True
                    self.cook_start_time = time.time()
                elif self.kitchen_layout[self.player_y][self.player_x] == 'S' and self.held_items and not self.is_cooking:
                    brewed_items_tuple = tuple(sorted(self.held_items))
                    title = self.brew_titles.get(brewed_items_tuple, "Brewed Unknown")
                    if title == self.current_coffee_type:
                        self.coffees_made += 1
                        self.reset_game()
                    else:
                        self.game_failed = True

    def update(self):
        self.screen.fill((255, 255, 255))
        self.draw_grid()
        if self.is_cooking and time.time() - self.cook_start_time >= self.COOK_TIME:
            self.is_cooking = False
        if self.coffees_made >= 5:
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
        required_text = f"Required Coffee: {self.current_coffee_type}"
        required_surface = self.font.render(required_text, True, (0, 0, 0))
        self.screen.blit(required_surface, (10, self.screen.get_height() - 70))

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