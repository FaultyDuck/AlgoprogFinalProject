import pygame as py
import os
import sys
from pygame import mixer
from timer import Timer

py.init()

mixer.init()
mixer.music.load("flight.mp3")
mixer.music.set_volume(0.3)
mixer.music.play()

#define screen size
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

#create game window
screen = py.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
py.display.set_caption("Music")

# timer_event = py.event.custom_type()
# py.time.set_timer(timer_event, 687)

BG = (0, 0, 0)
display_surface = py.display.set_mode((1280, 720))
clock = py.time.Clock()
font = py.font.Font(None, 50)

simple_timer = Timer(1000)
simple_timer.activate()

#game loop
run = True
while run:

  dt = clock.tick() / 1000

  #update background
  screen.fill(BG)

  #event handler
  for event in py.event.get():
    if event.type == py.QUIT:
      run = False

    # if event.type == timer_event:
    #   print('Tock')

  simple_timer.update()
  if not simple_timer.active:
    text_surf = font.render('1 second has passed', False, 'White')
    display_surface.blit(text_surf, (0,0))

  #update display
  py.display.update()

py.quit()