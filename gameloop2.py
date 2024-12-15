import pygame
import sys
from pygame.locals import QUIT

# Initialize Pygame
pygame.init()

# Screen dimensions and settings
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Horizontal Expanding Line")

# Colors
WHITE = (255, 255, 255)
BLUE = (50, 150, 255)

# Line class
class ExpandingLine:
    def __init__(self, x, y, max_width, height, expand_speed):
        self.x = x  # Center x-coordinate
        self.y = y  # Center y-coordinate
        self.width = 0  # Initial width
        self.height = height  # Fixed height (entire screen)
        self.max_width = max_width  # Maximum width
        self.expand_speed = expand_speed  # Speed of expansion

    def update(self):
        # Expand only width
        if self.width < self.max_width:
            self.width += self.expand_speed

    def draw(self, surface):
        # Draw the expanding line as a rectangle (for width effect)
        pygame.draw.rect(
            surface, 
            BLUE, 
            pygame.Rect(
                self.x - self.width // 2,  # Adjust for center alignment horizontally
                self.y - self.height // 2,  # Adjust for center alignment vertically
                self.width,  # Current width
                self.height  # Full screen height
            )
        )

    def is_expanded(self):
        return self.width >= self.max_width

# Game clock and settings
clock = pygame.time.Clock()
running = True
FPS = 60

# Timer variables
SPAWN_INTERVAL = 2000  # 2000 milliseconds (2 seconds)
DURATION = 2 * 60 * 1000  # 2 minutes in milliseconds
start_time = pygame.time.get_ticks()

# Line list
lines = []

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

    # Spawn a new line every 2000 milliseconds
    if elapsed_time % SPAWN_INTERVAL < 16:  # Check close to the frame time
        new_line = ExpandingLine(
            x=SCREEN_WIDTH // 2,
            y=SCREEN_HEIGHT // 2,
            max_width=SCREEN_WIDTH // 2,  # Expands to 50% of the screen width
            height=SCREEN_HEIGHT,        # Fixed height (full screen height)
            expand_speed=10              # Speed of expansion
        )
        lines.append(new_line)

    # Update and draw lines
    for line in lines[:]:
        line.update()
        line.draw(screen)

        # Remove the line if it has fully expanded
        if line.is_expanded():
            lines.remove(line)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

# Quit Pygame
pygame.quit()
sys.exit()
