import math
import numpy as np


class SpaceBody:
    space_bodies = []

    def __init__(self, x, y):
        self.image = None
        SpaceBody.space_bodies.append(self)

        self.x = x
        self.y = y
        self.x0 = x
        self.y0 = y
        self.t = 0
        self.vx = 0
        self.vy = 0
        self.vx0 = 0
        self.vy0 = 0
        self.vt = 1

    def update(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.t += self.vt * dt

        # Can't exceed speed of light
        assert abs(self.vx) <= 1
        assert abs(self.vy) <= 1

    def get_screen_pos(self, player, scale, width, height):
        tp, xp, yp = self.get_primed_coordinates(player, player)
        t, x, y = self.get_primed_coordinates(self, player)

        x = x - xp
        y = y - yp

        player.t = t

        if self == player:
            pass
            assert x == 0
            assert y == 0
            assert t == player.t

        return ((x * scale - self.image.get_rect().width / 2 + width / 2,
                 -y * scale - self.image.get_rect().height / 2 + height / 2),
                t)

    def get_primed_coordinates(self, body, player):
        # Lorenz transformation
        gamma = 1 / math.sqrt(1 - player.vy ** 2 - player.vx ** 2)
        matrix = np.array([[1, 0, -player.vx],
                           [0, 1, player.vy],
                           [-player.vx, player.vy, 1]])
        # (x,y) coordinates at t = 0 (static frame of reference)
        initial_point = np.array([[body.x],
                                  [body.y],
                                  [0]])
        # initial point in the moving reference frame
        initial_point_prime = gamma * np.dot(matrix, initial_point)
        # Direction of the worldline. (0,0,1) means no change in (x,y)
        worldline_direction = np.array([[0],
                                        [0],
                                        [1]])
        # Worldline in the moving reference frame
        worldline_direction_prime = gamma * np.dot(matrix, worldline_direction)
        # Time at which the object intersects moving time plane
        intersection_time = (player.t - initial_point_prime[2, 0]) / worldline_direction_prime[2, 0]
        xyt_prime = initial_point_prime + worldline_direction_prime * intersection_time
        x = xyt_prime[0, 0]
        y = xyt_prime[1, 0]
        t = xyt_prime[2, 0]
        return t, x, y
