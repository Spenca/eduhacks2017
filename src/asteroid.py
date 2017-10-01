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
        matrix = np.array([[1,   0,  vx],
                           [0,   1,  vy],
                           [-vx, -vy,  1]])

        input_vec = np.array([[vx * dt],
                              [vy * dt],
                              [dt]])

        out_vec = gamma * np.dot(matrix, input_vec)

        self.x -= out_vec[0, 0]
        self.y -= out_vec[1, 0]
        self.t += out_vec[2, 0]

        gamma = 1 / math.sqrt(1 - (vx * dt) ** 2 - (vy * dt) ** 2)
        matrix1 = np.array([[1,   0,   -vx * dt],
                           [0,   1,    -vy * dt],
                           [-vx * dt, -vy * dt,  1]])

        input_vec = np.array([[self.x],
                              [self.y],
                              [self.t]])

        out_vec = gamma * np.dot(matrix1, input_vec)

        self.x = out_vec[0, 0]
        self.y = out_vec[1, 0]
        self.t = out_vec[2, 0]
