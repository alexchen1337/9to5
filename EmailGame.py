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
        # Draw the meter as a bar
        bar_width = 200
        bar_height = 30
        fill_ratio = self.value / self.max_value
        fill_color = RED if self.name == "Boss Happiness" else BLUE  # Red for boss happiness, blue for salary
        pygame.draw.rect(screen, GRAY, (pos[0], pos[1], bar_width, bar_height))  # Grey background
        pygame.draw.rect(screen, fill_color, (pos[0], pos[1], bar_width * fill_ratio, bar_height))  # Fill based on value

class EmailGame:
    def __init__(self, screen, boss_happiness_meter, salary_meter, font):
        self.screen = screen
        self.font = font
        self.boss_happiness_meter = boss_happiness_meter
        self.salary_meter = salary_meter

        self.emails = []
        self.create_emails()

        self.current_email_index = 0
        self.reply_mode = False  # Track if we are in reply mode
        self.response_options = []  # Store response options for replies
        self.show_no_response_text = False  # Flag to control no response text visibility

    def create_emails(self):
        # Create a list of sample emails with varied content
        sample_contents = [
            "Subject: Project Update\n\nHi Team,\nPlease find attached the project update. Let me know if you have any questions.\nBest,\nManager",
            "Subject: Quick Reminder\n\nHello,\nJust a reminder to submit your reports by end of day tomorrow.\nThanks!",
            "Subject: Request for Feedback\n\nHi,\nCould you please review the attached document and provide your feedback? Thank you!",
            "Subject: Team Lunch\n\nHey everyone,\nWe are planning a team lunch this Friday. Please RSVP if you can make it.\nCheers!",
            "Subject: Important Notice\n\nDear Team,\nThis is to inform you about the upcoming policy changes. Please read the details carefully.",
            "Subject: Share This\n\nHi,\nCould you please share this document with others? It's important for our next meeting.\nThanks!",
            "Subject: Meeting Reschedule\n\nHello,\nThe meeting has been rescheduled to next week. Please check your calendars.\nBest regards.",
            "Subject: Client Request\n\nHi,\nWe received a request from the client for additional features. Let's discuss this in our next meeting.",
            "Subject: Thank You\n\nThank you for your hard work on the last project. It was a great success!",
            "Subject: New Policy Update\n\nPlease read the new policy document and let me know your thoughts."
        ]

        # Create email structure with response options
        for content in sample_contents:
            email_type = random.choice(['reply', 'forward', 'delete'])  # Randomly assign type
            email = {
                'content': content,
                'type': email_type
            }
            self.emails.append(email)

    def display_email(self):
        email = self.emails[self.current_email_index]
        self.screen.fill(DARK_GRAY)

        # Display email content
        content_lines = email['content'].split('\n')
        for i, line in enumerate(content_lines):
            text_surface = self.font.render(line, True, WHITE)
            self.screen.blit(text_surface, (20, 50 + i * 30))

        # Display buttons
        reply_button = self.font.render("Reply (R)", True, WHITE)
        forward_button = self.font.render("Forward (F)", True, WHITE)
        delete_button = self.font.render("Delete (D)", True, WHITE)
        self.screen.blit(reply_button, (20, 400))
        self.screen.blit(forward_button, (200, 400))
        self.screen.blit(delete_button, (380, 400))

        # Show reply options if in reply mode
        if self.reply_mode:
            if self.response_options:  # Check if response options are available
                response1 = self.font.render("1. " + self.response_options[0], True, WHITE)
                response2 = self.font.render("2. " + self.response_options[1], True, WHITE)
                self.screen.blit(response1, (20, 450))
                self.screen.blit(response2, (20, 490))
            else:
                self.show_no_response_text = True  # Set flag to show no response text

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
            self.response_options = ["I'll review this file", "I'll review the wrong file"]  # Example responses

        elif keys[pygame.K_f]:  # Forward
            self.forward_email()

        elif keys[pygame.K_d]:  # Delete
            self.delete_email()

        if self.reply_mode:
            if keys[pygame.K_1]:  # First response option
                self.reply_to_email(0)
            elif keys[pygame.K_2]:  # Second response option
                self.reply_to_email(1)

    def reply_to_email(self, option_index):
        email = self.emails[self.current_email_index]
        if option_index == 0:  # Correct response
            print("Correct response!")
            self.boss_happiness_meter.value = min(self.boss_happiness_meter.max_value, self.boss_happiness_meter.value + 10)  # Increase happiness
        else:  # Incorrect response
            print("Incorrect response!")
            self.boss_happiness_meter.decrease(10)  # Decrease boss happiness

        self.reply_mode = False
        self.show_no_response_text = False  # Reset flag when replying
        self.current_email_index += 1  # Move to the next email
        if self.current_email_index >= len(self.emails):
            # End the game after processing all emails
            print("Game Over! You have processed all emails.")
            pygame.quit()  # Quit the game

    def forward_email(self):
        print("Email forwarded.")
        self.show_no_response_text = False  # Reset flag when forwarding
        self.current_email_index += 1
        if self.current_email_index >= len(self.emails):
            # End the game after processing all emails
            print("Game Over! You have processed all emails.")
            pygame.quit()  # Quit the game

    def delete_email(self):
        print("Email deleted.")
        # Decrease boss happiness when an email is deleted incorrectly
        if self.emails[self.current_email_index]['type'] != 'delete':
            self.boss_happiness_meter.decrease(10)  # Decrease happiness if not a delete email
        self.show_no_response_text = False  # Reset flag when deleting
        self.current_email_index += 1
        if self.current_email_index >= len(self.emails):
            # End the game after processing all emails
            print("Game Over! You have processed all emails.")
            pygame.quit()  # Quit the game

def main():
    # Create the screen and font
    screen = pygame.display.set_mode((800, 600))  # Standard resolution
    pygame.display.set_caption("Email Game")
    font = pygame.font.Font(None, 24)  # Default font with size 24

    # Create meters
    boss_happiness_meter = Meter("Boss Happiness", 100)
    salary_meter = Meter("Salary", 100)

    # Initialize the Email Game
    email_game = EmailGame(screen, boss_happiness_meter, salary_meter, font)

    # Main game loop
    running = True
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        email_game.handle_input()
        email_game.display_email()

        if email_game.current_email_index >= len(email_game.emails):
            # End the game after processing all emails
            running = False

        pygame.display.flip()  # Update the display
        clock.tick(30)  # Frame rate

    pygame.quit()

if __name__ == "__main__":
    main()
