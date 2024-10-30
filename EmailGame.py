import pygame
import random
from Relationships import RelationshipGraph  # Assuming this is the file name

# Initialize Pygame and RelationshipGraph
pygame.init()
relationship_graph = RelationshipGraph()

# Screen setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Email Review Game")

# Font setup
FONT = pygame.font.Font(None, 32)

# Email data with 50 samples
emails = [
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

# Shuffle and pick 10 random emails for the game
random.shuffle(emails)
game_emails = emails[:10]

# Game variables
current_email_index = 0
correct_choices = 0
total_emails = len(game_emails)
game_over = False

# Text drawing helper
def draw_text(text, x, y):
    label = FONT.render(text, True, (0, 0, 0))
    screen.blit(label, (x, y))

# Function to evaluate performance at the end of the game
def evaluate_performance():
    if correct_choices >= 8:
        relationship_graph.increase_relationship("player", "boss", 10)
        print("Boss happiness increased due to good performance!")
    else:
        relationship_graph.decrease_relationship("player", "boss", 10)
        print("Boss happiness decreased due to poor performance!")
    relationship_graph.check_thresholds()

# Game loop
running = True
while running:
    screen.fill((255, 255, 255))

    # Check if game is over
    if current_email_index >= total_emails:
        draw_text(f"Game Over! Correct Choices: {correct_choices} out of {total_emails}", 200, 300)
        pygame.display.flip()
        pygame.time.wait(3000)
        evaluate_performance()  # Evaluate performance at the end
        running = False
        continue

    # Get current email
    email = game_emails[current_email_index]

    # Display email content
    draw_text(f"Subject: {email['subject']}", 50, 50)
    draw_text(f"Content: {email['content']}", 50, 100)
    draw_text("Choose an action: [1] Reply [2] Forward [3] Delete", 50, 200)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1 and email["action"] == "reply":
                # Show reply options
                draw_text(f"Reply Options: [A] {email['reply_options'][0]} [B] {email['reply_options'][1]}", 50, 250)
                pygame.display.flip()

                # Wait for user to choose reply option
                waiting_for_reply = True
                while waiting_for_reply:
                    for reply_event in pygame.event.get():
                        if reply_event.type == pygame.KEYDOWN:
                            if reply_event.key in [pygame.K_a, pygame.K_b]:
                                selected_reply = 0 if reply_event.key == pygame.K_a else 1
                                if selected_reply == email["correct_reply"]:
                                    draw_text("Correct Reply!", 50, 300)
                                    correct_choices += 1
                                else:
                                    draw_text("Incorrect Reply.", 50, 300)
                                current_email_index += 1
                                waiting_for_reply = False
                            elif reply_event.key == pygame.K_ESCAPE:
                                waiting_for_reply = False

            elif event.key == pygame.K_2 and email["action"] == "forward":
                if email["action"] == "forward":
                    draw_text("Correct! Email forwarded.", 50, 250)
                    correct_choices += 1
                    current_email_index += 1
                else:
                    draw_text("Incorrect choice.", 50, 250)
                    current_email_index += 1

            elif event.key == pygame.K_3 and email["action"] == "delete":
                if email["action"] == "delete":
                    draw_text("Correct! Email deleted.", 50, 250)
                    correct_choices += 1
                    current_email_index += 1
                else:
                    draw_text("Incorrect choice.", 50, 250)
                    current_email_index += 1

            else:
                draw_text("Incorrect choice. Try again.", 50, 250)
                current_email_index += 1

            pygame.display.flip()
            pygame.time.wait(1000)  # Pause before moving to the next email

    pygame.display.flip()

pygame.quit()
