import numpy as np
import matplotlib.pyplot as plt

__all__ = ["Base"]


class Base:
    def __init__(self, size_x, size_y, dx=0.001, dy=0.001, dt=1, auto_velocity=False):
        x = np.arange(-size_x / 2, size_x / 2, dx)
        y = np.arange(-size_y / 2, size_y / 2, dy)
        self.X, self.Y = np.meshgrid(x, y)
        self.profile = np.zeros(self.X.shape)
        self.dt = dt
        self.auto_vel = auto_velocity
        self.x = None
        self.y = None
        self.vl_x = 0
        self.vl_y = 0

    def set_location(self, x=0, y=0):
        if self.auto_vel:
            if self.x is None or self.y is None:
                self.x = x
                self.y = y
            self.vl_x = (x - self.x) / self.dt
            self.vl_y = (y - self.y) / self.dt
        self.x = x
        self.y = y

    def set_velocity(self, x=0, y=0):
        self.vl_x = x
        self.vl_y = y

    def local_grid(self):
        return self.X - self.x, self.Y - self.y

    def step(self):
        shape = self.shape(*self.local_grid())
        self.profile[shape] += self.mrr()[shape] * self.dt / self.area

    def plot(self, **kwargs):
        plt.pcolor(self.X, self.Y, self.profile, edgecolors="face", **kwargs)
        plt.gca().set_aspect("equal", "box")
