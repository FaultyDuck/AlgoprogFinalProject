import pygame
import sys
from pygame.locals import QUIT
from random import randint

# Initialize Pygame
pygame.init()

# Screen dimensions and settings
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Spawning Boxes")

# Colors
WHITE = (255, 255, 255)
BLUE = (50, 150, 255)

# Box class
class Box:
    def __init__(self, x, y, size, speed):
        self.rect = pygame.Rect(x, y, size, size)
        self.speed = speed

    def update(self):
        self.rect.y += self.speed

    def draw(self, surface):
        pygame.draw.rect(surface, BLUE, self.rect)

# Game clock and settings
clock = pygame.time.Clock()
running = True
FPS = 60

# Timer variables
SPAWN_INTERVAL = 800  # milliseconds
DURATION = 2 * 60 * 1000  # 2 minutes in milliseconds
start_time = pygame.time.get_ticks()

# Box list
boxes = []

# Main game loop
while running:
    # Clear the screen
    screen.fill(WHITE)

    # Check time
    current_time = pygame.time.get_ticks()
    elapsed_time = current_time - start_time

    if elapsed_time > DURATION:
        running = False  # End the game after 2 minutes

    # Event handling
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    # Spawn new box every 800 milliseconds
    if elapsed_time % SPAWN_INTERVAL < 16:  # Check close to the frame time
        x_position = randint(0, SCREEN_WIDTH - 50)  # Random x position
        new_box = Box(x_position, 0, 50, 5)  # Box size 50, speed 5
        boxes.append(new_box)

    # Update and draw boxes
    for box in boxes[:]:
        box.update()
        box.draw(screen)

        # Remove box if it moves off the screen
        if box.rect.top > SCREEN_HEIGHT:
            boxes.remove(box)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

# Quit Pygame
pygame.quit()
sys.exit()
