import pygame
import os
from store import Store
from Meter import Meter
from player import Player

# Constants
WIDTH, HEIGHT = 1280, 720  # Screen dimensions for 1280x720 resolution
BG_COLOR = (160, 160, 160)
BUTTON_COLOR = (0, 128, 255)
TEXT_COLOR = (255, 255, 255)
ERROR_COLOR = (255, 0, 0)

# Store
store = Store()
family_meter = Meter("Family Happiness", 100)
family_meter.decrease(50)

# Separate items by type and sort by price
health_items = sorted([item for item in store.items if item.type == "Health"], key=lambda x: x.price)
energy_items = sorted([item for item in store.items if item.type == "Energy"], key=lambda x: x.price)
family_items = sorted([item for item in store.items if item.type == "Family Happiness"], key=lambda x: x.price)

# Load images for each item
def load_item_image(item_name):
    try:
        image_path = os.path.join("assets", f"{item_name}.png")
        image = pygame.image.load(image_path)
        image = pygame.transform.scale(image, (50, 50))  # Resize to fit next to the button
        return image
    except pygame.error:
        print(f"Image for {item_name} not found.")
        return None

# Button setup with image
def create_button_with_image(screen, x, y, width, height, item, font):
    # Draw button
    button_rect = pygame.Rect(x + 60, y, width, height)  # Offset x to make room for the image
    pygame.draw.rect(screen, BUTTON_COLOR, button_rect)
    text_surface = font.render(f"{item.name} - ${item.price}", True, TEXT_COLOR)
    screen.blit(text_surface, (x + 70, y + 10))  # Text offset for alignment with image

    # Draw image if available
    image = load_item_image(item.name)
    if image:
        screen.blit(image, (x, y))  # Place image to the left of the button

    return button_rect

# Global message variable
insufficient_funds_message = ""
message_display_counter = 0  # Counter to control message display duration

# Event handling for purchasing items
def handle_purchase(item, player):
    global insufficient_funds_message, message_display_counter
    if player.checkings.get_value() >= item.price:  # Check if player can afford the item
        player.checkings.decrease(item.price)  # Deduct the price

        # Adjust the appropriate meter
        if item.type == "Health":
            player.health.increase(item.magnitude)
        elif item.type == "Energy":
            player.energy.increase(item.magnitude)
        elif item.type == "Family Happiness":
            family_meter.increase(item.magnitude)
        
        # Clear the message when purchase is successful
        insufficient_funds_message = ""
    else:
        # Update message and reset counter for display
        insufficient_funds_message = "Not enough money to purchase this item!"
        message_display_counter = 60  # Display message for 60 frames

# Main loop
def runStore(screen, font, player):
    global message_display_counter, insufficient_funds_message
    running = True
    while running:
        screen.fill(BG_COLOR)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                for button, item in buttons:
                    if button.collidepoint(x, y):
                        handle_purchase(item, player)

        # Create and display buttons with images for each type in separate columns
        buttons = []
        x_positions = [100, 500, 900]  # X positions for Health, Energy, and Family Happiness columns
        y_offset = 100  # Initial Y offset for the first button
        x_offset = 75   # Initial X offset used for alignment

        # Display Health items in the first column
        display_text(screen, "Health Items", x_positions[0] + x_offset - 25, y_offset / 2, font)
        for i, item in enumerate(health_items):
            button = create_button_with_image(screen, x_positions[0] - x_offset, y_offset + i * 70, 335, 50, item, font)
            buttons.append((button, item))

        # Display Energy items in the second column
        display_text(screen, "Energy Items", x_positions[1] + x_offset - 25, y_offset / 2, font)
        for i, item in enumerate(energy_items):
            button = create_button_with_image(screen, x_positions[1] - x_offset, y_offset + i * 70, 335, 50, item, font)
            buttons.append((button, item))

        # Display Family Happiness items in the third column
        display_text(screen, "Family Happiness Items", x_positions[2] - 50, y_offset / 2, font)
        for i, item in enumerate(family_items):
            button = create_button_with_image(screen, x_positions[2] - x_offset, y_offset + i * 70, 335, 50, item, font)
            buttons.append((button, item))

        # Display the insufficient funds message if it exists
        if message_display_counter > 0:
            display_text(screen, insufficient_funds_message, WIDTH // 2 - 300, HEIGHT - 200, font, ERROR_COLOR)
            message_display_counter -= 1

        # Display meter values and player money
        display_text(screen, f"Health: {player.health.get_value():.0f}", x_positions[0] + x_offset, HEIGHT - 100, font)
        display_text(screen, f"Energy: {player.energy.get_value():.0f}", x_positions[1] + x_offset, HEIGHT - 100, font)
        display_text(screen, f"Family Happiness: {family_meter.get_value():.0f}", x_positions[2], HEIGHT - 100, font)
        display_text(screen, f"Money: ${player.checkings.get_value():.2f}", x_positions[1] + x_offset, HEIGHT - 50, font)

        pygame.display.flip()

# Display text helper function
def display_text(screen, text, x, y, font, color=(0, 0, 0)):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))
