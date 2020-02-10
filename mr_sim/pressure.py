from .base import Base

__all__ = ["Flat"]


class Flat(Base):
    """A class used to calculate the pressure applied to a flat surface.

    This class determines the pressure applied to a flat surface from the normal force and torques applied to the tool.

    Note:
        This class assumes that all points of the tool are in contact with the
        part surface at all time.

    Attributes:
        force (float): The normal force applied to the tool.
        torque_x (float): The torque about the X axis applied to the tool.
        torque_y (float): The torque about the Y axis applied to the tool.

    Note:
        This class requires ``area``, ``Ix``, and ``Iy`` to be set by a subclass.
    """

    def __init__(self, *args, **kwargs):
        """
        Args:
            *args: Arguments to be passed on to superclasses.
            **kwargs: Keyword arguments to be passed on to superclasses.
        """
        super().__init__(*args, **kwargs)
        self.force = 0
        self.torque_x = 0
        self.torque_y = 0

    def set_force(self, force):
        """Set the current normal force applied to the tool.

        Args:
            force (float): The current normal force.
        """
        self.force = force

    def set_torque(self, x=0, y=0):
        """Set the current torques applied to the tool.

        Args:
            x (float): The current torque about the X axis. Defaults to 0.
            y (float): The current torque about the Y axis. Defaults to 0.
        """
        self.torque_x = x
        self.torque_y = y

    def pressure(self, x, y):
        """Determine the pressure the tool applied to the part surface.

        This function calculates the pressure applied at all points on the part
        surface.

        Args:
            x (numpy.ndarray): A 2D array of the X coordinates of the part centered
                at the current tool location.
            y (numpy.ndarray): A 2D array of the Y coordinates of the part centered
                at the current tool location.

        Returns:
            numpy.ndarray: A 2D array of the pressure applied by the tool.
        """
        return (
            self.force / self.area
            + x * self.torque_y / self.Iy
            - y * self.torque_x / self.Ix
        )
