import pygame
import random
import time
from Relationships import RelationshipGraph

class EmailGame:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.emails = [
            {"subject": "Project Deadline", "content": "Can you submit the report by Monday?", "action": "reply", 
             "reply_options": ["Yes, I can do that.", "No, I need more time."], "correct_reply": 0},
            {"subject": "Weekly Team Meeting", "content": "Are you attending the team meeting tomorrow?", "action": "reply", 
             "reply_options": ["Yes, I'll be there.", "Sorry, I have a conflict."], "correct_reply": 0},
            {"subject": "Urgent: Security Update", "content": "Please forward this to all department heads.", "action": "forward"},
            {"subject": "Spam Offer", "content": "Exclusive deal just for you!", "action": "delete"},
            {"subject": "Question About Report", "content": "Could you clarify your analysis in the report?", "action": "reply", 
             "reply_options": ["Sure, I’ll explain.", "It’s already clear."], "correct_reply": 0},
            {"subject": "Happy Birthday!", "content": "Don't forget to wish Sarah a happy birthday!", "action": "delete"},
            {"subject": "Client Feedback", "content": "Please review the client feedback and let me know your thoughts.", "action": "reply", 
             "reply_options": ["I’ll review it.", "Not necessary."], "correct_reply": 0},
            {"subject": "Monthly Report Due", "content": "The monthly report is due next week.", "action": "forward"},
            {"subject": "Discount Offer", "content": "Get 20% off on your next order!", "action": "delete"},
            {"subject": "Team Building Activity", "content": "Are you interested in joining the team building activity?", "action": "reply", 
             "reply_options": ["Yes, sounds fun!", "No, I’m not interested."], "correct_reply": 0},
            {"subject": "File Request", "content": "Could you forward the files to Sarah?", "action": "forward"},
            {"subject": "Lunch Plans", "content": "Do you want to join us for lunch today?", "action": "reply", 
             "reply_options": ["Yes, count me in!", "I’ll pass today."], "correct_reply": 0},
            {"subject": "Project Approval", "content": "Please send this to the client for approval.", "action": "forward"},
            {"subject": "Congratulations!", "content": "Congratulations on your work anniversary!", "action": "delete"},
            {"subject": "System Maintenance", "content": "The system will be down for maintenance this weekend.", "action": "delete"},
            {"subject": "Leave Request", "content": "Could you cover my tasks while I’m on leave?", "action": "reply", 
             "reply_options": ["Yes, I can help.", "I have too much work."], "correct_reply": 0},
            {"subject": "Task Reminder", "content": "Don't forget to complete the assigned tasks by end of day.", "action": "delete"},
            {"subject": "Sales Promotion", "content": "Big sale on office supplies. Don’t miss out!", "action": "delete"},
            {"subject": "Presentation", "content": "Could you review my presentation slides?", "action": "reply", 
             "reply_options": ["Sure, I’ll take a look.", "I don’t have time."], "correct_reply": 0},
            {"subject": "Daily Updates", "content": "Please forward this to all team members.", "action": "forward"},
            {"subject": "Budget Report", "content": "Can you send the budget report by Friday?", "action": "reply", 
             "reply_options": ["Yes, I can do that.", "No, I’ll need more time."], "correct_reply": 0},
            {"subject": "Software Update", "content": "There is a new update available for your software.", "action": "delete"},
            {"subject": "HR Policy Change", "content": "Please forward the updated HR policies to your team.", "action": "forward"},
            {"subject": "Meeting Follow-Up", "content": "Can we discuss the meeting outcomes?", "action": "reply", 
             "reply_options": ["Yes, let’s do it.", "I don’t need to."], "correct_reply": 0},
            {"subject": "Promotion Offer", "content": "Check out this amazing promotion!", "action": "delete"},
            {"subject": "Code Review", "content": "Could you help review my code changes?", "action": "reply", 
             "reply_options": ["Yes, happy to help.", "I’m too busy."], "correct_reply": 0},
            {"subject": "Event Invitation", "content": "You’re invited to the company event next month.", "action": "reply", 
             "reply_options": ["I’d love to attend.", "I’ll skip it."], "correct_reply": 0},
            {"subject": "Marketing Presentation", "content": "Forward this presentation to the sales team.", "action": "forward"},
            {"subject": "Important Notice", "content": "Please forward this notice to all employees.", "action": "forward"},
            {"subject": "Budget Approval", "content": "Could you approve the budget?", "action": "reply", 
             "reply_options": ["Yes, I approve.", "No, it needs changes."], "correct_reply": 0},
            {"subject": "Spam Promotion", "content": "Save big on your next purchase with this offer!", "action": "delete"},
            {"subject": "Team Discussion", "content": "Could you join the team discussion this afternoon?", "action": "reply", 
             "reply_options": ["Yes, I’ll be there.", "No, I can’t make it."], "correct_reply": 0},
            {"subject": "Newsletter Subscription", "content": "Don’t miss our next newsletter!", "action": "delete"},
            {"subject": "IT Support", "content": "Please send this to IT for troubleshooting.", "action": "forward"},
            {"subject": "Customer Query", "content": "Could you reply to the customer’s query?", "action": "reply", 
             "reply_options": ["Yes, I’ll handle it.", "I’ll pass."], "correct_reply": 0},
            {"subject": "System Alert", "content": "Your account may be at risk. Update your password.", "action": "delete"},
            {"subject": "Happy Holidays", "content": "Enjoy the holiday season with a special offer!", "action": "delete"},
            {"subject": "Document Review", "content": "Could you review the document before submission?", "action": "reply", 
             "reply_options": ["Yes, I’ll review it.", "I don’t need to."], "correct_reply": 0},
            {"subject": "Monthly Newsletter", "content": "Check out our monthly updates!", "action": "delete"},
            {"subject": "Feedback Request", "content": "Could you provide feedback on my proposal?", "action": "reply", 
             "reply_options": ["Yes, I’ll give feedback.", "No, I don’t have time."], "correct_reply": 0},
            {"subject": "Sales Report", "content": "Forward the sales report to the finance team.", "action": "forward"},
            {"subject": "Code Review Reminder", "content": "Please complete the code review by tomorrow.", "action": "delete"},
            {"subject": "Training Session", "content": "Do you want to attend the training session next week?", "action": "reply", 
             "reply_options": ["Yes, sign me up.", "No, I’m not interested."], "correct_reply": 0},
            {"subject": "Birthday Reminder", "content": "Don’t forget to wish Alice a happy birthday!", "action": "delete"},
            {"subject": "Job Application", "content": "Please forward this application to HR.", "action": "forward"},
            {"subject": "New Project Proposal", "content": "Could you review the new project proposal?", "action": "reply", 
             "reply_options": ["Yes, I’ll review it.", "No, I don’t need to."], "correct_reply": 0},
            {"subject": "Monthly Meeting", "content": "The monthly meeting is scheduled for next Tuesday.", "action": "delete"},
            {"subject": "Task Delegation", "content": "Could you take over this task?", "action": "reply", 
             "reply_options": ["Yes, I can help.", "No, I’m overloaded."], "correct_reply": 0},
        ]
        self.current_email = None
        self.user_choice = None
        self.waiting_for_reply = False
        self.success = False
        self.finished = False
        self.current_email_index = 0
        self.total_correct = 0
        self.total_incorrect = 0  # Track incorrect answers
        self.required_correct = 10
        self.max_incorrect = 6    # Maximum allowed incorrect answers
        self.start_time = None    # Track game start time
        self.time_limit = 30      # 30 second time limit
        self.message = None  # Initialize message attribute
        self.message_time = 0  # Initialize message_time attribute

    def start_game(self):
        random.shuffle(self.emails)
        self.current_email = self.emails[0]
        self.current_email_index = 0
        self.total_correct = 0
        self.total_incorrect = 0
        self.success = False
        self.finished = False
        self.start_time = time.time()

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if not self.waiting_for_reply:
                if event.key in [pygame.K_1, pygame.K_2, pygame.K_3]:
                    choice = event.key - pygame.K_1  # Convert to 0, 1, 2
                    if self.current_email["action"] == "reply" and choice == 0:
                        self.waiting_for_reply = True
                    else:
                        self.check_answer(choice)
            else:  # Handling reply options
                if event.key in [pygame.K_a, pygame.K_b]:
                    reply_choice = 0 if event.key == pygame.K_a else 1
                    self.check_reply(reply_choice)

    def check_answer(self, choice):
        action_map = {0: "reply", 1: "forward", 2: "delete"}
        action = action_map.get(choice)
        if self.current_email["action"] == action:
            self.total_correct += 1
        else:
            self.total_incorrect += 1
        self.check_game_over()
        if not self.finished:
            self.next_email()

    def check_reply(self, reply_choice):
        if self.current_email["correct_reply"] == reply_choice:
            self.total_correct += 1
        else:
            self.total_incorrect += 1
        self.waiting_for_reply = False
        self.check_game_over()
        if not self.finished:
            self.next_email()

    def check_game_over(self):
        current_time = time.time()
        time_elapsed = current_time - self.start_time
        
        # Check all failure conditions
        if (time_elapsed >= self.time_limit or 
            self.total_incorrect >= self.max_incorrect):
            self.finished = True
            self.success = False
        # Check win condition
        elif self.total_correct >= self.required_correct:
            self.finished = True
            self.success = True

    def next_email(self):
        self.current_email_index += 1
        if self.current_email_index >= len(self.emails):
            self.finished = True
            self.success = self.total_correct >= self.required_correct
        else:
            self.current_email = self.emails[self.current_email_index]

    def update(self):
        self.check_game_over()  # Check time limit
        self.screen.fill((30, 30, 30))
        
        if not self.finished:
            # Draw email content
            self.draw_text(f"Subject: {self.current_email['subject']}", 50, 50)
            self.draw_text(f"Content: {self.current_email['content']}", 50, 100)
            self.draw_text("Choose action: [1] Reply [2] Forward [3] Delete", 50, 200)
            
            if self.waiting_for_reply:
                self.draw_text(f"Reply Options:", 50, 250)
                self.draw_text(f"[A] {self.current_email['reply_options'][0]}", 50, 300)
                self.draw_text(f"[B] {self.current_email['reply_options'][1]}", 50, 350)

            # Draw time remaining
            time_elapsed = time.time() - self.start_time
            time_remaining = max(0, self.time_limit - time_elapsed)
            self.draw_text(f"Time Remaining: {int(time_remaining)}s", 50, self.screen.get_height() - 100)

        # Draw progress and errors
        self.draw_text(f"Correct: {self.total_correct}/{self.required_correct}", 50, self.screen.get_height() - 50)
        self.draw_text(f"Incorrect: {self.total_incorrect}/{self.max_incorrect}", 300, self.screen.get_height() - 50)

        # Draw message if recent
        if self.message and time.time() - self.message_time < 2:  # Show message for 2 seconds
            self.draw_text(self.message, self.screen.get_width()//2 - 50, self.screen.get_height()//2)

        # Draw game over message if finished
        if self.finished:
            if self.success:
                self.draw_text("Success! Well done!", self.screen.get_width()//2 - 100, self.screen.get_height()//2)
            else:
                if time.time() - self.start_time >= self.time_limit:
                    self.draw_text("Time's up! Game Over!", self.screen.get_width()//2 - 100, self.screen.get_height()//2)
                else:
                    self.draw_text("Too many errors! Game Over!", self.screen.get_width()//2 - 100, self.screen.get_height()//2)

    def draw_text(self, text, x, y):
        text_surface = self.font.render(text, True, (255, 255, 255))
        self.screen.blit(text_surface, (x, y))

    def is_finished(self):
        return self.finished

    def is_successful(self):
        return self.success

    def generate_email(self):
        email_types = [
            {
                "subject": "Spam Advertisement",
                "content": "CONGRATULATIONS! You've won a free vacation!",
                "correct_action": "DELETE",
                "options": ["REPLY", "FORWARD", "DELETE"]  # Randomize this order
            },
            {
                "subject": "Client Meeting Request",
                "content": "Can we schedule a meeting to discuss the project?",
                "correct_action": "REPLY",
                "options": ["DELETE", "REPLY", "FORWARD"]  # Different random order
            },
            {
                "subject": "IT Department Update",
                "content": "Please forward this security update to your team.",
                "correct_action": "FORWARD",
                "options": ["FORWARD", "DELETE", "REPLY"]  # Another random order
            }
        ]
        
        email = random.choice(email_types)
        # Randomize the order of options for each email
        random.shuffle(email["options"])
        return email
