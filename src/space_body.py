class SpaceBody:
    space_bodies = []

    def __init__(self, x, y):
        SpaceBody.space_bodies.append(self)

        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0

    def update(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt

        # Can't exceed speed of light
        assert abs(self.vx) <= 1
        assert abs(self.vy) <= 1
