import pygame
import random
import time

class TypingGame:
    def __init__(self, screen, font, time_limit=60):
        self.screen = screen
        self.font = font
        self.time_limit = time_limit
        self.prompt = self.generate_prompt()
        self.prompt_lines = self.wrap_text(self.prompt, self.screen.get_width() - 100)
        self.start_time = None
        self.user_input = ""
        self.success = False
        self.finished = False

    def generate_prompt(self):
        # List of random prompts to use in the game
        prompts = [
            "So, moving forward, let's make sure we're aligning our resources effectively. We really need to leverage our core competencies to drive synergy across departments. Keep those KPIs in mind, and let’s circle back next week with a clear action plan.",
            "I just want to double-click on that point—our primary focus should be on optimizing workflow efficiencies. We’re aiming to streamline processes, eliminate redundancies, and ideally see a 15% productivity increase across the board.",
            "Great, let’s park that idea for now, but I think it’s definitely something to revisit down the line. Right now, our bandwidth is limited, so we should focus on our current roadmap and iterate once we've hit those key milestones.",
            # Add more prompts if needed
        ]
        return random.choice(prompts)

    def wrap_text(self, text, max_width):
        """Splits the text into lines that fit within max_width."""
        words = text.split()
        lines = []
        current_line = ""

        for word in words:
            # Check if adding the next word would exceed the max width
            test_line = f"{current_line} {word}".strip()
            if self.font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word

        # Add the last line if there's any text left
        if current_line:
            lines.append(current_line)

        return lines

    def wrap_input_text(self, input_text, max_width):
        """Splits the user input into lines that fit within max_width."""
        lines = []
        current_line = ""

        for char in input_text:
            test_line = current_line + char
            if self.font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = char

        # Add the last line if there's any text left
        if current_line:
            lines.append(current_line)

        return lines

    def start_game(self):
        # Start the timer
        self.start_time = time.time()
        self.user_input = ""
        self.finished = False
        self.success = False

    def update(self):
        # Calculate remaining time
        elapsed_time = time.time() - self.start_time
        remaining_time = max(0, self.time_limit - elapsed_time)
        
        # Check if time has run out
        if remaining_time <= 0 and not self.finished:
            self.finished = True
            self.success = False

        # Display the wrapped prompt, wrapped user input, and timer
        self.display_wrapped_text(self.prompt_lines, (50, 100))
        
        # Wrap user input text and display it
        wrapped_input = self.wrap_input_text(self.user_input, self.screen.get_width() - 100)
        self.display_wrapped_text(wrapped_input, (50, 150 + len(self.prompt_lines) * 30))
        
        # Display timer
        self.display_text(f"Time Left: {int(remaining_time)}", (50, 200 + len(self.prompt_lines) * 30 + len(wrapped_input) * 30))

        # If input matches the prompt and within time, set success
        if self.user_input == self.prompt and not self.finished:
            self.finished = True
            self.success = True

    def display_text(self, text, position):
        # Helper function to render text on the screen
        rendered_text = self.font.render(text, True, (255, 255, 255))
        self.screen.blit(rendered_text, position)

    def display_wrapped_text(self, lines, start_position):
        """Displays each line of wrapped text with vertical spacing."""
        x, y = start_position
        for line in lines:
            self.display_text(line, (x, y))
            y += 30  # Move down for the next line

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and not self.finished:
            if event.key == pygame.K_RETURN:  # Press Enter to check input
                self.finished = True
                self.success = self.user_input == self.prompt
            elif event.key == pygame.K_BACKSPACE:  # Handle backspace
                self.user_input = self.user_input[:-1]
            elif event.unicode:  # Add character to input
                self.user_input += event.unicode

    def get_score(self):
        # Calculate score based on remaining time if success
        if self.success:
            elapsed_time = time.time() - self.start_time
            return max(0, int((self.time_limit - elapsed_time) * 10))
        return 0

    def is_finished(self):
        # Check if the game is finished
        return self.finished

    def is_successful(self):
        # Check if the game was successful
        return self.success