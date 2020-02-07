from .base import Base
import numpy as np

__all__ = ["Round", "Rectangular", "Square"]


class Round(Base):
    def __init__(self, *args, radius=None, **kwargs):
        super().__init__(*args, **kwargs)
        if radius is None:
            raise ValueError("Tool radius must be set.")
        self.radius = radius

    @property
    def radius(self):
        return self.r

    @radius.setter
    def radius(self, r):
        self.r = r
        self.area = np.pi * r ** 2
        self.Ix = np.pi * r ** 4 / 4
        self.Iy = np.pi * r ** 4 / 4

    def shape(self, x, y):
        return x ** 2 + y ** 2 <= self.r ** 2


class Rectangular(Base):
    def __init__(self, *args, width=None, height=None, **kwargs):
        if width is None:
            raise ValueError("Tool width must be set.")
        if height is None:
            raise ValueError("Tool height must be set.")
        super().__init__(*args, **kwargs)
        self.set_size(width, height)

    def set_size(self, width, height):
        self.width = width
        self.height = height
        self.area = width * height
        self.Ix = width * height ** 3 / 12
        self.Iy = width ** 3 * height / 12

    def shape(self, x, y):
        return (
            (-(self.width / 2) <= x)
            & ((self.width / 2) >= x)
            & (-(self.height / 2) <= y)
            & ((self.height / 2) >= y)
        )


class Square(Rectangular):
    def __init__(self, *args, width=None, **kwargs):
        super().__init__(*args, width=width, height=width, **kwargs)
