import pygame as py
import os

py.init()

# Define screen size
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Create game window
screen = py.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
py.display.set_caption("Masks")

# Define colors
BG = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

# Hide mouse cursor
py.mouse.set_visible(False)

# Load ship images
SHIP_DIR = 'ship'
if not os.path.exists(SHIP_DIR):
    print(f"Directory '{SHIP_DIR}' not found.")
    py.quit()
    exit()

# Filter valid image files
valid_extensions = {".png", ".jpg", ".jpeg", ".bmp"}
ship_images = [img for img in os.listdir(SHIP_DIR) if os.path.splitext(img)[1].lower() in valid_extensions]

# Load images and handle errors
SHIP = []
for img in ship_images:
    try:
        image = py.image.load(os.path.join(SHIP_DIR, img))
        SHIP.append(image)
    except py.error as e:
        print(f"Failed to load image {img}: {e}")

if not SHIP:
    print("No valid images found in the 'ship' directory.")
    py.quit()
    exit()

# Generate masks for images
SHIPMASK = [py.mask.from_surface(image) for image in SHIP]

# Function to convert masks to drawable surfaces
def mask_to_surface(mask, color=(255, 255, 255)):
    size = mask.get_size()
    surface = py.Surface(size, py.SRCALPHA)  # Create a transparent surface
    surface.fill((0, 0, 0, 0))  # Ensure it starts fully transparent

    # Set the mask pixels to the specified color
    for x in range(size[0]):
        for y in range(size[1]):
            if mask.get_at((x, y)):  # If the pixel is part of the mask
                surface.set_at((x, y), color)
    return surface

# Convert masks to surfaces
SURFMASK = [mask_to_surface(mask, color=(255, 0, 0)) for mask in SHIPMASK]

# Example positions
positions = [(100, 100), (200, 200)]

# Game loop
run = True
while run:
    # Update background
    screen.fill(BG)

    # Draw masks to the screen
    for i, surface in enumerate(SURFMASK):
        if i < len(positions):  # Ensure we don't exceed the number of positions
            screen.blit(surface, positions[i])

    # Event handler
    for event in py.event.get():
        if event.type == py.QUIT:
            run = False

    # Update display
    py.display.flip()

py.quit()
