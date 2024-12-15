import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Delayed and Interval Box Spawning")

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# Box class
class Box:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.color = BLUE
        self.width = 20
        self.height = 90

    def move(self):
        self.y += 5  # Move the box downward
        if self.y > SCREEN_HEIGHT:
            self.y = -self.size  # Reset position to top when it moves off-screen

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))

# Game clock and settings
clock = pygame.time.Clock()
FPS = 60

# Timer variables
INITIAL_DELAY = 15000  # 15 seconds in milliseconds
SPAWN_INTERVAL = 800   # 800 milliseconds
start_time = pygame.time.get_ticks()  # Record the program's start time
last_spawn_time = None  # To track the last box spawn time

# List to hold all boxes
boxes = []

# Main game loop
running = True
while running:
    # Clear the screen
    screen.fill(WHITE)

    # Check the current time
    current_time = pygame.time.get_ticks()

    # Check if the initial delay has passed
    if current_time - start_time >= INITIAL_DELAY:
        # Begin spawning at intervals of 800 milliseconds
        if last_spawn_time is None or current_time - last_spawn_time >= SPAWN_INTERVAL:
            # Spawn a box at a random horizontal position
            x = random.randint(0, SCREEN_WIDTH - 50)
            new_box = Box(x, -50, 50)  # Start slightly above the screen
            boxes.append(new_box)

            # Update the last spawn time
            last_spawn_time = current_time

    # Update and draw all boxes
    for box in boxes:
        box.move()
        box.draw(screen)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

# Quit Pygame
pygame.quit()
sys.exit()
