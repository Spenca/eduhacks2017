import pygame
import numpy as np
import math

from src.game import *
from src.space_body import SpaceBody


class Asteroid(SpaceBody):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = pygame.image.load("assets/asteroid.png")

    def update(self, dt):
        vx = SpaceBody.player.vx
        vy = SpaceBody.player.vy
        vt = SpaceBody.player.vt

        gamma = 1/math.sqrt(1 - vx ** 2 - vy ** 2)
        x_prm = gamma * (vx * dt + vx * dt)
        y_prm = gamma * (vy * dt + vy * dt)
        t_prm = gamma * (-vx * vx * dt - vy * vy * dt + dt)

        self.x -= x_prm
        self.y -= y_prm
        self.t += t_prm

        gamma = 1 / math.sqrt(1 - (vx * dt) ** 2 - (vy * dt) ** 2)
        x_prm = gamma * (self.x - vx * dt * self.t)
        y_prm = gamma * (self.y - vy * dt * self.t)
        t_prm = gamma * (vx * dt * self.x + vy * dt * self.y + self.t)

        self.x = x_prm
        self.y = y_prm
        self.t = t_prm
