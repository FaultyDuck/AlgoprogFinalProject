import os
import pygame as py

py.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800

screen = py.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

dt = 0

clock=py.time.Clock()

player_pos = py.Vector2(screen.get_width() / 2, screen.get_height() /2)

run = True
while run:

    screen.fill((0, 0, 0))

    py.draw.circle(screen,'blue',player_pos,10)

    keys=py.key.get_pressed()
    if keys[py.K_w]:
        player_pos.y -= 200 * dt
        if player_pos.y < 40:
            player_pos.y = 40
    if keys[py.K_a]:
        player_pos.x -= 200 * dt
        if player_pos.x < 40:
            player_pos.x = 40
    if keys[py.K_s]:
        player_pos.y += 200 * dt
        if player_pos.y > 680:
            player_pos.y = 680
    if keys[py.K_d]:
        player_pos.x += 200 * dt
        if player_pos.x > 1160:
            player_pos.x = 1160

    for event in py.event.get():
        if event.type == py.QUIT:
            run = False

    py.display.update()
    dt=clock.tick()/1000

py.quit()