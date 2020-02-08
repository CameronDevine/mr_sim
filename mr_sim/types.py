from .base import Base
import numpy as np

__all__ = ["Orbital", "Belt", "Rotary"]


class Orbital(Base):
    def __init__(self, *args, eccentricity=None, **kwargs):
        super().__init__(*args, **kwargs)
        if eccentricity is None:
            raise ValueError("Tool eccentricity must be set.")
        self.eccentricity = eccentricity
        self.orbital_speed = 0
        self.rotational_speed = 0

    def set_speed(self, orbital_speed=0, rotational_speed=0):
        self.orbital_speed = orbital_speed
        self.rotational_speed = rotational_speed

    def velocity(self, x, y):
        return np.sqrt(
            (self.eccentricity * self.orbital_speed) ** 2
            + (x ** 2 + y ** 2) * self.rotational_speed ** 2
            + self.vl_x ** 2
            + self.vl_y ** 2
        )  # This is an approximation that should be verified


class Belt(Base):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.speed = 0

    def set_speed(self, speed):
        self.speed = speed

    def velocity(self, x, y):
        return np.sqrt(self.speed ** 2 + self.vl_x ** 2 + self.vl_y ** 2)


class Rotary(Base):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.speed = 0

    def set_speed(self, speed):
        self.speed = speed

    def velocity(self, x, y):
        return np.sqrt(
            (x ** 2 + y ** 2) * self.speed ** 2 + self.vl_x ** 2 + self.vl_y ** 2
        )
