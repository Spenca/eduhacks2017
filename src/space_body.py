import math
import numpy as np


class SpaceBody:
    space_bodies = []

    def __init__(self, x, y):
        self.image = None
        SpaceBody.space_bodies.append(self)

        self.x = x
        self.y = y

    def update(self, dt):
        pass

    def get_screen_pos(self, player, scale, width, height):
        initial_position = self.lorenz_transform(player,
                                                 np.array([[self.x - player.x],  # Space
                                                           [self.y - player.y],  # Space
                                                           [player.t]]))      # Time

        direction = self.lorenz_transform(player, np.array([[0],   # Space
                                                            [0],   # Space
                                                            [1]]))  # Time

        t_star = (player.t - initial_position[2, 0]) / direction[2, 0]

        intersection = initial_position + direction * t_star

        x = intersection[0, 0]
        y = intersection[1, 0]
        t = intersection[2, 0]

        return ((x * scale - self.image.get_rect().width / 2 + width / 2,
                 -y * scale - self.image.get_rect().height / 2 + height / 2),
                t)

    def lorenz_transform(self, player, vector):
        #matrix = np.array([[1, 0, -player.vx],
        #                   [0, 1, -player.vy],
        #                   [0, 0, 1]])
        #return np.dot(matrix, vector)
        return vector
