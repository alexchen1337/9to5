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
        
        # Add dialogue options based on NPC type
        self.dialogues = self.get_dialogues(name)

        # Add new variables for relationship monitoring
        self.gossip_threshold = 30  # Relationship must be above this or triggers negative event
        self.has_triggered_gossip = False  # Ensures the event only happens once
        self.has_triggered_argument = False  # For wife

    def get_dialogues(self, name):
        if name == "Boss":
            return [
                {
                    "prompt": "What's your approach to meeting deadlines?",
                    "options": [
                        {"text": "Quality over speed", "effect": -5},
                        {"text": "Meet deadlines at all costs", "effect": 5}
                    ]
                },
                {
                    "prompt": "How do you handle workplace conflicts?",
                    "options": [
                        {"text": "Address them immediately", "effect": 5},
                        {"text": "Let people work it out themselves", "effect": -5}
                    ]
                },
                {
                    "prompt": "What's your view on innovation?",
                    "options": [
                        {"text": "Stick to proven methods", "effect": 5},
                        {"text": "Always try new approaches", "effect": -5}
                    ]
                },
                {
                    "prompt": "How do you handle criticism?",
                    "options": [
                        {"text": "Defend your position", "effect": -5},
                        {"text": "Accept and reflect", "effect": 5}
                    ]
                },
                {
                    "prompt": "What's your stance on overtime?",
                    "options": [
                        {"text": "It shows dedication", "effect": 5},
                        {"text": "Efficiency within hours", "effect": -5}
                    ]
                },
                {
                    "prompt": "How do you view workplace competition?",
                    "options": [
                        {"text": "It drives improvement", "effect": -5},
                        {"text": "Collaboration is key", "effect": 5}
                    ]
                },
                {
                    "prompt": "What's your take on office politics?",
                    "options": [
                        {"text": "Navigate them carefully", "effect": 5},
                        {"text": "Stay completely neutral", "effect": -5}
                    ]
                },
                {
                    "prompt": "How do you handle project setbacks?",
                    "options": [
                        {"text": "Find someone accountable", "effect": -5},
                        {"text": "Focus on solutions", "effect": 5}
                    ]
                },
                {
                    "prompt": "What's your view on company traditions?",
                    "options": [
                        {"text": "Preserve them", "effect": 5},
                        {"text": "Update with times", "effect": -5}
                    ]
                },
                {
                    "prompt": "How do you approach risk-taking?",
                    "options": [
                        {"text": "Calculated risks only", "effect": 5},
                        {"text": "Bold moves win big", "effect": -5}
                    ]
                },
                {
                    "prompt": "What's your stance on remote work?",
                    "options": [
                        {"text": "Office presence matters", "effect": 5},
                        {"text": "Results over location", "effect": -5}
                    ]
                },
                {
                    "prompt": "How do you view workplace hierarchy?",
                    "options": [
                        {"text": "Essential for order", "effect": 5},
                        {"text": "Flat structure works better", "effect": -5}
                    ]
                },
                {
                    "prompt": "What's your approach to team building?",
                    "options": [
                        {"text": "Formal activities", "effect": -5},
                        {"text": "Natural connections", "effect": 5}
                    ]
                },
                {
                    "prompt": "How do you handle disagreements?",
                    "options": [
                        {"text": "Stand your ground", "effect": -5},
                        {"text": "Find middle ground", "effect": 5}
                    ]
                },
                {
                    "prompt": "What's your view on workplace changes?",
                    "options": [
                        {"text": "Gradual implementation", "effect": 5},
                        {"text": "Quick adaptation", "effect": -5}
                    ]
                },
                {
                    "prompt": "How do you approach deadlines?",
                    "options": [
                        {"text": "Extensions if needed", "effect": -5},
                        {"text": "Meet them no matter what", "effect": 5}
                    ]
                },
                {
                    "prompt": "What's your take on workplace feedback?",
                    "options": [
                        {"text": "Direct and honest", "effect": 5},
                        {"text": "Gentle and supportive", "effect": -5}
                    ]
                },
                {
                    "prompt": "How do you view work-life balance?",
                    "options": [
                        {"text": "Work comes first", "effect": 5},
                        {"text": "Personal life priority", "effect": -5}
                    ]
                },
                {
                    "prompt": "What's your approach to meetings?",
                    "options": [
                        {"text": "Quick and focused", "effect": -5},
                        {"text": "Thorough discussion", "effect": 5}
                    ]
                },
                {
                    "prompt": "How do you handle stress?",
                    "options": [
                        {"text": "Push through it", "effect": 5},
                        {"text": "Take breaks", "effect": -5}
                    ]
                },
                {
                    "prompt": "What's your view on workplace diversity?",
                    "options": [
                        {"text": "Merit-based only", "effect": -5},
                        {"text": "Active inclusion", "effect": 5}
                    ]
                },
                {
                    "prompt": "How do you approach innovation?",
                    "options": [
                        {"text": "Careful planning", "effect": 5},
                        {"text": "Quick experimentation", "effect": -5}
                    ]
                },
                {
                    "prompt": "What's your take on workplace rules?",
                    "options": [
                        {"text": "Strictly follow them", "effect": 5},
                        {"text": "Flexible interpretation", "effect": -5}
                    ]
                },
                {
                    "prompt": "How do you view success?",
                    "options": [
                        {"text": "Individual achievement", "effect": -5},
                        {"text": "Team accomplishment", "effect": 5}
                    ]
                },
                {
                    "prompt": "What's your approach to problems?",
                    "options": [
                        {"text": "Methodical analysis", "effect": 5},
                        {"text": "Quick solutions", "effect": -5}
                    ]
                }
            ]
        elif name == "Wife":
            return random.choice([
                {
                    "text": "I miss having dinner together like we used to...",
                    "options": [
                        {"text": "I miss that too. Let's plan a special dinner this weekend.", "effect": 10},
                        {"text": "Sorry, I've been really busy with work lately.", "effect": -5}
                    ]
                },
                {
                    "text": "Do you even remember our anniversary date?",
                    "options": [
                        {"text": "Of course! It's next month, right?", "effect": -15},
                        {"text": "The 15th of June, the happiest day of my life.", "effect": 10}
                    ]
                },
                {
                    "text": "Your coworker seems to make you laugh more than I do these days...",
                    "options": [
                        {"text": "Don't be ridiculous, it's just work friendship.", "effect": -10},
                        {"text": "You're right, I should be more mindful of boundaries.", "effect": 15}
                    ]
                },
                {
                    "text": "Maybe we could take a vacation together soon?",
                    "options": [
                        {"text": "I can't take time off work right now.", "effect": -10},
                        {"text": "That's a wonderful idea! Let's start planning.", "effect": 15}
                    ]
                },
                {
                    "text": "I made your favorite dinner tonight...",
                    "options": [
                        {"text": "I'll have to work late again, sorry.", "effect": -15},
                        {"text": "I'll be home in time, I promise!", "effect": 10}
                    ]
                },
                {
                    "text": "Remember when we used to go on weekend adventures?",
                    "options": [
                        {"text": "Those were fun times! Let's do something this weekend.", "effect": 15},
                        {"text": "We're not young anymore, things change.", "effect": -10}
                    ]
                },
                {
                    "text": "I saw you got a raise at work. When were you going to tell me?",
                    "options": [
                        {"text": "I was waiting for the right moment to surprise you.", "effect": 10},
                        {"text": "It's not a big deal, just work stuff.", "effect": -15}
                    ]
                },
                {
                    "text": "Your mother called. She misses us...",
                    "options": [
                        {"text": "Let's invite her over for dinner soon.", "effect": 15},
                        {"text": "Tell her I'm too busy right now.", "effect": -10}
                    ]
                },
                {
                    "text": "I feel like we're growing apart...",
                    "options": [
                        {"text": "That's just how marriage works sometimes.", "effect": -20},
                        {"text": "Let's work on this together. I love you.", "effect": 15}
                    ]
                },
                {
                    "text": "Can we talk about our future plans?",
                    "options": [
                        {"text": "Not now, I'm tired from work.", "effect": -15},
                        {"text": "Of course, our future together is important to me.", "effect": 10}
                    ]
                },
                {
                    "text": "I bought us concert tickets for next weekend...",
                    "options": [
                        {"text": "Perfect! It'll be like our first date.", "effect": 15},
                        {"text": "I might have to work that day.", "effect": -10}
                    ]
                },
                {
                    "text": "Do you still find time for us between all your work?",
                    "options": [
                        {"text": "I'm doing this all for us.", "effect": -5},
                        {"text": "You're right, I need to make more time for you.", "effect": 15}
                    ]
                },
                {
                    "text": "I saw you texting late last night. Was it work again?",
                    "options": [
                        {"text": "Yes, just finishing up some projects.", "effect": -10},
                        {"text": "I should've put the phone away and spent time with you.", "effect": 15}
                    ]
                },
                {
                    "text": "Remember our dream of traveling the world together?",
                    "options": [
                        {"text": "We should start planning our first trip!", "effect": 15},
                        {"text": "Dreams change as we get older.", "effect": -10}
                    ]
                },
                {
                    "text": "I cleaned your office space at home...",
                    "options": [
                        {"text": "You shouldn't have touched my things.", "effect": -15},
                        {"text": "Thank you, that was very thoughtful.", "effect": 10}
                    ]
                },
                {
                    "text": "Can we have breakfast together tomorrow?",
                    "options": [
                        {"text": "I have an early meeting.", "effect": -10},
                        {"text": "I'll make time. I miss our morning talks.", "effect": 15}
                    ]
                },
                {
                    "text": "Your friends say they hardly see you anymore...",
                    "options": [
                        {"text": "Let's host a dinner party this weekend!", "effect": 15},
                        {"text": "They should understand I'm busy.", "effect": -10}
                    ]
                },
                {
                    "text": "I got a promotion at my job today!",
                    "options": [
                        {"text": "That's nice, dear.", "effect": -15},
                        {"text": "I'm so proud of you! Let's celebrate!", "effect": 20}
                    ]
                },
                {
                    "text": "Do you remember why you fell in love with me?",
                    "options": [
                        {"text": "Of course, your smile still brightens my day.", "effect": 15},
                        {"text": "That was a long time ago...", "effect": -20}
                    ]
                },
                {
                    "text": "I've been thinking about taking dance classes...",
                    "options": [
                        {"text": "That sounds like a waste of time.", "effect": -15},
                        {"text": "We should take them together!", "effect": 15}
                    ]
                },
                {
                    "text": "Your dad's retirement party is next month...",
                    "options": [
                        {"text": "I'll definitely be there, family is important.", "effect": 15},
                        {"text": "I'll try to make it if work allows.", "effect": -10}
                    ]
                },
                {
                    "text": "Remember our first apartment together?",
                    "options": [
                        {"text": "Yeah, it was tiny but perfect.", "effect": 15},
                        {"text": "Glad we upgraded from that place.", "effect": -5}
                    ]
                },
                {
                    "text": "I made plans for us this weekend...",
                    "options": [
                        {"text": "You should have checked with me first.", "effect": -15},
                        {"text": "I can't wait to see what you planned!", "effect": 10}
                    ]
                },
                {
                    "text": "Do you think we've changed since we got married?",
                    "options": [
                        {"text": "Yes, we've grown stronger together.", "effect": 15},
                        {"text": "Everyone changes, that's life.", "effect": -10}
                    ]
                },
                {
                    "text": "I miss the little notes you used to leave me...",
                    "options": [
                        {"text": "Those were silly anyway.", "effect": -15},
                        {"text": "I'll start doing that again, just for you.", "effect": 15}
                    ]
                }
            ])
        else:  # Coworker
            return [
                {
                    "prompt": "How do you feel about office gossip?",
                    "options": [
                        {"text": "It builds connections", "effect": -5},
                        {"text": "Keep things professional", "effect": 5}
                    ]
                },
                {
                    "prompt": "What's your lunch break style?",
                    "options": [
                        {"text": "Quick and efficient", "effect": -5},
                        {"text": "Social and relaxed", "effect": 5}
                    ]
                },
                {
                    "prompt": "How do you handle tight deadlines?",
                    "options": [
                        {"text": "Ask for help", "effect": 5},
                        {"text": "Handle it alone", "effect": -5}
                    ]
                },
                {
                    "prompt": "What's your view on office celebrations?",
                    "options": [
                        {"text": "Keep them minimal", "effect": -5},
                        {"text": "They boost morale", "effect": 5}
                    ]
                },
                {
                    "prompt": "How do you approach collaboration?",
                    "options": [
                        {"text": "Independent work", "effect": -5},
                        {"text": "Team effort", "effect": 5}
                    ]
                },
                {
                    "prompt": "What's your take on office friendships?",
                    "options": [
                        {"text": "Keep it professional", "effect": -5},
                        {"text": "Build relationships", "effect": 5}
                    ]
                },
                {
                    "prompt": "How do you handle workplace stress?",
                    "options": [
                        {"text": "Share with colleagues", "effect": 5},
                        {"text": "Keep it to yourself", "effect": -5}
                    ]
                },
                {
                    "prompt": "What's your view on office competition?",
                    "options": [
                        {"text": "Healthy motivation", "effect": 5},
                        {"text": "Unnecessary pressure", "effect": -5}
                    ]
                },
                {
                    "prompt": "How do you approach new projects?",
                    "options": [
                        {"text": "Dive right in", "effect": -5},
                        {"text": "Plan thoroughly", "effect": 5}
                    ]
                },
                {
                    "prompt": "What's your take on office hours?",
                    "options": [
                        {"text": "Strict schedule", "effect": -5},
                        {"text": "Flexible timing", "effect": 5}
                    ]
                },
                {
                    "prompt": "How do you handle mistakes?",
                    "options": [
                        {"text": "Learn and move on", "effect": 5},
                        {"text": "Analyze extensively", "effect": -5}
                    ]
                },
                {
                    "prompt": "What's your view on workplace changes?",
                    "options": [
                        {"text": "Embrace them", "effect": 5},
                        {"text": "Prefer stability", "effect": -5}
                    ]
                },
                {
                    "prompt": "How do you approach feedback?",
                    "options": [
                        {"text": "Welcome it openly", "effect": 5},
                        {"text": "Prefer autonomy", "effect": -5}
                    ]
                },
                {
                    "prompt": "What's your lunch preference?",
                    "options": [
                        {"text": "Eat at desk", "effect": -5},
                        {"text": "Social lunch", "effect": 5}
                    ]
                },
                {
                    "prompt": "How do you view workplace communication?",
                    "options": [
                        {"text": "Formal channels", "effect": -5},
                        {"text": "Open dialogue", "effect": 5}
                    ]
                },
                {
                    "prompt": "What's your approach to meetings?",
                    "options": [
                        {"text": "Active participation", "effect": 5},
                        {"text": "Listen quietly", "effect": -5}
                    ]
                },
                {
                    "prompt": "How do you handle conflicts?",
                    "options": [
                        {"text": "Direct discussion", "effect": 5},
                        {"text": "Avoid confrontation", "effect": -5}
                    ]
                },
                {
                    "prompt": "What's your view on office events?",
                    "options": [
                        {"text": "Network opportunity", "effect": 5},
                        {"text": "Optional social time", "effect": -5}
                    ]
                },
                {
                    "prompt": "How do you approach deadlines?",
                    "options": [
                        {"text": "Last minute rush", "effect": -5},
                        {"text": "Steady progress", "effect": 5}
                    ]
                },
                {
                    "prompt": "What's your take on workplace dress code?",
                    "options": [
                        {"text": "Express personality", "effect": 5},
                        {"text": "Strict professional", "effect": -5}
                    ]
                },
                {
                    "prompt": "How do you view team success?",
                    "options": [
                        {"text": "Individual effort", "effect": -5},
                        {"text": "Group achievement", "effect": 5}
                    ]
                },
                {
                    "prompt": "What's your approach to learning?",
                    "options": [
                        {"text": "Self-directed", "effect": -5},
                        {"text": "Learn from others", "effect": 5}
                    ]
                },
                {
                    "prompt": "How do you handle busy periods?",
                    "options": [
                        {"text": "Focus alone", "effect": -5},
                        {"text": "Collaborate more", "effect": 5}
                    ]
                },
                {
                    "prompt": "What's your view on workplace recognition?",
                    "options": [
                        {"text": "Public praise", "effect": 5},
                        {"text": "Private acknowledgment", "effect": -5}
                    ]
                },
                {
                    "prompt": "How do you approach problems?",
                    "options": [
                        {"text": "Solve independently", "effect": -5},
                        {"text": "Seek input", "effect": 5}
                    ]
                }
            ]

    def is_near_player(self, player_rect):
        distance = pygame.math.Vector2(
            self.rect.centerx - player_rect.centerx,
            self.rect.centery - player_rect.centery
        ).length()
        return distance <= self.interaction_radius

    def interact(self, relationship_graph):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_interaction < self.interaction_cooldown:
            return None

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
        prompt_text = font.render(dialogue['prompt'], True, text_color)
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