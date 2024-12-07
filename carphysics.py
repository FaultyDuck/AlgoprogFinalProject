import pygame as py
import time
import math
from carutil import scale_image, blit_rotate_center

GRASS = scale_image(py.image.load("grass.jpg"), 2.5)
TRACK = scale_image(py.image.load("track.png"), 0.9)

TRACK_BORDER = scale_image(py.image.load("track-border.png"), 0.9)

RED_CAR = scale_image(py.image.load("red-car.png"), 0.55)
GREEN_CAR = scale_image(py.image.load("green-car.png"), 0.55)

#SCREEN_WIDTH = 1000
#SCREEN_HEIGHT = 600

WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()

#WIN = py.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
WIN = py.display.set_mode((WIDTH, HEIGHT))
py.display.set_caption('Car Physics 50 Min Tutorial')


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
        blit_rotate_center(win, self.img, (self.x, self.y), self.angle)

    def move_forward(self):
        self.vel = min(self.vel + self.acceleration, self.max_vel)
        self.move()
        
    def move(self):
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel

        self.y -= vertical
        self.x -= horizontal

    def reduce_speed(self):
        self.vel = max(self.vel - self.acceleration / 2, 0)
        self.move()
        
class PlayerCar(AllCar):
    IMG = RED_CAR
    START_POS = (180, 200)


def draw(win, images, player_car):
    for img, pos in images:
        win.blit(img, pos)

    player_car.draw(win)
    py.display.update()

FPS = 60

run = True
clock = py.time.Clock()
images = [(GRASS, (0, 0)), (TRACK, (0, 0))]
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

    if not moved:
        player_car.reduce_speed()

py.quit()