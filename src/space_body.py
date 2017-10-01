import math
import numpy as np


class SpaceBody:
    player = None
    space_bodies = []

    def __init__(self, x, y):
        self.image = None
        SpaceBody.space_bodies.append(self)

        self.x = x
        self.y = y
        self.t = 0

    def update(self, dt):
        pass

    def get_screen_pos(self, player, scale, width, height):

        return ((self.x * scale - self.image.get_rect().width / 2 + width / 2,
                 -self.y * scale - self.image.get_rect().height / 2 + height / 2),
                self.t)