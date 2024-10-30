import pygame
import random
from Meter import Meter  # Import the Meter class from Meter.py

# Initialize Pygame
pygame.init()

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

# Initialize meters for salary and boss happiness
salary_meter = Meter("Salary", max_value=100, min_value=0)
boss_happiness_meter = Meter("Boss Happiness", max_value=100, min_value=0)

# Game loop
running = True
email_index = 0
score = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear screen
    screen.fill((255, 255, 255))

    # Display email subject and content
    email = game_emails[email_index]
    subject_text = FONT.render(email["subject"], True, (0, 0, 0))
    content_text = FONT.render(email["content"], True, (0, 0, 0))
    screen.blit(subject_text, (20, 20))
    screen.blit(content_text, (20, 60))

    # Display options for reply or action
    if email["action"] == "reply":
        for i, option in enumerate(email["reply_options"]):
            option_text = FONT.render(f"{i + 1}. {option}", True, (0, 0, 0))
            screen.blit(option_text, (20, 120 + i * 30))

    # Display meters
    salary_meter.draw(screen)
    boss_happiness_meter.draw(screen)

    pygame.display.flip()

    # Wait for user input (1, 2, 3, or 4)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_1] and email["action"] == "reply":
        reply_index = 0  # Assume first option is selected
    elif keys[pygame.K_2] and email["action"] == "reply":
        reply_index = 1  # Assume second option is selected
    elif email["action"] == "delete":
        reply_index = None  # Assume delete action
    elif email["action"] == "forward":
        reply_index = None  # Assume forward action

    # Evaluate the player's choice
    if email["action"] == "reply" and reply_index is not None:
        if reply_index == email["correct_reply"]:
            score += 10
            salary_meter.increase(5)  # Increase salary by 5
            boss_happiness_meter.increase(10)  # Increase boss happiness by 10
        else:
            score -= 5
            salary_meter.decrease(5)  # Decrease salary by 5
            boss_happiness_meter.decrease(10)  # Decrease boss happiness by 10
    elif email["action"] == "delete":
        score += 5
        boss_happiness_meter.increase(5)  # Increase boss happiness by 5
    elif email["action"] == "forward":
        score += 2
        boss_happiness_meter.increase(2)  # Increase boss happiness by 2

    # Move to the next email or end the game
    email_index += 1
    if email_index >= len(game_emails):
        running = False  # End game if all emails are processed

# Display final score
screen.fill((255, 255, 255))
final_score_text = FONT.render(f"Final Score: {score}", True, (0, 0, 0))
screen.blit(final_score_text, (WIDTH // 2 - final_score_text.get_width() // 2, HEIGHT // 2))
pygame.display.flip()

# Wait for a while before quitting
pygame.time.wait(3000)
pygame.quit()
