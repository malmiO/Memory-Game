import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Memory Game")

# Colors
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED = (200, 0, 0)

# Fonts
title_font = pygame.font.Font(None, 50)
instr_font = pygame.font.Font(None, 30)

# Game clock
clock = pygame.time.Clock()

# Cards setup
cards = ['A', 'A', 'B', 'B', 'C', 'C', 'D', 'D']
random.shuffle(cards)
revealed = [False] * len(cards)

# Card positions (4x2 grid)
card_rects = []
card_width = WIDTH // 4
card_height = HEIGHT // 2

for row in range(2):
    for col in range(4):
        rect = pygame.Rect(col * card_width, row * card_height, card_width, card_height)
        card_rects.append(rect)

# Welcome screen
def show_welcome_screen():
    screen.fill(WHITE)
    
    # Title
    title_text = title_font.render("Welcome to Memory Game!", True, BLACK)
    title_rect = title_text.get_rect(center=(WIDTH//2, HEIGHT//4))
    screen.blit(title_text, title_rect)
    
    # Instructions
    instructions = [
        "Click on two cards to find a match.",
        "If they match, they stay revealed.",
        "Try to match all pairs in the fewest attempts!",
        "Press any key or click to start..."
    ]
    
    for i, line in enumerate(instructions):
        instr_text = instr_font.render(line, True, BLACK)
        instr_rect = instr_text.get_rect(center=(WIDTH//2, HEIGHT//2 + i*40))
        screen.blit(instr_text, instr_rect)
    
    pygame.display.flip()
    
    # Wait for any key press or mouse click
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False

# Draw the game board
def draw_board():
    screen.fill(WHITE)
    for i, rect in enumerate(card_rects):
        if revealed[i]:
            pygame.draw.rect(screen, GREEN, rect)
            text = title_font.render(cards[i], True, BLACK)
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)
        else:
            pygame.draw.rect(screen, GRAY, rect)
    pygame.display.flip()

# Show welcome screen before starting
show_welcome_screen()

# Game variables
first_choice = None
second_choice = None
matches_found = 0
attempts = 0
total_matches = len(cards) // 2
waiting = False
wait_time = 0

# Main game loop
running = True
while running:
    draw_board()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and not waiting:
            pos = pygame.mouse.get_pos()
            for i, rect in enumerate(card_rects):
                if rect.collidepoint(pos) and not revealed[i]:
                    if first_choice is None:
                        first_choice = i
                        revealed[i] = True
                    elif second_choice is None and i != first_choice:
                        second_choice = i
                        revealed[i] = True
                        attempts += 1
                        waiting = True
                        wait_time = pygame.time.get_ticks()

    # Check for match after short delay
    if waiting:
        if pygame.time.get_ticks() - wait_time > 1000:  # 1 second delay
            if cards[first_choice] == cards[second_choice]:
                matches_found += 1
            else:
                revealed[first_choice] = False
                revealed[second_choice] = False
            first_choice = None
            second_choice = None
            waiting = False

    # Game won screen
    if matches_found == total_matches:
        screen.fill(WHITE)
        text = title_font.render(f"You won in {attempts} attempts!", True, RED)
        text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2))
        screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.wait(3000)
        running = False

    clock.tick(30)
