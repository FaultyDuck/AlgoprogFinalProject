import pygame as py
import os
import sys

py.init()

screen = py.display.set_mode((500, 500), 0, 32)
display = py.Surface((100,100))

images = [py.image.load('ship/' + img) for img in os.listdir('ship')]

clock = py.time.Clock()

def render_stack(surf, images, pos, rotation, spread=1):
    for i, img in enumerate(images):
        rotated_img = py.transform.rotate(img, rotation)
        surf.blit(rotated_img, (pos[0] - rotated_img.get_width() // 2, pos[1] - rotated_img.get_height() // 2 - i * spread))

frame = 0

while True:
    display.fill('#000000')

    frame += 1

    render_stack(display, images, (50, 50), frame)

    for event in py.event.get():
        if event.type == py.QUIT:
            py.quit()
            sys.exit()
        if event.type == py.KEYDOWN:
            if event.key == py.K_ESCAPE:
                py.quit()
                sys.exit()

    screen.blit(py.transform.scale(display, screen.get_size()), (0, 0))
    py.display.update()
    clock.tick(60)