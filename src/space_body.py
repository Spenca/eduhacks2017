import math
import numpy as np

class SpaceBody:
    space_bodies = []

    def __init__(self, x, y):
        self.image = None
        SpaceBody.space_bodies.append(self)

        self.x = x
        self.y = y
        self.t = 0
        self.vx = 0
        self.vy = 0
        self.vt = 1

    def update(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.t += self.vt * dt

        # Can't exceed speed of light
        assert abs(self.vx) <= 1
        assert abs(self.vy) <= 1

    def get_screen_pos(self, player, scale, width, height):
        gamma = 1 / math.sqrt(1 - player.vy ** 2 - player.vx ** 2)

        static_time = player.t / gamma + player.vx * self.x - player.vy * self.y

        initial_point = np.array([[self.x],
                                  [self.y],
                                  [0]])

        worldline_direction = np.array([[self.vx],
                                        [self.vy],
                                        [1]])

        xyt = initial_point + worldline_direction * static_time

        matrix = np.array([[1,        0,      -self.vx],
                           [0,        1,       self.vy],
                           [-self.vx, self.vy, 1]])

        xyt_prime = gamma * np.dot(matrix, xyt)

        x = xyt_prime[0, 0]
        y = xyt_prime[1, 0]

        return ((x - player.x) * scale - player.image.get_rect().width / 2 + width / 2,
                (-y + player.y) * scale - player.image.get_rect().height / 2 + height / 2)
