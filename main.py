import pygame as py
import time
import os
import math
import sys
from pygame import mixer
from carutil import *
import random 
from random import randint

py.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
BLUE = (50, 150, 255)
RED = (255,0,0)

BACKGROUND = scale_image(py.image.load("star.jpg"), 2)

SHIP = [py.image.load('ship/' + img) for img in os.listdir('ship')]

SHIPMASK = [py.mask.from_surface(image) for image in SHIP]

WIDTH, HEIGHT = BACKGROUND.get_width(), BACKGROUND.get_height()

WIN = py.display.set_mode((WIDTH, HEIGHT))
py.display.set_caption('Maingame')

font = py.font.Font(None, 74)
button_font = py.font.Font(None, 50)

PROD = py.Rect(20, 20, 20, 20)

#temp
#obstacles = []
#for _ in range(16):
#    obstacle_rect = py.Rect(random.randint(0, 500), random.randint(0, 300), 25, 25)
#    obstacles.append(obstacle_rect)

def mask_to_surface(mask, color=(255, 255, 255)):
    size = mask.get_size()
    surface = py.Surface(size, py.SRCALPHA)  #Create a transparent surface
    surface.fill((0, 0, 0, 0))  #Ensure it starts fully transparent

    #Set the mask pixels to the specified color
    for x in range(size[0]):
        for y in range(size[1]):
            if mask.get_at((x, y)):  #If the pixel is part of the mask
                surface.set_at((x, y), color)
    return surface

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

class Circle:
    def __init__(self, x, y, radius, speed):
        self.x = x
        self.y = y
        self.radius = radius
        self.speed = speed
        self.split = False        
        self.surface = py.Surface((2 * radius, 2 * radius), py.SRCALPHA)  # Transparent surface for the circle
        py.draw.circle(self.surface, RED, (radius, radius), radius)  # Draw the red circle on the surface
        
        # Create the mask for this circle (based on its surface)
        self.mask = py.mask.from_surface(self.surface)

    def move_to_center(self):
        if self.y > HEIGHT // 2:
            self.y -= self.speed
        else:
            self.split = True  #Mark the circle for splitting

    def draw(self, surface):
        py.draw.circle(surface, RED, (int(self.x), int(self.y)), self.radius)

    def check_collisions(self, masks_list):
        # Iterate through the list of masks and check for overlap with each mask
        for other_mask_obj in masks_list:
            # Unpack the x, y, and mask directly from the list (without trying to unpack mask incorrectly)
            other_x, other_y, other_mask = other_mask_obj
            
            # Calculate the offset based on positions of the two objects
            offset = (int(self.x - other_x), int(self.y - other_y))
            overlap_area = self.mask.overlap(other_mask, offset)  # Check for overlap

            # If overlap_area is not None, a collision occurred
            if overlap_area:
                print("Collision detected!")
                return True
        return False
    
class MiniCircle:
    def __init__(self, x, y, radius, angle, speed):
        self.x = x
        self.y = y
        self.radius = radius
        self.angle = angle  # Angle in radians for movement direction
        self.speed = speed
        self.surface = py.Surface((2 * radius, 2 * radius), py.SRCALPHA)  # Transparent surface for the circle
        py.draw.circle(self.surface, RED, (radius, radius), radius)  # Draw the red circle on the surface
        
        # Create the mask for this mini circle (based on its surface)
        self.mask = py.mask.from_surface(self.surface)

    def update(self):
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed

    def draw(self, surface):
        py.draw.circle(surface, RED, (int(self.x), int(self.y)), self.radius)

    def check_collisions(self, masks_list):
        # Iterate through the list of masks and check for overlap with each mask
        for other_mask_obj in masks_list:
            # Unpack the x, y, and mask directly from the list (without trying to unpack mask incorrectly)
            other_x, other_y, other_mask = other_mask_obj
            
            # Calculate the offset based on positions of the two objects
            offset = (int(self.x - other_x), int(self.y - other_y))
            overlap_area = self.mask.overlap(other_mask, offset)  # Check for overlap

            # If overlap_area is not None, a collision occurred
            if overlap_area:
                print("Collision detected!")
                return True
        return False

