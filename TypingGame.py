import pygame
import random
import time
import string

class TypingGame:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.time_limit = 55
        self.prompt = self.generate_prompt()
        self.prompt_lines = self.wrap_text(self.prompt, self.screen.get_width() - 100)
        self.start_time = None
        self.user_input = ""
        self.success = False
        self.finished = False

    def generate_prompt(self):
        prompts = [
            "Moving forward, lets make sure we are aligning our resources effectively. We really need to leverage our core competencies to drive synergy across departments. Keep those KPIs in mind, and lets circle back next week with a clear action plan.",
            "I want to focus on that point, our primary focus should be on optimizing workflow efficiencies. We are aiming to streamline processes, eliminate redundancies, and ideally see a 15% productivity increase across the board.",
            "Great, lets park that idea for now, but I think its definitely something to revisit down the line. Right now, our bandwidth is limited, so we should focus on our current roadmap and iterate once we hit those key milestones.",
            "I think the low hanging fruit here is to enhance customer touchpoints. We need to create a more seamless experience for users, leveraging our analytics to improve engagement and drive conversions.",
            "Can we take a 10000 foot view on this? Our objective here is to map out a strategy that will provide both immediate wins and long term value. We do not want to lose sight of the forest for the trees.",
            "I want everyone to take a look at the latest numbers from last quarter. If we drill down, we will see that there is room to optimize our spend while increasing ROI. Lets reconvene with actionable insights next week.",
            "To add to that idea, we need to be agile with our deliverables. It is essential to stay adaptive in this market. Lets prioritize projects that bring us the highest value in the shortest time frame.",
            "Can we make sure we are all on the same page regarding project timelines? Our goal is to be proactive, not reactive. I would like us to build a timeline that ensures we are meeting all deadlines without bottlenecks.",
            "Just to clarify, our target is to enhance customer experience at every touchpoint. That means aligning our messaging, product, and service quality with customer expectations. It is all about brand consistency and building trust.",
            "Lets not reinvent the wheel here. We already have a solid foundation, what we need to do is refine and iterate. Focus on quick wins and bring back results in our next sync."
        ]
        return random.choice(prompts)

    def wrap_text(self, text, max_width):
        words = text.split()
        lines = []
        current_line = ""

        for word in words:
            test_line = f"{current_line} {word}".strip()
            if self.font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word

        if current_line:
            lines.append(current_line)

        return lines

    def wrap_input_text(self, input_text, max_width):
        lines = []
        current_line = ""

        for char in input_text:
            test_line = current_line + char
            if self.font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = char

        if current_line:
            lines.append(current_line)

        return lines

    def start_game(self):
        self.start_time = time.time()
        self.user_input = ""
        self.finished = False
        self.success = False

    def update(self):
        elapsed_time = time.time() - self.start_time
        remaining_time = max(0, self.time_limit - elapsed_time)

        if remaining_time <= 0 and not self.finished:
            self.finished = True
            self.success = False
            print("Time's up! Task failed.")  # Optional feedback

        # Display the wrapped prompt and user input with highlighting
        self.display_wrapped_text(self.prompt_lines, (50, 100))
        
        wrapped_input = self.wrap_input_text(self.user_input, self.screen.get_width() - 100)
        self.display_wrapped_text_with_highlighting(wrapped_input, self.prompt, (50, 150 + len(self.prompt_lines) * 30))
        
        # Display timer
        self.display_text(f"Time Left: {int(remaining_time)}", (50, 200 + len(self.prompt_lines) * 30 + len(wrapped_input) * 30))

        # Check for completion (case-insensitive)
        if self.user_input.lower() == self.prompt.lower() and not self.finished:
            self.finished = True
            self.success = True

    def display_text(self, text, position, color=(255, 255, 255)):
        rendered_text = self.font.render(text, True, color)
        self.screen.blit(rendered_text, position)

    def display_wrapped_text(self, lines, start_position):
        x, y = start_position
        for line in lines:
            self.display_text(line, (x, y))
            y += 30  

    def display_wrapped_text_with_highlighting(self, wrapped_input, prompt, start_position):
        x, y = start_position
        correct_color = (255, 255, 255)  # White
        incorrect_color = (255, 0, 0)    # Red

        prompt_lower = prompt.lower()
        user_input_lower = self.user_input.lower()
        
        # Check if there's an error in the current input
        self.has_error = False
        for i, char in enumerate(user_input_lower):
            if i >= len(prompt_lower) or char != prompt_lower[i]:
                self.has_error = True
                break

        for line in wrapped_input:
            rendered_line = ""
            line_has_error = False
            
            for i, char in enumerate(line):
                rendered_line += char
                # Check if character is correct and no previous errors
                if i < len(prompt_lower) and user_input_lower[i] == prompt_lower[i] and not line_has_error:
                    color = correct_color
                else:
                    color = incorrect_color
                    line_has_error = True
                
                self.display_text(rendered_line, (x, y), color)
            y += 30

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and not self.finished:
            if event.key == pygame.K_BACKSPACE:
                self.user_input = self.user_input[:-1]
                # Reset error state when backspacing
                self.has_error = False
            elif event.key == pygame.K_RETURN:
                pass  # Ignore enter key
            else:
                # Only accept new characters if there's no error
                if not self.has_error and event.unicode.isprintable():
                    self.user_input += event.unicode

    def get_score(self):
        if self.success:
            elapsed_time = time.time() - self.start_time
            return max(0, int((self.time_limit - elapsed_time) * 10))
        return 0

    def is_finished(self):
        return self.finished

    def is_successful(self):
        return self.success
