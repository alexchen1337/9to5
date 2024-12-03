import pygame
import time

class CutsceneScreen:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.start_time = None
        self.display_time = 5  # How long to show each cutscene (in seconds)
        
        # Dictionary of cutscene texts for each game
        self.cutscenes = {
            "typing": [
                "TYPING TEST",
                "",
                "The boss needs you to prove your typing skills!",
                "Type the words as they appear on screen.",
                "You have 40 seconds to type as many words as you can.",
                "Make too many mistakes or run out of time, and you'll fail.",
                "",
                "Press SPACE to begin..."
            ],
            
            "email": [
                "EMAIL MANAGEMENT",
                "",
                "Time to clean up the company inbox!",
                "For each email, choose the correct action:",
                "REPLY (1) - Respond to important messages",
                "FORWARD (2) - Pass along to relevant departments",
                "DELETE (3) - Remove spam and unnecessary emails",
                "",
                "You have 30 seconds to handle 10 emails correctly.",
                "6 mistakes and you're out!",
                "",
                "Press SPACE to begin..."
            ],
            
            "coffee": [
                "COFFEE RUN",
                "",
                "The office needs their caffeine fix!",
                "Follow the recipe exactly as shown.",
                "Add ingredients in the correct order:",
                "Press 1-4 for different ingredients",
                "Make sure you don't mess up anyone's order!",
                "",
                "Press SPACE to begin..."
            ],
            
            "sandwich": [
                "LUNCH ORDERS",
                "",
                "Everyone's hungry - time to make sandwiches!",
                "Follow each order carefully:",
                "Add ingredients in the exact order shown",
                "Press 1-4 for different ingredients",
                "Don't mix up the orders or you'll have to start over!",
                "",
                "Press SPACE to begin..."
            ],
            
            "gossip": [
                "Your coworker has been spreading negative rumors about you...",
                "The boss overheard some concerning things about your work ethic...",
                "This has affected your standing in the company...",
                "Your salary has been reduced by 20%"
            ],
            
            "boss_angry": [
                "Your boss seems particularly upset today...",
                "You can feel the tension in the air...",
                "Something bad is about to happen..."
            ],
            "wife_argument": [
                "Your wife is upset about your work-life balance...",
                "She feels like you're never home anymore...",
                "Maybe you should try to spend more time with her?"
            ],
            "wife_catches_flirting": [
                "Your wife has walked in to the office...",
                "She caught you flirting with your co-worker!",
                "She's furious and storms out of the office.",
                "You better fix this quickly!"
            ]
        }
        
    def start(self, cutscene_type):
        self.current_game = cutscene_type
        self.start_time = time.time()
        self.waiting_for_input = True
        
    def update(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.waiting_for_input = False
            return True
        return False
            
    def draw(self):
        self.screen.fill((30, 30, 30))  # Dark background
        
        # Draw the cutscene text
        y_offset = 100
        for line in self.cutscenes[self.current_game]:
            if line == self.cutscenes[self.current_game][0]:  # Title line
                text_surface = self.font.render(line, True, (255, 255, 0))  # Yellow for title
                text_rect = text_surface.get_rect(center=(self.screen.get_width() // 2, y_offset))
            else:
                text_surface = self.font.render(line, True, (255, 255, 255))  # White for other text
                text_rect = text_surface.get_rect(center=(self.screen.get_width() // 2, y_offset))
            
            self.screen.blit(text_surface, text_rect)
            y_offset += 40
            
        pygame.display.flip() 