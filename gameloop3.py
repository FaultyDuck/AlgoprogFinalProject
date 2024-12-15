import pygame
import sys
import math
from pygame.locals import QUIT

# Initialize Pygame
pygame.init()

# Screen dimensions and settings
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Controlled Spawning and Moving Circles")

# Colors
WHITE = (255, 255, 255)
RED = (255, 50, 50)

# Circle class
class Circle:
    def __init__(self, x, y, radius, direction, speed):
        self.x = x
        self.y = y
        self.radius = radius
        self.direction = direction  # A tuple for movement (dx, dy)
        self.speed = speed
        self.split = False

    def move(self):
        # Move in the specified direction
        self.x += self.direction[0] * self.speed
        self.y += self.direction[1] * self.speed

        # Stop moving when it reaches the center
        if (
            (self.direction[0] != 0 and abs(self.x - SCREEN_WIDTH // 2) <= self.speed)
            or (self.direction[1] != 0 and abs(self.y - SCREEN_HEIGHT // 2) <= self.speed)
        ):
            self.x, self.y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
            self.split = True  # Mark the circle for splitting

    def draw(self, surface):
        pygame.draw.circle(surface, RED, (int(self.x), int(self.y)), self.radius)

# Mini circle class
class MiniCircle:
    def __init__(self, x, y, radius, angle, speed):
        self.x = x
        self.y = y
        self.radius = radius
        self.angle = angle  # Angle in radians for movement direction
        self.speed = speed

    def update(self):
        # Move based on the angle
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed

    def draw(self, surface):
        pygame.draw.circle(surface, RED, (int(self.x), int(self.y)), self.radius)

# Game clock and settings
clock = pygame.time.Clock()
FPS = 60

# Timer variables
SPAWN_INTERVAL = 2000  # 2 seconds
STOP_SPAWN_AFTER = 20000  # 20 seconds in milliseconds
RESUME_SPAWN_AFTER = 50000  # 50 seconds in milliseconds (20 + 30 seconds)
start_time = pygame.time.get_ticks()

# Game object lists
circles = []
mini_circles = []

# Main game loop
running = True
while running:
    # Clear the screen
    screen.fill(WHITE)

    # Current time
    current_time = pygame.time.get_ticks()
    elapsed_time = current_time - start_time

    # Stop spawning after 20 seconds and resume after 50 seconds
    spawning_enabled = elapsed_time < STOP_SPAWN_AFTER or elapsed_time >= RESUME_SPAWN_AFTER

    # Event handling
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    # Spawn a new circle every 2000 milliseconds if spawning is enabled
    if spawning_enabled and elapsed_time % SPAWN_INTERVAL < 16:
        # Define the starting position and direction of the big circle
        start_x, start_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT  # From the bottom
        direction = (0, -1)  # Moving up (-1 in the y-direction)
        speed = 5  # Adjust speed here
        new_circle = Circle(start_x, start_y, 40, direction, speed)
        circles.append(new_circle)

    # Update and draw main circles
    for circle in circles[:]:
        if not circle.split:
            circle.move()
            circle.draw(screen)
        else:
            # Split into 16 mini circles
            angle_step = 2 * math.pi / 16  # Divide 360° into 16 parts
            for i in range(16):
                angle = i * angle_step
                new_mini_circle = MiniCircle(circle.x, circle.y, 10, angle, 5)
                mini_circles.append(new_mini_circle)
            circles.remove(circle)

    # Update and draw mini circles
    for mini_circle in mini_circles[:]:
        mini_circle.update()
        mini_circle.draw(screen)

        # Remove mini circles once they move off-screen
        if (
            mini_circle.x < 0
            or mini_circle.x > SCREEN_WIDTH
            or mini_circle.y < 0
            or mini_circle.y > SCREEN_HEIGHT
        ):
            mini_circles.remove(mini_circle)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

# Quit Pygame
pygame.quit()
sys.exit()
