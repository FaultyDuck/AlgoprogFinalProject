import os
import pygame as py

py.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800

screen = py.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

dt = 0

clock=py.time.Clock()

player_pos = py.Vector2(screen.get_width() / 2, screen.get_height() /2)

rect1 = py.Rect(player_pos.x, player_pos.y, 100, 100)

run = True
while run:

    screen.fill((0, 0, 0))

    py.draw.rect(screen, '#45e1ee', rect1)

    keys=py.key.get_pressed()
    if keys[py.K_w]:
        rect1.y -= 200 * dt
        if rect1.y < 40:
            rect1.y = 40
    if keys[py.K_a]:
        rect1.x -= 200 * dt
        if rect1.x < 40:
            rect1.x = 40
    if keys[py.K_s]:
        rect1.y += 200 * dt
        #if rect1.y > 680:
           # rect1.y = 680
    if keys[py.K_d]:
        rect1.x += 200 * dt
        #if rect1.x > 1160:
            #rect1.x = 1160

    for event in py.event.get():
        if event.type == py.QUIT:
            run = False

    py.display.update()
    dt=clock.tick()/1000

py.quit()