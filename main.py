import pygame as py
import time
import os
import math
import sys
from pygame import mixer
from carutil import *
import random

py.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
BLUE = (50, 150, 255)

BACKGROUND = scale_image(py.image.load("star.jpg"), 2)

SHIP = [py.image.load('ship/' + img) for img in os.listdir('ship')]

WIDTH, HEIGHT = BACKGROUND.get_width(), BACKGROUND.get_height()

WIN = py.display.set_mode((WIDTH, HEIGHT))
py.display.set_caption('Maingame')

font = py.font.Font(None, 74)
button_font = py.font.Font(None, 50)

#temp
#obstacles = []
#for _ in range(16):
#    obstacle_rect = py.Rect(random.randint(0, 500), random.randint(0, 300), 25, 25)
#    obstacles.append(obstacle_rect)

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

    def collide(self, mask, x=0, y=0):
        ship_mask = py.mask.from_surface(self.img)
        offset = (int(self.x - x), int(self.y - y))
        poi = mask.overlap(ship_mask, offset)
        return poi

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

def moving(player):
    keys = py.key.get_pressed()
    moved = False

    if keys[py.K_a]:
        player_car.rotate(left = True)
        #if player_car.x < 40: #YOU NEED TO CHECK THIS CONSTANTLY, OR ELSE IT WILL NOT WORK 
        #    player_car.x = 40
    if keys[py.K_d]:
        player_car.rotate(right = True)
        #if player_car.x > 1160: #ADD THIS TO THE FUNCTION FOR CONTINUE MOVEMENT AND BACKWARDS MOVEMENT TO STOP THE PLAYER FROM MOVING
        #    player_car.x = 1160
    if keys[py.K_w]:
        moved = True
        player_car.move_forward()
        #if player_car.y < 40: #OMNI MOVEMENT
        #    player_car.y = 40
    if keys[py.K_s]:
        moved = True
        player_car.move_backward()
        #if player_car.y > 680:
        #    player_car.y = 680

    if not moved:
        player_car.reduce_speed()

FPS = 60

images = [(BACKGROUND, (0, 0))]
player_car = PlayerCar(4, 4)

class Button:
    def __init__(self, x, y, width, height, text, action=None):
        self.rect = py.Rect(x, y, width, height)
        self.text = text
        self.color = GRAY
        self.action = action

    def draw(self, surface):
        py.draw.rect(surface, self.color, self.rect)
        text_draw = button_font.render(self.text, True, WHITE)
        text_rect = text_draw.get_rect(center=self.rect.center)
        surface.blit(text_draw, text_rect)

    def check_click(self, pos):
        if self.rect.collidepoint(pos) and self.action:
            self.action()

def start_game():
    start = True  # Replace with game logic
    gameclock = py.time.Clock()

    py.mouse.set_visible(False)

    mixer.init()
    mixer.music.load("flight.mp3")
    mixer.music.set_volume(0.5)
    mixer.music.play()

    while start:
        gameclock.tick(FPS)

        draw(WIN, images, player_car)
        
        for event in py.event.get():
            if event.type == py.QUIT:
                start = False
            elif event.type == py.KEYDOWN:
                if event.key == py.K_ESCAPE:
                    start = False
                    #run = True use class system to start and stop the instances

        #screen collisions
        if player_car.y < 20:
            player_car.y = 20
        if player_car.y > (HEIGHT - 20):
            player_car.y = (HEIGHT - 20)
        if player_car.x < 20:
            player_car.x = 20
        if player_car.x > (WIDTH - 20):
            player_car.x = (WIDTH - 20)
        
        moving(player_car)

        #for obstacle in obstacles:
        #    if player_car.colliderect(obstacle):
        #        py.quit()

        #for obstacle in obstacles:
        #    py.draw.rect(WIN, BLUE, obstacle)

    py.quit()
    sys.exit()
        #add pause screen later

def quit_game():
    py.quit()
    sys.exit()

buttons = [
    Button(630, 250, 200, 60, "Start Game", start_game),
    Button(630, 400, 200, 60, "Quit", quit_game),
]

def play_game():
    run = True
    clock = py.time.Clock()

    while run:
        clock.tick(FPS)

        for event in py.event.get():
            if event.type == py.QUIT:
                run = False
            elif event.type == py.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for button in buttons:
                        button.check_click(event.pos)
                    #add transfter into the second instance
        
        title_draw = font.render("Collision Drift", True, BLUE)
        title_rect = title_draw.get_rect(center=(WIDTH // 2, 100))
        WIN.blit(title_draw, title_rect)

        for button in buttons:
            button.draw(WIN)
        
        py.display.flip()

    #if player_car.collide()

    py.quit()
    sys.exit()

if __name__ == "__main__":
    play_game()

#add wall collisions #DONE
#menu music 
#pause
#enemies
#collision detection
#death animation