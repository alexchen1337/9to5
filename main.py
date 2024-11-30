import pygame
from player import Player
from IntroScreen import IntroScreen
from EndScreen import EndScreen
from Meter import Meter  # Import your Meter class
from StoreRunner import runStore
from TaskList import TaskList
from TypingGame import TypingGame
from Relationships import RelationshipGraph
from Npc import NPC
from DayTransitionScreen import DayTransitionScreen

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

# Create NPCs
boss = NPC("./assets/player1.png", scale_factor=8, screen_width=SCREEN_WIDTH, screen_height=SCREEN_HEIGHT, 
           name="Boss", job_title="Regional Manager")
coworker = NPC("./assets/player2.png", scale_factor=8, screen_width=SCREEN_WIDTH, screen_height=SCREEN_HEIGHT, 
               name="Coworker", job_title="Assistant")

# Create NPC group
npc_group = pygame.sprite.Group()
npc_group.add(boss)
npc_group.add(coworker)

# Adjust the font size for meters (at the top with other font definitions)
meter_font_size = 18  # Smaller font for meters
meter_font = pygame.font.Font(font_path, meter_font_size)

# Function to draw a bar on the screen
def draw_meter(screen, meter, x, y, width=150, height=15, color=(0, 255, 0)):  # Reduced width and height
    # Calculate the fill ratio based on the meter's value
    fill_ratio = meter.get_value() / meter.max_value
    fill_width = int(width * fill_ratio)
    
    # Bar background
    pygame.draw.rect(screen, (50, 50, 50), (x, y, width, height))  # Gray background
    # Bar fill
    pygame.draw.rect(screen, color, (x, y, fill_width, height))  # Customizable fill color
    # Text label with smaller font and integer values
    text_surface = meter_font.render(f"{meter.name}: {int(meter.value)}/{meter.max_value}", True, text_color)
    screen.blit(text_surface, (x, y - meter_font_size))  # Position text above bar

# After initializing font
day_font = pygame.font.Font(font_path, 24)  # Smaller font for day display

