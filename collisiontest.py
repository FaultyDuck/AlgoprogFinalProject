import pygame as py
import random

py.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

screen = py.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
py.display.set_caption("Collision Testing")

rect1 = py.Rect(0, 0, 25, 25)

obstacles = []
for _ in range(16):
    obstacle_rect = py.Rect(random.randint(0, 500), random.randint(0, 300), 25, 25)
    obstacles.append(obstacle_rect)

BG = ('#212427')
GREEN = (0, 240, 0)
RED = (240, 0, 0)
BLUE = (0, 0, 240)

#Hide mouse cursor
py.mouse.set_visible(False)

run = True
while run:
    screen.fill(BG)

    #If statement to detect collision between two rectangles
    col = GREEN
    for obstacle in obstacles:
        if rect1.colliderect(obstacle):
            col = RED

    #if rect1.collidelist(obstacles) >= 0:
        #print(rect1.collidelist(obstacles))
        #col = RED

        #print the number that collided with in the list, different way of detecting collisions in a list without for loop

    pos = py.mouse.get_pos()
    rect1.center = pos

    py.draw.rect(screen, col, rect1)
    for obstacle in obstacles:
        py.draw.rect(screen, BLUE, obstacle)

    for event in py.event.get():
        if event.type == py.QUIT:
            run = False

    py.display.flip()

py.quit()