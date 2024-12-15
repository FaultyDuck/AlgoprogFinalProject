import pygame as py
import os

py.init()

#define screen size
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

#create game window
screen = py.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
py.display.set_caption("Masks")

#define colours
BG = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

#hide mouse cursor
py.mouse.set_visible(False)

SHIP = [py.image.load('ship/' + img) for img in os.listdir('ship')]

WIDTH= 600
HEIGHT = 600

SHIPMASK = [py.mask.from_surface(image) for image in SHIP]

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

SURFMASK = [mask_to_surface(mask, color=(255, 0, 0)) for mask in SHIPMASK]

positions = [(100, 100), (300, 200)]

#game loop
run = True
while run:

  #update background
  screen.fill(BG)

  for i, surface in enumerate(SURFMASK):
      if i < len(positions):  # Ensure we don't exceed the number of positions
          screen.blit(surface, positions[i])


  #event handler
  for event in py.event.get():
    if event.type == py.QUIT:
      run = False

  #update display
  py.display.flip()

py.quit()