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

def draw_meter(screen, meter, x, y, width=200, height=20, color=(255, 255, 255)):
    # Draw background (empty meter)
    pygame.draw.rect(screen, (100, 100, 100), (x, y, width, height))
    # Draw filled portion
    fill_width = (meter.get_value() / meter.max_value) * width
    pygame.draw.rect(screen, color, (x, y, fill_width, height))
    # Draw meter text
    font = pygame.font.Font(None, 24)
    text = font.render(f"{meter.name}: {meter.get_value()}/{meter.max_value}", True, (255, 255, 255))
    screen.blit(text, (x, y - 20))
    
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
    
    # Combine all items into a single list for navigation
    all_items = health_items + energy_items + family_items
    selected_index = 0
    confirming_purchase = False
    
    while running:
        screen.fill(BG_COLOR)
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if confirming_purchase:
                        confirming_purchase = False  # If in purchase confirmation, cancel that first
                    else:
                        return False  # If not confirming purchase, exit store
                elif event.key == pygame.K_UP:
                    if not confirming_purchase:
                        selected_index = (selected_index - 1) % len(all_items)
                elif event.key == pygame.K_DOWN:
                    if not confirming_purchase:
                        selected_index = (selected_index + 1) % len(all_items)
                elif event.key == pygame.K_RETURN:
                    if confirming_purchase:
                        # Confirm purchase
                        handle_purchase(all_items[selected_index], player)
                        confirming_purchase = False
                    else:
                        confirming_purchase = True

        # Display items in columns
        x_positions = [100, 500, 900]
        y_offset = 100
        x_offset = 75

        # Display column headers
        display_text(screen, "Health Items", x_positions[0] + x_offset - 25, y_offset / 2, font)
        display_text(screen, "Energy Items", x_positions[1] + x_offset - 25, y_offset / 2, font)
        display_text(screen, "Family Happiness Items", x_positions[2] - 50, y_offset / 2, font)

        # Display all items
        current_index = 0
        for items, x_pos in zip([health_items, energy_items, family_items], x_positions):
            for i, item in enumerate(items):
                button_rect = pygame.Rect(x_pos - x_offset + 60, y_offset + i * 70, 335, 50)
                
                # Highlight selected item
                if current_index == selected_index:
                    pygame.draw.rect(screen, (255, 255, 0), button_rect)  # Yellow highlight
                else:
                    pygame.draw.rect(screen, BUTTON_COLOR, button_rect)
                
                # Draw item image
                image = load_item_image(item.name)
                if image:
                    screen.blit(image, (x_pos - x_offset, y_offset + i * 70))
                
                # Draw item text
                text_surface = font.render(f"{item.name} - ${item.price}", True, TEXT_COLOR)
                screen.blit(text_surface, (x_pos - x_offset + 70, y_offset + i * 70 + 10))
                
                current_index += 1

        # Display confirmation dialog
        if confirming_purchase:
            selected_item = all_items[selected_index]
            dialog_rect = pygame.Rect(WIDTH//2 - 200, HEIGHT//2 - 100, 400, 200)
            pygame.draw.rect(screen, (200, 200, 200), dialog_rect)
            display_text(screen, f"Buy {selected_item.name} for ${selected_item.price}?", 
                        WIDTH//2 - 150, HEIGHT//2 - 50, font)
            display_text(screen, "Press ENTER to confirm", WIDTH//2 - 150, HEIGHT//2, font)
            display_text(screen, "Press ESC to cancel", WIDTH//2 - 150, HEIGHT//2 + 50, font)

        # Display messages and meters
        if message_display_counter > 0:
            display_text(screen, insufficient_funds_message, WIDTH//2 - 300, HEIGHT - 200, font, ERROR_COLOR)
            message_display_counter -= 1

        # Draw meters and money display - centered under store items
        meter_y = HEIGHT - 100  # Position meters higher up
        meter_spacing = 250  # Space between meters
        meter_start_x = (WIDTH - (meter_spacing * 2 + 200)) // 2  # Center all three meters
        
        # Health meter
        draw_meter(screen, player.health, meter_start_x, meter_y, width=200, height=20, color=(255, 0, 0))
        # Energy meter
        draw_meter(screen, player.energy, meter_start_x + meter_spacing, meter_y, width=200, height=20, color=(255, 255, 0))
        # Money display
        money_text = font.render(f"${player.checkings.get_value():.2f}", True, (0, 255, 0))
        money_rect = money_text.get_rect(center=(meter_start_x + meter_spacing * 2 + 100, meter_y + 10))
        screen.blit(money_text, money_rect)

        # Controls text moved below meters
        controls_text = "Use UP/DOWN to navigate, ENTER to select, ESC to exit"
        controls_surface = font.render(controls_text, True, TEXT_COLOR)
        controls_rect = controls_surface.get_rect(centerx=WIDTH // 2, bottom=HEIGHT - 10)
        screen.blit(controls_surface, controls_rect)

        pygame.display.flip()

# Display text helper function
def display_text(screen, text, x, y, font, color=(0, 0, 0)):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))