# After initializing font
def draw_day_counter(screen, day, font):
    day_text = font.render(f"Day: {day}/{last_day}", True, text_color)
    day_rect = day_text.get_rect(midtop=(SCREEN_WIDTH // 2, 10))  # Center horizontally, 10px from top
    screen.blit(day_text, day_rect)

# Displays how to use store so the user knows to click E
def display_store_hint(screen):
    # Render the text for the store hint
    store_text = game_font.render("Store (Press E)", True, (255, 255, 255))  # White text
    store_text_rect = store_text.get_rect(midtop=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 40))  # Center horizontally, a bit above the bottom
    screen.blit(store_text, store_text_rect)

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

# Define the tasks for the office (replace with games)
tasks = [
    "Complete Typing Test",
    "Handle Email Inbox",
    "Make Coffee", 
    "Make Burgers"
]

# Initialize the TaskList (update position to top left)
task_list = TaskList(tasks, game_font, x=10, y=10, color=(255, 255, 255))

# After initializing player
relationship_graph = RelationshipGraph()  # Initialize relationship system
base_task_reward = 50  # Base reward for completing tasks
min_task_reward = 5    # Minimum reward possible

# Function to calculate reward based on boss relationship
def calculate_reward():
    boss_relationship = relationship_graph.get_relationship("player", "boss")
    # Every 20 points of relationship adds $5 to base reward
    relationship_bonus = (boss_relationship - 80) // 20 * 5  # Start bonus at 80 relationship
    reward = base_task_reward + relationship_bonus
    return max(min_task_reward, min(reward, 100))  # Cap between min_task_reward and 100

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
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_t:  # Toggle task list visibility
                task_list.toggle_visibility()
        
        # Move task handling to office screen (current_screen == 2)
        if current_screen == 2 and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1 and not task_list.is_completed(0):  # Typing Game
                typing_game = TypingGame(screen, game_font)
                typing_game.start_game()
                game_running = True
                
                while game_running:
                    for game_event in pygame.event.get():
                        if game_event.type == pygame.QUIT:
                            running = False
                            game_running = False
                        typing_game.handle_event(game_event)
                    
                    screen.fill((30, 30, 30))  # Dark background
                    typing_game.update()
                    pygame.display.flip()
                    
                    if typing_game.is_finished():
                        game_running = False
                        if typing_game.is_successful():
                            task_list.toggle_task(0)
                            player.energy.decrease(10)
                            # Increase relationship with boss on success
                            relationship_graph.increase_relationship("player", "boss", 5)  # Increase by 5 points
                            reward = calculate_reward()
                            player.checkings.increase(reward)
                            print(f"Earned ${reward} from typing task!")
                            print("Boss is impressed with your performance!")
                        else:
                            # Failed the game
                            relationship_graph.decrease_relationship("player", "boss", 10)
                            print("Boss is disappointed with your performance!")

            elif event.key == pygame.K_2 and not task_list.is_completed(1):  # Email Game
                # Similar structure for email game
                pass

    # Get key presses for player movement
    keys_pressed = pygame.key.get_pressed()

    # Update player position with boundary checks
    player_group.update(keys_pressed, SCREEN_WIDTH, SCREEN_HEIGHT)

    # Screen transition logic
    if (current_screen == 1 and player.rect.right >= SCREEN_WIDTH):
        # Show transition to work
        transition_screen = DayTransitionScreen(screen)
        waiting_for_transition = True
        
        while waiting_for_transition:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    waiting_for_transition = False
            
            if transition_screen.draw(current_day, going_to_work=True):
                waiting_for_transition = False
            clock.tick(FPS)
        
        current_screen = 2
        player.rect.left = 0 + 10
        player.health.decrease(10)
        task_list.reset_tasks()
        boss.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)
        coworker.rect.center = (SCREEN_WIDTH // 3, SCREEN_HEIGHT // 2)

    elif (current_screen == 2 and player.rect.left <= 0):
        # Show transition to home
        transition_screen = DayTransitionScreen(screen)
        waiting_for_transition = True
        
        while waiting_for_transition:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    waiting_for_transition = False
            
            if transition_screen.draw(current_day, going_to_work=False):
                waiting_for_transition = False
            clock.tick(FPS)
        
        current_screen = 1
        player.rect.right = SCREEN_WIDTH - 10
        current_day += 1

    # Fill the screen with a color
    if (current_screen == 1):
        background_image = pygame.image.load('./assets/HomeScreen.png')
        background_image = pygame.transform.scale(background_image, (1280, 720))
        screen.blit(background_image, (0,0))
    elif (current_screen == 2):
        screen.fill((50, 50, 150)) # Dark Blue
        task_list.draw(screen)  # Move task list to work screen
        # Update and draw NPCs in office
        npc_group.update(SCREEN_WIDTH, SCREEN_HEIGHT)
        npc_group.draw(screen)

        for npc in npc_group:
            npc.draw_minibar(screen, relationship_graph, npc.name.lower())
            npc.draw_name(screen)  # Draw name


    # Draw the player
    player_group.draw(screen)

    # Draw meters in bottom right corner
    draw_meter(screen, player.health, SCREEN_WIDTH - 300, SCREEN_HEIGHT - 100, width=200, height=20, color=(255, 0, 0))
    draw_meter(screen, player.energy, SCREEN_WIDTH - 300, SCREEN_HEIGHT - 50, width=200, height=20, color=(255, 255, 0))

    display_store_hint(screen) # tells user to press e if they want to use store

    # Money text
    money_text = meter_font.render(f"${player.checkings.get_value():.2f}", True, (0, 255, 0))
    money_rect = money_text.get_rect(bottomright=(SCREEN_WIDTH - 100, SCREEN_HEIGHT - 10))
    screen.blit(money_text, money_rect)

    # Draw day counter (moved to here, after other drawing operations)
    draw_day_counter(screen, current_day, day_font)

    # Update the display
    pygame.display.flip()

    # Limit the frame rate
    clock.tick(FPS)

    if keys_pressed[pygame.K_e]:  # Enter the store
        storeRunning = runStore(screen, game_font, player)

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

