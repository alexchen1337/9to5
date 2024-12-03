import pygame
import random

class NPC(pygame.sprite.Sprite):
    def __init__(self, sprite_path, scale_factor, screen_width, screen_height, name, job_title):
        super().__init__()
        self.image = pygame.image.load(sprite_path)
        self.image = pygame.transform.scale(self.image, (self.image.get_width() * scale_factor, self.image.get_height() * scale_factor))
        self.rect = self.image.get_rect()

        # Set the NPC's starting position to a random location within the screen
        self.rect.x = random.randint(0, screen_width - self.rect.width)
        self.rect.y = random.randint(0, screen_height - self.rect.height)
        
        self.name = name
        self.job_title = job_title
        self.mood = random.choice(['happy', 'neutral', 'unhappy'])
        
        # Movement variables
        self.speed = 2
        self.direction = pygame.math.Vector2()
        self.change_direction_timer = 0
        self.change_direction_interval = 60  # frames until direction change

        # Pause variables
        self.is_paused = False
        self.pause_timer = 0
        self.pause_duration = 0
        self.move_timer = 0
        self.move_interval = 10000  # 10 seconds in milliseconds

        # Add interaction radius and cooldown
        self.interaction_radius = 100
        self.interaction_cooldown = 2000
        self.last_interaction = 0
        
        # Add default dialogues based on NPC type
        if name == "Boss":
            self.dialogues = [
                {
                    "text": "How's that report coming along?",
                    "options": [
                        {"text": "Almost done!", "effect": 5},
                        {"text": "What report?", "effect": -5}
                    ]
                },
                # Add more boss-specific dialogues...
            ]
        elif name == "Coworker":
            self.dialogues = [
                {
                    "text": "Did you hear about the new policy?",
                    "options": [
                        {"text": "Tell me more!", "effect": 5},
                        {"text": "Not interested.", "effect": -5}
                    ]
                },
                # Add more coworker-specific dialogues...
            ]
        elif name == "Wife":
            self.dialogues = [
                {
                    "text": "How was work today?",
                    "options": [
                        {"text": "Let me tell you all about it!", "effect": 5},
                        {"text": "I don't want to talk about it.", "effect": -5}
                    ]
                },
                {
                    "text": "Do you remember our anniversary?",
                    "options": [
                        {"text": "Of course, I have something special planned!", "effect": 10},
                        {"text": "Oh no, I forgot...", "effect": -10}
                    ]
                },
                {
                    "text": "Can we spend some time together this weekend?",
                    "options": [
                        {"text": "Absolutely, let's plan something fun!", "effect": 5},
                        {"text": "I'm too busy this weekend.", "effect": -5}
                    ]
                },
                {
                    "text": "I made your favorite dinner tonight.",
                    "options": [
                        {"text": "Thank you, I can't wait to eat!", "effect": 5},
                        {"text": "I'm not hungry right now.", "effect": -5}
                    ]
                },
                {
                    "text": "I was thinking about redecorating the living room.",
                    "options": [
                        {"text": "Great idea, let's do it together!", "effect": 5},
                        {"text": "I like it the way it is.", "effect": -5}
                    ]
                },
                {
                    "text": "I found a new hobby I want to try.",
                    "options": [
                        {"text": "That sounds exciting, tell me more!", "effect": 5},
                        {"text": "Do we have time for that?", "effect": -5}
                    ]
                },
                {
                    "text": "I feel like we haven't talked much lately.",
                    "options": [
                        {"text": "Let's sit down and catch up.", "effect": 5},
                        {"text": "I've been really busy.", "effect": -5}
                    ]
                },
                {
                    "text": "I saw a movie that I think you'd love.",
                    "options": [
                        {"text": "Let's watch it together!", "effect": 5},
                        {"text": "I'm not interested in movies.", "effect": -5}
                    ]
                },
                {
                    "text": "I need your help with something.",
                    "options": [
                        {"text": "Sure, what do you need?", "effect": 5},
                        {"text": "Can it wait?", "effect": -5}
                    ]
                },
                {
                    "text": "I was thinking about taking a vacation.",
                    "options": [
                        {"text": "That sounds wonderful, let's plan it!", "effect": 5},
                        {"text": "We can't afford that right now.", "effect": -5}
                    ]
                },
                {
                    "text": "I love spending time with you.",
                    "options": [
                        {"text": "I love it too!", "effect": 5},
                        {"text": "I need some space.", "effect": -5}
                    ]
                },
                {
                    "text": "I have a surprise for you.",
                    "options": [
                        {"text": "I can't wait to see it!", "effect": 5},
                        {"text": "I'm not in the mood for surprises.", "effect": -5}
                    ]
                },
                {
                    "text": "I think we should talk about our future.",
                    "options": [
                        {"text": "Yes, let's discuss it.", "effect": 5},
                        {"text": "I'm not ready for that conversation.", "effect": -5}
                    ]
                },
                {
                    "text": "I feel like we need a date night.",
                    "options": [
                        {"text": "Let's plan one soon!", "effect": 5},
                        {"text": "I'm too tired for that.", "effect": -5}
                    ]
                },
                {
                    "text": "I appreciate everything you do for us.",
                    "options": [
                        {"text": "Thank you, that means a lot.", "effect": 5},
                        {"text": "I don't need your appreciation.", "effect": -5}
                    ]
                },
                {
                    "text": "I want to try cooking a new recipe.",
                    "options": [
                        {"text": "Let's do it together!", "effect": 5},
                        {"text": "I'm not interested in cooking.", "effect": -5}
                    ]
                },
                {
                    "text": "I think we should start a new project together.",
                    "options": [
                        {"text": "That sounds like a great idea!", "effect": 5},
                        {"text": "I don't have time for that.", "effect": -5}
                    ]
                },
                {
                    "text": "I feel like we need to reconnect.",
                    "options": [
                        {"text": "I agree, let's work on it.", "effect": 5},
                        {"text": "I think we're fine.", "effect": -5}
                    ]
                },
                {
                    "text": "I want to hear about your day.",
                    "options": [
                        {"text": "I'd love to share it with you.", "effect": 5},
                        {"text": "It's not worth talking about.", "effect": -5}
                    ]
                },
                {
                    "text": "I think we should have a family meeting.",
                    "options": [
                        {"text": "That's a good idea.", "effect": 5},
                        {"text": "I don't see the point.", "effect": -5}
                    ]
                }
            ]

        # Add new variables for relationship monitoring
        self.gossip_threshold = 30  # Relationship must be above this or triggers negative event
        self.has_triggered_gossip = False  # Ensures the event only happens once
        self.has_triggered_argument = False  # For wife

    def is_near_player(self, player_rect):
        distance = pygame.math.Vector2(
            self.rect.centerx - player_rect.centerx,
            self.rect.centery - player_rect.centery
        ).length()
        return distance <= self.interaction_radius

    def interact(self, relationship_graph):
        # Add check for empty dialogues
        if not hasattr(self, 'dialogues') or not self.dialogues:
            # Return a default dialogue if none exists
            return {
                "text": f"Hello! I'm {self.name}.",
                "options": [
                    {"text": "Nice to meet you!", "effect": 5},
                    {"text": "Whatever...", "effect": -5}
                ]
            }
        
        current_time = pygame.time.get_ticks()
        if current_time - self.last_interaction < self.interaction_cooldown:
            return None

        # Select a random dialogue
        dialogue = random.choice(self.dialogues)
        self.last_interaction = current_time
        return dialogue

    def update(self, screen_width, screen_height, player_rect=None):
        # Store previous position
        previous_pos = self.rect.copy()
        
        if player_rect and self.is_near_player(player_rect):
            # Stop moving when player is near
            return

        current_time = pygame.time.get_ticks()

        # Check if it's time to pause
        if not self.is_paused and current_time - self.move_timer > self.move_interval:
            self.is_paused = True
            self.pause_duration = random.randint(1000, 3000)  # Pause for 1-3 seconds
            self.pause_timer = current_time

        # If paused, check if pause duration is over
        if self.is_paused:
            if current_time - self.pause_timer > self.pause_duration:
                self.is_paused = False
                self.move_timer = current_time  # Reset move timer
            else:
                return  # Skip movement update if paused

        # Update direction timer
        self.change_direction_timer += 1
        if self.change_direction_timer >= self.change_direction_interval:
            # Choose new random direction
            self.direction.x = random.uniform(-1, 1)
            self.direction.y = random.uniform(-1, 1)
            self.direction = self.direction.normalize()
            self.change_direction_timer = 0
            self.change_direction_interval = random.randint(30, 90)  # Random interval

        # Move NPC
        self.rect.x += self.direction.x * self.speed
        self.rect.y += self.direction.y * self.speed

        # Add boundary checks including top 300 pixels restriction
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > screen_width:
            self.rect.right = screen_width
        if self.rect.top < 200:  # Prevent moving into top 200 pixels
            self.rect.top = 200
        if self.rect.bottom > screen_height:
            self.rect.bottom = screen_height

    def chat(self):
        chat_responses = {
            'happy': f"{self.name}: I'm having a great day!",
            'neutral': f"{self.name}: Just another day at the office.",
            'unhappy': f"{self.name}: Don't speak to me."
        }
        print(chat_responses[self.mood])

    def change_mood(self, new_mood):
        if new_mood in ['happy', 'neutral', 'unhappy']:
            self.mood = new_mood
        else:
            print("Invalid mood!")

    def __str__(self):
        return f"{self.name} - {self.job_title}, Mood: {self.mood}"

    def draw_minibar(self, screen, relationship_graph, target):
        # Get the relationship weight for this NPC
        weight = relationship_graph.get_relationship("player", target)

        # Determine the color based on the weight
        if weight > 60:
            color = (0, 255, 0)  # Green
        elif 30 <= weight <= 60:
            color = (255, 255, 0)  # Yellow
        else:
            color = (255, 0, 0)  # Red

        # Calculate the position and size of the minibar
        bar_width = 50
        bar_height = 5
        bar_x = self.rect.centerx - bar_width // 2
        bar_y = self.rect.bottom + 5  # Place it below the NPC

        # Background of the bar
        pygame.draw.rect(screen, (100, 100, 100), (bar_x, bar_y, bar_width, bar_height))

        # Filled portion of the bar
        filled_width = int((weight / 100) * bar_width)
        pygame.draw.rect(screen, color, (bar_x, bar_y, filled_width, bar_height))
    
    def draw_name(self, screen):
        # Define the font for the NPC's name
        font = pygame.font.Font(None, 24)  # Default font, size 24
        text_surface = font.render(self.name, True, (255, 255, 255))  # White color

        # Position the name just above the NPC
        text_rect = text_surface.get_rect(midbottom=(self.rect.centerx, self.rect.top - 5))
        screen.blit(text_surface, text_rect)

    def draw_interaction_prompt(self, screen, font):
        text = font.render("Press ENTER to interact", True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.rect.centerx, self.rect.top - 20))
        screen.blit(text, text_rect)

    def draw_dialogue_box(self, screen, font, dialogue, show_result=None):
        # Set up dialogue box dimensions and colors
        box_width = 800
        box_height = 200
        box_x = (screen.get_width() - box_width) // 2
        box_y = screen.get_height() - box_height - 20
        
        # Draw semi-transparent background
        dialogue_surface = pygame.Surface((box_width, box_height))
        dialogue_surface.fill((0, 0, 0))
        dialogue_surface.set_alpha(200)
        screen.blit(dialogue_surface, (box_x, box_y))
        
        # Draw border
        pygame.draw.rect(screen, (255, 255, 255), (box_x, box_y, box_width, box_height), 2)
        
        # Render dialogue text
        text_color = (255, 255, 255)
        # Use 'text' key for wife dialogue and 'prompt' for others
        dialogue_text = dialogue.get('text', dialogue.get('prompt'))
        prompt_text = font.render(dialogue_text, True, text_color)
        screen.blit(prompt_text, (box_x + 20, box_y + 20))
        
        # If showing result
        if show_result is not None:
            result_text = "Good choice!" if show_result else "Bad choice..."
            result_color = (0, 255, 0) if show_result else (255, 0, 0)
            result_surface = font.render(result_text, True, result_color)
            result_rect = result_surface.get_rect(center=(box_x + box_width//2, box_y + box_height//2))
            screen.blit(result_surface, result_rect)
        else:
            # Draw options
            y_offset = 80
            for i, option in enumerate(dialogue['options']):
                option_text = f"{i+1}. {option['text']}"
                option_surface = font.render(option_text, True, text_color)
                screen.blit(option_surface, (box_x + 20, box_y + y_offset))
                y_offset += 40