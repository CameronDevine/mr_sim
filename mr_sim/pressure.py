from .base import Base

__all__ = ["Flat"]


class Flat(Base):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.force = 0
        self.torque_x = 0
        self.torque_y = 0

    def set_force(self, force):
        self.force = force

    def set_torque(self, x=0, y=0):
        self.torque_x = x
        self.torque_y = y

    def pressure(self, x, y):
        return (
            self.force / self.area
            + x * self.torque_y / self.Iy
            - y * self.torque_x / self.Ix
        )  # Make sure signs are correct here.
