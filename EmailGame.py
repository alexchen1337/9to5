import pygame
import random

# Initialize Pygame
pygame.init()

# Define Colors
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
DARK_GRAY = (50, 50, 50)

# Meter class
class Meter:
    def __init__(self, name, max_value):
        self.name = name
        self.value = max_value
        self.max_value = max_value

    def decrease(self, amount):
        self.value = max(0, self.value - amount)

    def draw(self, screen, pos):
        bar_width = 200
        bar_height = 30
        fill_ratio = self.value / self.max_value
        fill_color = RED if self.name == "Boss Happiness" else BLUE
        pygame.draw.rect(screen, GRAY, (pos[0], pos[1], bar_width, bar_height))
        pygame.draw.rect(screen, fill_color, (pos[0], pos[1], bar_width * fill_ratio, bar_height))

class EmailGame:
    def __init__(self, screen, boss_happiness_meter, salary_meter, font):
        self.screen = screen
        self.font = font
        self.boss_happiness_meter = boss_happiness_meter
        self.salary_meter = salary_meter

        self.emails = []
        self.create_emails()

        self.current_email_index = 0
        self.reply_mode = False
        self.response_options = []
        self.show_no_response_text = False

    def create_emails(self):
        # Email samples with various actions
        sample_emails = [
            {"content": "Subject: Project Update\n\nHi Team,\nPlease find attached the project update.", "type": "reply", "responses": ["I'll review it right away!", "I don’t have time for this now."]},
            {"content": "Subject: Quick Reminder\n\nReminder to submit your reports by tomorrow.", "type": "reply", "responses": ["Thanks for the reminder!", "I’ll submit it next week."]},
            {"content": "Subject: Discount on Extended Car Warranty!\n\nGet 50% off now!", "type": "spam"},
            {"content": "Subject: Share This with the Marketing Team\n\nHi, please share this document with the marketing team.", "type": "forward", "responses": ["I’ll forward it to the team.", "I don’t think anyone else needs this."]},
            {"content": "Subject: Meeting Reschedule\n\nThe meeting has been rescheduled.", "type": "reply", "responses": ["Thanks, I’ll update my calendar.", "I’ll just skip the meeting."]},
            {"content": "Subject: Free Vacation Prize!\n\nClaim your free vacation to Hawaii!", "type": "spam"},
            {"content": "Subject: Client Feedback\n\nPlease forward this to the client for review.", "type": "forward", "responses": ["I’ll forward it right away.", "I don’t think they need this."]},
            {"content": "Subject: Important Notice\n\nPolicy changes are now live. Read carefully.", "type": "reply", "responses": ["I’ll read the changes.", "Not interested in policies."]},
        ]

        for email_data in sample_emails:
            self.emails.append(email_data)

    def display_email(self):
        if self.current_email_index >= len(self.emails):
            print("Game Over! You have processed all emails.")
            pygame.quit()
            return

        email = self.emails[self.current_email_index]
        self.screen.fill(DARK_GRAY)

        # Display email content
        content_lines = email['content'].split('\n')
        for i, line in enumerate(content_lines):
            text_surface = self.font.render(line, True, WHITE)
            self.screen.blit(text_surface, (20, 50 + i * 30))

        # Display action buttons
        reply_button = self.font.render("Reply (R)", True, WHITE)
        forward_button = self.font.render("Forward (F)", True, WHITE)
        delete_button = self.font.render("Delete (D)", True, WHITE)
        self.screen.blit(reply_button, (20, 400))
        self.screen.blit(forward_button, (200, 400))
        self.screen.blit(delete_button, (380, 400))

        # Show reply options if in reply mode
        if self.reply_mode:
            if self.response_options:
                response1 = self.font.render("1. " + self.response_options[0], True, WHITE)
                response2 = self.font.render("2. " + self.response_options[1], True, WHITE)
                self.screen.blit(response1, (20, 450))
                self.screen.blit(response2, (20, 490))
            else:
                self.show_no_response_text = True

        # Display "No response options available" text if applicable
        if self.show_no_response_text:
            no_response = self.font.render("No response options available.", True, WHITE)
            self.screen.blit(no_response, (20, 450))

        # Draw meters
        self.boss_happiness_meter.draw(self.screen, (20, 550))
        self.salary_meter.draw(self.screen, (20, 600))

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:  # Reply
            self.reply_mode = True
            if self.emails[self.current_email_index]["type"] == "reply":
                self.response_options = self.emails[self.current_email_index]["responses"]
            else:
                print("Incorrect action! This email is not for replying.")
                self.boss_happiness_meter.decrease(10)
                self.show_no_response_text = True

        elif keys[pygame.K_f]:  # Forward
            if self.emails[self.current_email_index]["type"] == "forward":
                print("Email forwarded successfully.")
                self.boss_happiness_meter.value = min(self.boss_happiness_meter.max_value, self.boss_happiness_meter.value + 10)
            else:
                print("Incorrect action! This email is not for forwarding.")
                self.boss_happiness_meter.decrease(10)
            self.show_no_response_text = False
            self.current_email_index += 1

        elif keys[pygame.K_d]:  # Delete
            if self.emails[self.current_email_index]["type"] == "spam":
                print("Spam deleted.")
                self.salary_meter.value = min(self.salary_meter.max_value, self.salary_meter.value + 10)
            else:
                print("Incorrect action! This email is not spam.")
                self.boss_happiness_meter.decrease(10)
            self.show_no_response_text = False
            self.current_email_index += 1

        if self.reply_mode:
            if keys[pygame.K_1]:  # First response option
                self.reply_to_email(0)
            elif keys[pygame.K_2]:  # Second response option
                self.reply_to_email(1)

    def reply_to_email(self, option_index):
        email = self.emails[self.current_email_index]
        if email["type"] == "reply":
            if option_index == 0:  # Correct response
                print("Correct response!")
                self.boss_happiness_meter.value = min(self.boss_happiness_meter.max_value, self.boss_happiness_meter.value + 10)
            else:  # Incorrect response
                print("Incorrect response!")
                self.boss_happiness_meter.decrease(10)

        self.reply_mode = False
        self.show_no_response_text = False
        self.current_email_index += 1
        if self.current_email_index >= len(self.emails):
            print("Game Over! You have processed all emails.")
            pygame.quit()

def main():
    # Initialize screen and font
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Email Game")
    font = pygame.font.Font(None, 24)

    # Create meters
    boss_happiness_meter = Meter("Boss Happiness", 100)
    salary_meter = Meter("Salary", 100)

    # Initialize the Email Game
    email_game = EmailGame(screen, boss_happiness_meter, salary_meter, font)

    # Main game loop
    running = True
    clock = pygame.time.Clock()
    
    while running:
        # Check for quit event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Handle input and update game state
        email_game.handle_input()

        # Check if the game is over (i.e., all emails processed)
        if email_game.current_email_index >= len(email_game.emails):
            print("Game Over! You have processed all emails.")
            running = False  # Stop the loop
            continue  # Skip display update if game is over

        # Display current email and update the display
        email_game.display_email()
        pygame.display.flip()
        clock.tick(30)

    # Clean up and quit Pygame after the loop ends
    pygame.quit()

if __name__ == "__main__":
    main()
