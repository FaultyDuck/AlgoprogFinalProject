import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Objects with Red Color and Their Masks")

# Define colors
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# Function to create a surface with a red object and generate a mask
def create_red_object(x, y, width, height):
    # Create the surface
    surface = pygame.Surface((width, height))
    
    # Fill the surface with red color
    surface.fill(RED)
    
    # Generate a mask for the surface
    mask = pygame.mask.from_surface(surface)
    
    return surface, mask, (x, y)

# Create a few red objects with their masks
red_rect_surface, red_rect_mask, red_rect_position = create_red_object(100, 100, 50, 50)
red_circle_surface, red_circle_mask, red_circle_position = create_red_object(300, 200, 80, 80)

# Main game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the screen with white
    screen.fill(WHITE)

    # Draw the red objects
    screen.blit(red_rect_surface, red_rect_position)
    screen.blit(red_circle_surface, red_circle_position)

    # Example: Check the mask of the red rectangle
    if red_rect_mask.get_at((25, 25)):  # Check if the point (25, 25) is in the mask (should be red)
        print("Red rectangle mask has non-transparent pixel at (25, 25)")

    # Example: Check the mask of the red circle
    if red_circle_mask.get_at((40, 40)):  # Check if the point (40, 40) is in the mask (should be red)
        print("Red circle mask has non-transparent pixel at (40, 40)")

    # Update the display
    pygame.display.flip()

    # Control the frame rate
    pygame.time.Clock().tick(60)

# Quit Pygame
pygame.quit()
sys.exit()
