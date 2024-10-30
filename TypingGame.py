import pygame
import random
import time
import string

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
        prompts = [
            "So, moving forward, let's make sure we're aligning our resources effectively. We really need to leverage our core competencies to drive synergy across departments. Keep those KPIs in mind, and let’s circle back next week with a clear action plan.",
    "I just want to double-click on that point—our primary focus should be on optimizing workflow efficiencies. We’re aiming to streamline processes, eliminate redundancies, and ideally see a 15% productivity increase across the board.",
    "Great, let’s park that idea for now, but I think it’s definitely something to revisit down the line. Right now, our bandwidth is limited, so we should focus on our current roadmap and iterate once we've hit those key milestones.",
    "I think the low-hanging fruit here is to enhance customer touchpoints. We need to create a more seamless experience for users, leveraging our analytics to improve engagement and ultimately drive conversions.",
    "Can we take a 10,000-foot view on this? Our objective here is to map out a strategy that’ll provide both immediate wins and long-term value. We don’t want to lose sight of the forest for the trees.",
    "I want everyone to take a look at the latest numbers from last quarter. If we drill down, we’ll see that there’s room to optimize our spend while increasing ROI. Let’s reconvene with actionable insights next week.",
    "To piggyback on that idea, we need to be agile with our deliverables. It’s essential to stay adaptive in this market. Let’s prioritize projects that bring us the highest value in the shortest time frame.",
    "Can we make sure we’re all on the same page regarding project timelines? Our goal is to be proactive, not reactive. I’d like us to build a timeline that ensures we're meeting all deadlines without bottlenecks.",
    "Just to clarify, our target is to enhance customer experience at every touchpoint. That means aligning our messaging, product, and service quality with customer expectations. It’s all about brand consistency and building trust.",
    "Let’s not reinvent the wheel here. We already have a solid foundation—what we need to do is refine and iterate. Focus on quick wins and bring back results in our next sync.",
    "Everyone, let’s shift gears to prioritize resource allocation. We have to make sure we’re optimizing our efforts where they count the most. That’ll involve some hard choices, but it’ll keep us efficient.",
    "I want us to drill down on our customer personas. Understanding them will allow us to personalize and better meet their needs. This quarter, let’s make this a priority to drive retention rates.",
    "If we can get everyone’s buy-in on the roadmap, it’ll make execution smoother. Transparency and open feedback are key here, so let’s make sure everyone’s voices are heard.",
    "Looking at the bigger picture, we should be considering scalability in every project. Let’s future-proof our processes so we can handle growth without constant restructuring.",
    "Can we circle back on last week's action items? I think we have some gaps in execution that need addressing. If everyone can provide status updates, we’ll have a clearer path forward.",
    "Our focus for the next quarter should be on delivering measurable results. Set clear KPIs for your teams and let’s keep a close eye on progress. We’ll assess at the end of each sprint.",
    "The goal is to work smarter, not harder. Look for efficiencies within your team and let’s see if we can reduce redundant tasks. Our time could be better spent on value-added activities.",
    "Are there any blockers that are stopping us from meeting these deadlines? Let’s get those out in the open so we can find solutions before they impact our timeline.",
    "I’d like to see us take a data-driven approach to decision-making. Let’s base our strategies on insights rather than assumptions, and ensure we’re tracking the right metrics.",
    "Let’s go around and get everyone’s quick thoughts. I want to ensure we’re capturing a 360-degree perspective on this project. Your input is essential to refining our approach.",
    "Our North Star remains customer satisfaction. Whatever we do, it’s all in service of that goal. Let’s make sure every team member understands this is our primary directive.",
    "Could everyone please ensure their deliverables are on track? If you anticipate delays, flag them early so we can recalibrate without compromising the timeline.",
    "All right, let’s table any less critical issues until we’ve resolved our high-priority action items. This will ensure we’re dedicating resources to the most impactful tasks.",
    "I want us to start thinking about cross-department collaboration. There are synergies we can exploit by working more closely with other teams. Let’s strategize on how we can facilitate that.",
    "As we move forward, let’s keep an agile mindset. Flexibility will be essential in a market that changes rapidly. We need to pivot quickly if we spot new opportunities.",
    "I’d like to schedule a deep-dive meeting to discuss this. A high-level overview isn’t enough; we need to get into the weeds and map out every part of the process.",
    "Are we benchmarking against industry standards? I’d like us to have a clear idea of where we stand relative to competitors. It’ll help us position ourselves effectively.",
    "If everyone could come to the next meeting with at least two potential solutions to these pain points, we can have a constructive discussion and decide on the best course of action.",
    "We’re looking for ideas that have a strong ROI. Think strategically about which initiatives will have the most impact for the least investment. Let’s not overextend our resources.",
    "Remember, our endgame is growth. Everything we do should be driving towards that outcome. I’d like everyone to keep that in mind when prioritizing tasks.",
    "Any feedback on the current workflow? If there are inefficiencies, we need to address them head-on. Our goal is a seamless, scalable process that doesn’t burn out the team.",
    "I’d like us to build a contingency plan. Let’s be prepared for worst-case scenarios so that any disruptions don’t stall our progress. Think of it as insurance for the project.",
    "Can we add more checkpoints in the timeline? Regular reviews will allow us to catch issues early and ensure we’re on track to meet our deliverables.",
    "Our top priority should be quality over quantity. Delivering a polished product is more important than rushing to complete multiple projects at once.",
    "Let’s establish a framework for feedback so everyone can share insights. It’ll keep the process collaborative and ensure we’re all invested in the final product.",
    "Are there any quick wins we can leverage to boost morale? If we can identify small victories, it’ll keep momentum going for the bigger, long-term projects.",
    "I’d like to see us get proactive with our risk assessment. Identifying potential blockers now will allow us to mitigate issues before they even arise.",
    "We need to streamline communication. Let’s reduce redundant updates and make sure information is accessible and clear. Efficiency here will free up time for execution.",
    "Are we optimizing our tech stack? Let’s ensure we’re using tools that enhance productivity rather than add complexity. It might be time to audit and consolidate.",
    "For our next phase, let’s focus on stakeholder alignment. We need buy-in at all levels to maintain momentum and avoid bottlenecks when we hit critical milestones.",
    "Can we create a knowledge-sharing platform? That way, we can capture everyone’s expertise and make it accessible across the team, especially for cross-functional projects.",
    "Before we close, I want everyone to prepare a list of three key takeaways for next week’s meeting. It’ll give us a head start and keep us focused on what matters.",
    "Are we thinking about succession planning? We should be prepared for team transitions and ensure we have backup personnel for critical roles to avoid disruptions.",
    "Let’s not get bogged down in the details. Keep your focus on the overarching goals and revisit specifics only if they’re critical to achieving the next milestone.",
    "Everyone, please document your processes. If we have clear SOPs, we’ll avoid confusion down the line and ensure a consistent approach regardless of team changes.",
    "Can we set up a system for peer reviews? It’ll help maintain high-quality outputs and allow team members to learn from one another in a constructive way.",
    "I’d like us to build a playbook for future projects. It’ll create a framework that simplifies onboarding and ensures we’re not starting from scratch each time.",
    "Is everyone clear on their next steps? Clarity is key here, so let’s eliminate any ambiguity now to avoid misunderstandings and rework later.",
    "Please flag any resource constraints as soon as they arise. The sooner we know, the quicker we can adjust to keep things moving smoothly.",
    "Our goal is seamless execution. Keep communication open, focus on high-impact tasks, and don’t hesitate to escalate if you hit a roadblock. Let’s keep up the momentum."
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
        correct_color = (255, 255, 255)
        incorrect_color = (255, 0, 0)

        prompt_lower = prompt.lower()
        user_input_lower = self.user_input.lower()

        for line in wrapped_input:
            rendered_line = ""
            for i, char in enumerate(line):
                if i < len(prompt_lower) and user_input_lower[i] == prompt_lower[i]:
                    rendered_line += char
                    color = correct_color
                else:
                    rendered_line += char
                    color = incorrect_color
                self.display_text(rendered_line, (x, y), color)
            y += 30 

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and not self.finished:
            if event.key == pygame.K_BACKSPACE:
                self.user_input = self.user_input[:-1]
            elif event.unicode in string.ascii_letters + string.digits + string.punctuation + " ":
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
