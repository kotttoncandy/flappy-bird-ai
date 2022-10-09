from random import randint
import pygame

class Pipe():
    def __init__(self, y):
        self.rect = pygame.Rect(630, y, 80, 1000)

    def update(self, delta):
        self.rect.left -= 300 * delta