class Box:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.color = RED
        self.width = 20
        self.height = 90
        self.surface = py.Surface((self.width, self.height), py.SRCALPHA)  # Transparent surface for the box
        py.draw.rect(self.surface, self.color, (0, 0, self.width, self.height))  # Draw the red box on the surface
        
        # Create the mask for this box (based on its surface)
        self.mask = py.mask.from_surface(self.surface)

    def move(self):
        self.y += 5  #Move the box downward
        if self.y > HEIGHT:
            self.y = -self.size  #Reset position to top when it moves off-screen

    def draw(self, surface):
        py.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))

    def check_collisions(self, masks_list):
        # Iterate through the list of masks and check for overlap with each mask
        for other_mask_obj in masks_list:
            # Unpack the x, y, and mask directly from the list (without trying to unpack mask incorrectly)
            other_x, other_y, other_mask = other_mask_obj
            
            # Calculate the offset based on positions of the two objects
            offset = (int(self.x - other_x), int(self.y - other_y))
            overlap_area = self.mask.overlap(other_mask, offset)  # Check for overlap

            # If overlap_area is not None, a collision occurred
            if overlap_area:
                print("Collision detected!")
                return True
        return False

class ExpandingLine:
    def __init__(self, x, y, max_width, height, expand_speed):
        self.x = x 
        self.y = y 
        self.width = 0  # nitial width
        self.height = height  #Fixed height (entire screen)
        self.max_width = max_width  #Maximum width
        self.expand_speed = expand_speed  #Speed of expansion
        # Create a transparent surface for the expanding line
        self.surface = py.Surface((self.max_width, self.height), py.SRCALPHA)
        py.draw.rect(self.surface, RED, (0, 0, self.max_width, self.height))  # Draw the red line
        
        # Create the mask for this expanding line (based on its surface)
        self.mask = py.mask.from_surface(self.surface)

    def update(self):
        if self.width < self.max_width:
            self.width += self.expand_speed

    def draw(self, surface):
        py.draw.rect(
            surface, RED, py.Rect(self.x - self.width // 2, self.y - self.height // 2, self.width, self.height))

    def is_expanded(self):
        return self.width >= self.max_width

    def check_collisions(self, masks_list):
        # Iterate through the list of masks and check for overlap with each mask
        for other_mask_obj in masks_list:
            # Unpack the x, y, and mask directly from the list (without trying to unpack mask incorrectly)
            other_x, other_y, other_mask = other_mask_obj
            
            # Calculate the offset based on positions of the two objects
            offset = (int(self.x - other_x), int(self.y - other_y))
            overlap_area = self.mask.overlap(other_mask, offset)  # Check for overlap

            # If overlap_area is not None, a collision occurred
            if overlap_area:
                print("Collision detected!")
                return True
        return False

SPAWN_INTERVAL_BOX = 1000
SPAWN_DELAY_BOX = 30000
STOP_SPAWN_BOX = 50000
DELETE_ALL_BOXES_TIME = 60000

SPAWN_INTERVAL_CIRCLE = 2000
STOP_SPAWN_CIRCLE = 20000
RESUME_SPAWN_CIRCLE = 50000

SPAWN_INTERVAL_LINE = 5000
STOP_SPAWN_LINE = 0
RESUME_SPAWN_LINE = 90000
FPS = 60

SURFMASK = [mask_to_surface(mask, color=(255,255,255)) for mask in SHIPMASK]

images = [(BACKGROUND, (0, 0))]
player_car = PlayerCar(4, 4)

circles = []
mini_circles = []
boxes = []
lines = []

BAR_WIDTH = 600
BAR_HEIGHT = 30
BAR_X = (WIDTH - BAR_WIDTH) // 2
BAR_Y = 40
DURATION = 120000

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

# def is_mask_touching_red(mask, surface):
#     for x in range(WIDTH):
#         for y in range(HEIGHT):
#             if surface.get_at((x, y)) == RED:  # Check if the pixel is red
#                 if mask.get_at((x, y)):  # Check if the mask is also present at this point
#                     return True  # Mask is touching the red color
#     return False  # No overlap with red

# def check_masks_collide_with_red(masks, red_mask):
#     for mask in masks:
#         # Try to find the overlap between the player mask and red mask
#         offset = (mask.get_offset()[0], mask.get_offset()[1])  # Get the offset of the mask
#         if mask.overlap(red_mask, offset):  # Check for overlap between masks
#             return True  # If overlap is found, return True
#     return False  # No collision found

start_time = py.time.get_ticks()

def start_game():
    start = True
    gameclock = py.time.Clock()

    last_spawn_time = None

    py.mouse.set_visible(False)

    mixer.init()
    mixer.music.load("flight.mp3")
    mixer.music.set_volume(0.1)
    mixer.music.play()

    positions = [(player_car.x, player_car.y)]

    while start:

        draw(WIN, images, player_car)

        current_time = py.time.get_ticks()
        elapsed_time = current_time - start_time

        spawning_enabled = elapsed_time < STOP_SPAWN_CIRCLE or elapsed_time >= RESUME_SPAWN_CIRCLE
        spawning_enabled_line = elapsed_time < STOP_SPAWN_LINE or elapsed_time >= RESUME_SPAWN_LINE

        if elapsed_time >= DURATION:
            start = False

        progress = min(elapsed_time / DURATION, 1)

        py.draw.rect(WIN, WHITE, (BAR_X, BAR_Y, BAR_WIDTH, BAR_HEIGHT), 2)

        filled_width = int(progress * BAR_WIDTH)
        py.draw.rect(WIN, BLUE, (BAR_X, BAR_Y, filled_width, BAR_HEIGHT))

        # if is_mask_touching_red(SURFMASK):
        #     start = False

        # if check_masks_collide_with_red(SURFMASK, RED):
        #     start = False
        
        if spawning_enabled and elapsed_time % SPAWN_INTERVAL_CIRCLE < 16:
            new_circle = Circle(WIDTH // 2, HEIGHT, 40, 5)
            circles.append(new_circle)
            if new_circle.check_collisions(SHIPMASK):
                start = False

        for circle in circles[:]:
            if not circle.split:
                circle.move_to_center()
                circle.draw(WIN)
            else:
                #Split into 16 mini circles
                angle_step = 2 * math.pi / 16  #Divide 360° into 16 parts
                for i in range(16):
                    angle = i * angle_step
                    new_mini_circle = MiniCircle(circle.x, circle.y, 10, angle, 5)
                    mini_circles.append(new_mini_circle)
                    if new_mini_circle.check_collisions(SHIPMASK):
                        start = False
                circles.remove(circle)

        #Update and draw mini circles
        for mini_circle in mini_circles[:]:
            mini_circle.update()
            mini_circle.draw(WIN)

            #Remove mini circles once they move off-screen
            if (
                mini_circle.x < 0
                or mini_circle.x > WIDTH
                or mini_circle.y < 0
                or mini_circle.y > HEIGHT
            ):
                mini_circles.remove(mini_circle)

        if SPAWN_DELAY_BOX <= current_time - start_time < STOP_SPAWN_BOX:
            if last_spawn_time is None or current_time - last_spawn_time >= SPAWN_INTERVAL_BOX:
                #Spawn a box at a random horizontal position
                x = random.randint(0, WIDTH - 50)
                new_box = Box(x, -50, 50)  #Start slightly above the screen
                boxes.append(new_box)

                #Update the last spawn time
                last_spawn_time = current_time

                if new_box.check_collisions(SHIPMASK):
                    start = False

        if current_time - start_time >= DELETE_ALL_BOXES_TIME:
            boxes.clear()

        #Update and draw all boxes
        for box in boxes:
            box.move()
            box.draw(WIN)

            if box.y > HEIGHT:
                boxes.remove(box)

        random_x = random.randint(0, WIDTH)

        if spawning_enabled_line and elapsed_time % SPAWN_INTERVAL_LINE < 16:  #Check close to the frame time
            new_line = ExpandingLine(
            x=random_x,
            y=HEIGHT // 2,
            max_width=WIDTH // 5,
            height=HEIGHT,       
            expand_speed=8             
        )
            if new_line.check_collisions(SHIPMASK):
                start = False
            lines.append(new_line)

        #Update and draw lines
        for line in lines[:]:
            line.update()
            line.draw(WIN)

            #Remove the line if it has fully expanded
            if line.is_expanded():
                lines.remove(line)

        py.display.flip()

        for i, surface in enumerate(SURFMASK):
            if i < len(positions):  #Ensure we don't exceed the number of positions
                WIN.blit(surface, positions[i])
        
        for event in py.event.get():
            if event.type == py.QUIT:
                start = False
            elif event.type == py.KEYDOWN:
                if event.key == py.K_ESCAPE:
                    start = False

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
        gameclock.tick(FPS)

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