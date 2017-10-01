import pygame
import numpy as np

from src.space_body import SpaceBody


class Asteroid(SpaceBody):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = pygame.image.load("assets/asteroid.png")