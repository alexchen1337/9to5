import pygame
from player import Player
from IntroScreen import IntroScreen
from EndScreen import EndScreen
from Meter import Meter  
from StoreRunner import runStore
from TaskList import TaskList
from TypingGame import TypingGame
from EmailGame import EmailGame
from Relationships import RelationshipGraph
from Npc import NPC
from DayTransitionScreen import DayTransitionScreen
from SandwichGame import SandwichGame 
from CoffeeGame import CoffeeGame  
from CutsceneScreen import CutsceneScreen
import random

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
boss = NPC("./assets/boss.png", scale_factor=8, screen_width=SCREEN_WIDTH, screen_height=SCREEN_HEIGHT, 
           name="Boss", job_title="Regional Manager")
coworker = NPC("./assets/coworker.png", scale_factor=8, screen_width=SCREEN_WIDTH, screen_height=SCREEN_HEIGHT, 
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
def get_daily_tasks(day):
    all_tasks = [
        "Complete Typing Test",
        "Handle Email Inbox",
        "Make Coffee",
        "Make Burgers"
    ]
    
    # First 4 days: one specific task per day
    if day == 1:
        return ["Complete Typing Test"]
    elif day == 2:
        return ["Handle Email Inbox"]
    elif day == 3:
        return ["Make Coffee"]
    elif day == 4:
        return ["Make Burgers"]
    # Days 5-10: 2 random tasks
    elif 5 <= day <= 10:
        return random.sample(all_tasks, 2)
    # Days 11-20: 3 random tasks
    elif 11 <= day <= 20:
        return random.sample(all_tasks, 3)
    # Days 21-30: all 4 tasks in random order
    else:
        return random.sample(all_tasks, 4)

# Replace the tasks initialization with:
tasks = get_daily_tasks(current_day)
task_list = TaskList(tasks, game_font, x=10, y=10, color=(255, 255, 255))

# After initializing task_list and before the main game loop
tasks_for_today = tasks.copy()  # Create a copy of the tasks list to use for today

# After initializing player
relationship_graph = RelationshipGraph()  # Initialize relationship system
base_task_reward = 50  # Base reward for completing tasks
min_task_reward = 5    # Minimum reward possible

# Function to calculate reward based on boss relationship
def calculate_reward(relationship_graph):
    boss_relationship = relationship_graph.get_relationship("player", "boss")
    base_reward = 15  # Base reward
    
    # Calculate multiplier based on relationship (0.5x to 2x)
    relationship_multiplier = boss_relationship / 50  # 50 is neutral point
    relationship_multiplier = max(0.5, min(2.0, relationship_multiplier))  # Clamp between 0.5x and 2x
    
    final_reward = base_reward * relationship_multiplier
    return round(final_reward, 2)  # Round to 2 decimal places

# After pygame.init(), add this with the other image loads:
office_background = pygame.image.load('./assets/office.jpeg')
office_background = pygame.transform.scale(office_background, (1280, 720))

def run_game(game):
    game.start_game()
    
    # If it's day 30, halve the time limit for any game that has one
    if current_day == 30:
        if hasattr(game, 'time_limit'):
            game.time_limit = game.time_limit / 2
            print("FINAL DAY: Time limits halved! Good luck!")
    
    game_running = True
    while game_running:
        for game_event in pygame.event.get():
            if game_event.type == pygame.QUIT:
                return False
            game.handle_event(game_event)
        
        screen.fill((30, 30, 30))
        game.update()
        pygame.display.flip()
        
        if game.is_finished():
            game_running = False
            return game.is_successful()

def handle_game_result(success, task_index, game_type):
    if success:
        task_list.toggle_task(task_index)
        player.energy.decrease(10)
        relationship_graph.increase_relationship("player", "boss", 5)
        reward = calculate_reward(relationship_graph)
        player.checkings.increase(reward)
        print(f"Earned ${reward} from {game_type} task!")
        print("Boss is impressed with your performance!")
    else:
        relationship_graph.decrease_relationship("player", "boss", 10)
        print("Boss is disappointed with your performance!")

# After initializing pygame and before the main game loop
cutscene_screen = CutsceneScreen(screen, game_font)

def handle_coworker_relationship(relationship_graph, player, cutscene_screen):
    coworker_relationship = relationship_graph.get_relationship("player", "coworker")
    
    # Changed threshold from previous value to 50 - coworker gossips when below neutral
    if coworker_relationship < 50 and not coworker.has_triggered_gossip:
        coworker.has_triggered_gossip = True
        
        # Play cutscene
        cutscene_screen.start("gossip")
        waiting_for_cutscene = True
        while waiting_for_cutscene:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if cutscene_screen.update(event):
                    waiting_for_cutscene = False
            cutscene_screen.draw()
            pygame.display.flip()
            clock.tick(FPS)
        
        # Increase salary reduction from 20% to 25% for more impact
        current_balance = player.checkings.get_value()
        salary_reduction = current_balance * 0.25  # 25% salary reduction
        player.checkings.decrease(salary_reduction)
        
        # Show message about salary reduction
        print(f"Your poor relationship with your coworker has affected your reputation.")
        print(f"The boss has decided to reduce your salary by 25%")
    
    return True

def check_boss_relationship(relationship_graph, player, cutscene_screen):
    boss_relationship = relationship_graph.get_relationship("player", "boss")
    
    if boss_relationship < 50:
        scenarios = [
            # Original scenarios
            {
                "message": "Your boss has 'accidentally' thrown a stapler at you.",
                "health_impact": -25
            },
            {
                "message": "Your boss made you work through lunch break, citing 'urgent deadlines'.",
                "health_impact": -20,
                "energy_impact": -15
            },
            {
                "message": "Your boss scheduled all your meetings for 6 AM this week.",
                "health_impact": -15,
                "energy_impact": -20
            },
            {
                "message": "Your boss made you redo all of yesterday's work, claiming it was 'not up to standards'.",
                "health_impact": -10,
                "energy_impact": -25
            },
            {
                "message": "Your boss 'forgot' to turn on the AC in your office during a heatwave.",
                "health_impact": -20,
                "energy_impact": -20
            },
            {
                "message": "Your boss volunteered you for weekend inventory duty without asking.",
                "health_impact": -15,
                "energy_impact": -25
            },
            # New scenarios
            {
                "message": "Your boss 'lost' your vacation request form for the third time.",
                "health_impact": -20,
                "energy_impact": -20
            },
            {
                "message": "Your boss took credit for your project during the company meeting.",
                "health_impact": -25,
                "energy_impact": -15
            },
            {
                "message": "Your boss moved your desk next to the noisy printer room.",
                "health_impact": -20,
                "energy_impact": -20
            },
            {
                "message": "Your boss assigned you to train the new intern while keeping all your deadlines.",
                "health_impact": -15,
                "energy_impact": -25
            },
            {
                "message": "Your boss 'accidentally' spilled hot coffee on your laptop.",
                "health_impact": -25,
                "energy_impact": -15
            },
            {
                "message": "Your boss scheduled your performance review for 7 PM on a Friday.",
                "health_impact": -20,
                "energy_impact": -20
            },
            {
                "message": "Your boss made you present to the board with only 5 minutes notice.",
                "health_impact": -25,
                "energy_impact": -15
            },
            {
                "message": "Your boss blamed you for their missed deadline in front of the whole team.",
                "health_impact": -25,
                "energy_impact": -15
            },
            {
                "message": "Your boss 'reorganized' your filing system while you were at lunch.",
                "health_impact": -15,
                "energy_impact": -25
            },
            {
                "message": "Your boss scheduled mandatory team building on your birthday weekend.",
                "health_impact": -20,
                "energy_impact": -20
            }
        ]
        
        scenario = random.choice(scenarios)
        
        # Play cutscene
        cutscene_screen.start("boss_angry")
        waiting_for_cutscene = True
        while waiting_for_cutscene:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if cutscene_screen.update(event):
                    waiting_for_cutscene = False
            cutscene_screen.draw()
            pygame.display.flip()
        
        # Show scenario message with space to exit
        font = pygame.font.Font(None, 36)
        text_surface = font.render(scenario["message"], True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        
        space_text = font.render("Press SPACE to continue", True, (255, 255, 255))
        space_rect = space_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        
        screen.blit(text_surface, text_rect)
        screen.blit(space_text, space_rect)
        pygame.display.flip()
        
        # Wait for single space press to exit
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    waiting = False
        
        # Apply impacts
        if "health_impact" in scenario:
            player.health.decrease(abs(scenario["health_impact"]))
        if "energy_impact" in scenario:
            player.energy.decrease(abs(scenario["energy_impact"]))
        
        relationship_graph.set_relationship("player", "boss", 51)
    
    return True

while running:
    # Add this check with the other loss conditions at the start of the loop
    if(player.checkings.get_value() <= 0):
        running = False
        end_text = "You ran out of money and had to file for bankruptcy."

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
            for task_index, task in enumerate(tasks):
                if event.key == pygame.K_1 + task_index:
                    # Check if this task can be attempted (is next in sequence)
                    if not task_list.can_attempt_task(task_index):
                        continue  # Skip if not the current task
                        
                    if "Typing" in task:
                        cutscene_screen.start("typing")
                        waiting_for_cutscene = True
                        while waiting_for_cutscene:
                            for cutscene_event in pygame.event.get():
                                if cutscene_event.type == pygame.QUIT:
                                    running = False
                                    waiting_for_cutscene = False
                                if cutscene_screen.update(cutscene_event):
                                    waiting_for_cutscene = False
                            cutscene_screen.draw()
                            clock.tick(FPS)
                        
                        typing_game = TypingGame(screen, game_font)
                        success = run_game(typing_game)
                        handle_game_result(success, task_index, "typing")
                    
                    elif "Email" in task:
                        cutscene_screen.start("email")
                        waiting_for_cutscene = True
                        while waiting_for_cutscene:
                            for cutscene_event in pygame.event.get():
                                if cutscene_event.type == pygame.QUIT:
                                    running = False
                                    waiting_for_cutscene = False
                                if cutscene_screen.update(cutscene_event):
                                    waiting_for_cutscene = False
                            cutscene_screen.draw()
                            clock.tick(FPS)
                        
                        email_game = EmailGame(screen, game_font)
                        success = run_game(email_game)
                        handle_game_result(success, task_index, "email")
                    
                    elif "Coffee" in task:
                        cutscene_screen.start("coffee")
                        waiting_for_cutscene = True
                        while waiting_for_cutscene:
                            for cutscene_event in pygame.event.get():
                                if cutscene_event.type == pygame.QUIT:
                                    running = False
                                    waiting_for_cutscene = False
                                if cutscene_screen.update(cutscene_event):
                                    waiting_for_cutscene = False
                            cutscene_screen.draw()
                            clock.tick(FPS)
                        
                        coffee_game = CoffeeGame(screen, game_font)
                        success = run_game(coffee_game)
                        handle_game_result(success, task_index, "coffee")
                    
                    elif "Burger" in task:
                        cutscene_screen.start("sandwich")
                        waiting_for_cutscene = True
                        while waiting_for_cutscene:
                            for cutscene_event in pygame.event.get():
                                if cutscene_event.type == pygame.QUIT:
                                    running = False
                                    waiting_for_cutscene = False
                                if cutscene_screen.update(cutscene_event):
                                    waiting_for_cutscene = False
                            cutscene_screen.draw()
                            clock.tick(FPS)
                        
                        sandwich_game = SandwichGame(screen, game_font)
                        success = run_game(sandwich_game)
                        handle_game_result(success, task_index, "sandwich")

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
        # Update tasks for the new day
        tasks = get_daily_tasks(current_day)
        task_list = TaskList(tasks, game_font, x=10, y=10, color=(255, 255, 255))
        boss.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)
        coworker.rect.center = (SCREEN_WIDTH // 3, SCREEN_HEIGHT // 2)

    elif (current_screen == 2 and player.rect.left <= 0):
        # Remove task completion check and proceed directly with transition
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
        
        # Decrease coworker relationship at end of each day
        current_relationship = relationship_graph.get_relationship("player", "coworker")
        relationship_graph.decrease_relationship("player", "coworker", 5)  # Lose 5 points per day
        print(f"Your coworker feels neglected. Relationship decreased to {relationship_graph.get_relationship('player', 'coworker')}")
        
        current_screen = 1
        player.rect.right = SCREEN_WIDTH - 10
        current_day += 1

    # Fill the screen with a color
    if (current_screen == 1):
        background_image = pygame.image.load('./assets/HomeScreen.png')
        background_image = pygame.transform.scale(background_image, (1280, 720))
        screen.blit(background_image, (0,0))
    elif (current_screen == 2):
        screen.blit(office_background, (0,0))
        task_list.draw(screen)  # Move task list to work screen
        # Update and draw NPCs in office
        npc_group.update(SCREEN_WIDTH, SCREEN_HEIGHT)
        npc_group.draw(screen)

        for npc in npc_group:
            npc.draw_minibar(screen, relationship_graph, npc.name.lower())
            npc.draw_name(screen)  # Draw name

        # Update NPCs with player position
        for npc in npc_group:
            npc.update(SCREEN_WIDTH, SCREEN_HEIGHT, player.rect)
            
            # Check for interaction
            if npc.is_near_player(player.rect):
                npc.draw_interaction_prompt(screen, game_font)
                
                if keys_pressed[pygame.K_RETURN]:
                    dialogue = npc.interact(relationship_graph)
                    if dialogue:  # Only show if interaction cooldown has passed
                        waiting_for_choice = True
                        show_result = None
                        result_timer = 0
                        
                        while waiting_for_choice:
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    running = False
                                    waiting_for_choice = False
                                elif event.type == pygame.KEYDOWN:
                                    if event.key in [pygame.K_1, pygame.K_2]:
                                        choice_idx = 0 if event.key == pygame.K_1 else 1
                                        effect = dialogue['options'][choice_idx]['effect']
                                        
                                        # Determine if it was a good choice
                                        show_result = effect > 0
                                        
                                        if effect > 0:
                                            relationship_graph.increase_relationship("player", npc.name.lower(), abs(effect))
                                        else:
                                            relationship_graph.decrease_relationship("player", npc.name.lower(), abs(effect))
                                        
                                        result_timer = pygame.time.get_ticks()
                                        
                            # Draw the game state
                            screen.fill((30, 30, 30))
                            
                            # Draw background elements
                            if current_screen == 1:
                                background_image = pygame.image.load('./assets/HomeScreen.png')
                                background_image = pygame.transform.scale(background_image, (1280, 720))
                                screen.blit(background_image, (0,0))
                            elif current_screen == 2:
                                screen.blit(office_background, (0,0))
                            
                            # Draw sprites
                            player_group.draw(screen)
                            npc_group.draw(screen)
                            
                            # Draw dialogue box with result if available
                            npc.draw_dialogue_box(screen, game_font, dialogue, show_result)
                            
                            pygame.display.flip()
                            
                            # If showing result, wait 2 seconds then close
                            if show_result is not None:
                                if pygame.time.get_ticks() - result_timer > 2000:  # 2 seconds
                                    waiting_for_choice = False
                            
                            clock.tick(FPS)

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

    if current_screen == 2:  # Only check during office screen
        if not handle_coworker_relationship(relationship_graph, player, cutscene_screen):
            running = False  # Only end if there's a quit event
        if not check_boss_relationship(relationship_graph, player, cutscene_screen):
            running = False

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

