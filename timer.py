import pygame as py
from pygame.time import get_ticks

class Timer:
    def __init__(self, duration):
        self.duration = duration
        self.start_time = 0
        self.active = False

    def activate(self):
        self.activate = True
        self.start_time = get_ticks()

    def deavtivate(self):
        self.active = False
        self.start_time = 0
        if self.repeat:
            self.activate

    def update(self):
        if self.active:
            current_time = get_ticks()
            if current_time - self.start_time >= self.duration:
                self.deactivate()