import pygame
import math

from .space_body import SpaceBody

ACCELERATION = 0.1
ROTATION_SPEED = 1


class Player(SpaceBody):
    def __init__(self):
        super().__init__(0, 0)

        self.rotation = math.pi/2

        self.up_image = pygame.image.load("assets/player.png")
        self.image = pygame.transform.rotate(self.up_image, self.rotation * 180/math.pi)

    def thrust_forward(self, dt):
        dvx = ACCELERATION * math.cos(self.rotation) * dt
        dvy = ACCELERATION * math.sin(self.rotation) * dt

        self.move(dvx, dvy)

    def thrust_backwards(self, dt):
        dvx = -ACCELERATION * math.cos(self.rotation) * dt
        dvy = -ACCELERATION * math.sin(self.rotation) * dt

        self.move(dvx, dvy)

    def move(self, dvx, dvy):
        self.vx = (self.vx + dvx) / (1 + abs(self.vx * dvx))
        self.vy = (self.vy + dvy) / (1 + abs(self.vy * dvy))

    def rotate_right(self, dt):
        self.rotation -= ROTATION_SPEED * dt

        self.update_sprite()

    def rotate_left(self, dt):
        self.rotation += ROTATION_SPEED * dt

        self.update_sprite()

    def update_sprite(self):
        self.image = pygame.transform.rotate(self.up_image, self.rotation * 180/math.pi)

    def update(self, dt):
        super(Player, self).update(dt)
