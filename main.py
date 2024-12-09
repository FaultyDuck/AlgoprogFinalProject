import pygame as py
import time
import os
import math
from carutil import scale_image, stack

BACKGROUND = scale_image(py.image.load("star.jpg"), 2)

SHIP = [py.image.load('ship/' + img) for img in os.listdir('ship')]

WIDTH, HEIGHT = BACKGROUND.get_width(), BACKGROUND.get_height()

WIN = py.display.set_mode((WIDTH, HEIGHT))
py.display.set_caption('Maingame')

class AllCar:
    def __init__(self, max_vel, rotation_vel):
        self.max_vel = max_vel
        self.vel = 0
        self.rotation_vel = rotation_vel
        self.angle = 0
        self.img = self.IMG
        self.x, self.y = self.START_POS
        self.acceleration = 0.1
    
    def rotate(self, left=False, right=False):
        if left:
            self.angle += self.rotation_vel
        elif right:
            self.angle -= self.rotation_vel

    def draw(self, win):
        stack(win, self.img, (self.x, self.y), self.angle)

    def move_forward(self):
        self.vel = min(self.vel + self.acceleration, self.max_vel)
        self.move()

    def move_backward(self):
        self.vel = max(self.vel - self.acceleration, -self.max_vel/1.5)
        self.move()
        
    def move(self):
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel

        self.y -= vertical
        self.x -= horizontal

class PlayerCar(AllCar):
    IMG = SHIP
    START_POS = (WIDTH/2, HEIGHT/2)

    def reduce_speed(self):
        self.vel = max(self.vel - self.acceleration / 2, 0)
        self.move()


def draw(win, images, player_car):
    for img, pos in images:
        win.blit(img, pos)

    player_car.draw(win)
    py.display.update()

FPS = 60

run = True
clock = py.time.Clock()
images = [(BACKGROUND, (0, 0))]
player_car = PlayerCar(4, 4)

while run:
    clock.tick(FPS)

    draw(WIN, images, player_car)

    for event in py.event.get():
        if event.type == py.QUIT:
            run = False

    keys = py.key.get_pressed()
    moved = False

    if keys[py.K_a]:
        player_car.rotate(left = True)
    if keys[py.K_d]:
        player_car.rotate(right = True)
    if keys[py.K_w]:
        moved = True
        player_car.move_forward()
    if keys[py.K_s]:
        moved = True
        player_car.move_backward()

    if not moved:
        player_car.reduce_speed()

py.quit()