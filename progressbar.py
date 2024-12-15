import pygame
import sys
from pygame.locals import QUIT

# Initialize Pygame
pygame.init()

# Screen dimensions and settings
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 200
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Song Progress Bar")

# Colors
WHITE = (255, 255, 255)
BLUE = (50, 150, 255)
BLACK = (0, 0, 0)

# Progress bar settings
BAR_WIDTH = 600
BAR_HEIGHT = 30
BAR_X = (SCREEN_WIDTH - BAR_WIDTH) // 2
BAR_Y = (SCREEN_HEIGHT - BAR_HEIGHT) // 2
SONG_DURATION = 120000  # 2 minutes in milliseconds

# Game clock and settings
clock = pygame.time.Clock()
FPS = 60

# Timer variables
start_time = pygame.time.get_ticks()

# Main game loop
running = True
while running:
    # Clear the screen
    screen.fill(WHITE)

    # Check the elapsed time
    current_time = pygame.time.get_ticks()
    elapsed_time = current_time - start_time

    if elapsed_time >= SONG_DURATION:
        running = False  # Close the program when the song ends

    # Calculate progress percentage
    progress = min(elapsed_time / SONG_DURATION, 1)

    # Draw progress bar background
    pygame.draw.rect(screen, BLACK, (BAR_X, BAR_Y, BAR_WIDTH, BAR_HEIGHT), 2)

    # Draw the filled portion of the progress bar
    filled_width = int(progress * BAR_WIDTH)
    pygame.draw.rect(screen, BLUE, (BAR_X, BAR_Y, filled_width, BAR_HEIGHT))

    # Update the display
    pygame.display.flip()

    # Event handling
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    # Cap the frame rate
    clock.tick(FPS)

# Quit Pygame
pygame.quit()
sys.exit()
