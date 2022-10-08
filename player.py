import pygame
from timer import RepeatedTimer

class Player():
    def __init__(self):
        self.rect = pygame.Rect(250,100, 25, 25)
        self.jumping = False
        self.fitness = 0
        def timed():
            self.jumping = False
        self.jump_timer = RepeatedTimer(0.3, timed, False)

    def jump(self):
        self.jumping = True
        self.jump_timer.start()