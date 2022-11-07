from .base import Base
import numpy as np

__all__ = ["Orbital", "Belt", "Rotary"]


class Orbital(Base):
    """A class for simulating a random orbit sander.

    This class includes the necessary methods for calculating the total velocity
    of a random orbit sander.

    Attributes:
        eccentricity (float): The eccentric distance of the sander.
        orbital_speed (float): The current rotational speed of the eccentric link.
        rotational_speed (float): The current rotational speed of the pad with
            with respect to the part surface.
    """

    def __init__(self, *args, eccentricity=None, **kwargs):
        """
        Args:
            *args: Arguments to be passed on to superclasses.
            eccentricity (float): The eccentric distance of the sander. Defaults to None.
            **kwargs: Keyword arguments to be passed on to superclasses.

        Raises:
            ValueError: If ``eccentricity`` is not set.
        """
        super().__init__(*args, **kwargs)
        if eccentricity is None:
            raise ValueError("Tool eccentricity must be set.")
        self.eccentricity = eccentricity
        self.orbital_speed = 0
        self.rotational_speed = 0

    def set_speed(self, orbital_speed=0, rotational_speed=0):
        """Sets the orbital and rotational speed.

        Args:
            orbital_speed (float): The current rotational speed of the eccentric
                link. Defaults to 0.
            rotational_speed (float): The current rotational speed of the pad with
                with respect to the part surface. Defaults to 0.
        """
        self.orbital_speed = orbital_speed
        self.rotational_speed = rotational_speed

    def velocity(self, x, y):
        """Determines the velocity of the tool

        Determines the total velocity of the tool with respect to the part sufrace.

        Note:
            This is an approximation that should be more rigerously verified.

        Args:
            x (numpy.ndarray): A 2D array of the X coordinates of the part centered
                at the current tool location.
            y (numpy.ndarray): A 2D array of the Y coordinates of the part centered
                at the current tool location.

        Returns:
            numpy.ndarray: A 2D array of velocity on the part surface.
        """
        return np.sqrt(
            (self.eccentricity * self.orbital_speed) ** 2
            + (x**2 + y**2) * self.rotational_speed**2
        )


class Belt(Base):
    """A class for simulating a belt sander.

    This class includes the necessary methods for calculating the total velocity
    of a belt sander.

    Attributes:
        speed (float): The current speed of the belt.
    """

    def __init__(self, *args, **kwargs):
        """
        Args:
            *args: Arguments to be passed on to superclasses.
            **kwargs: Keyword arguments to be passed on to superclasses.
        """
        super().__init__(*args, **kwargs)
        self.speed = 0

    def set_speed(self, speed):
        """Sets the speed of the belt.

        Args:
            speed (float): The current speed of the belt.
        """
        self.speed = speed

    def velocity(self, x, y):
        """Determines the velocity of the tool

        Determines the total velocity of the tool with respect to the part sufrace.

        Note:
            This is an approximation that should be more rigerously verified.

        Args:
            x (numpy.ndarray): A 2D array of the X coordinates of the part centered
                at the current tool location.
            y (numpy.ndarray): A 2D array of the Y coordinates of the part centered
                at the current tool location.

        Returns:
            numpy.ndarray: A 2D array of velocity on the part surface.
        """
        return self.speed


class Rotary(Base):
    """A class for simulating a rotary abrasive tool.

    This class includes the necessary methods for calculating the total velocity
    of a rotary tool.

    Attributes:
        speed (float): The current rotational speed of the tool.
    """

    def __init__(self, *args, **kwargs):
        """
        Args:
            *args: Arguments to be passed on to superclasses.
            **kwargs: Keyword arguments to be passed on to superclasses.
        """
        super().__init__(*args, **kwargs)
        self.speed = 0

    def set_speed(self, speed):
        """Sets the rotational speed of the tool.

        Args:
            speed (float): The current rotational speed of the tool.
        """
        self.speed = speed

    def velocity(self, x, y):
        """Determines the velocity of the tool

        Determines the total velocity of the tool with respect to the part sufrace.

        Note:
            This is an approximation that should be more rigerously verified.

        Args:
            x (numpy.ndarray): A 2D array of the X coordinates of the part centered
                at the current tool location.
            y (numpy.ndarray): A 2D array of the Y coordinates of the part centered
                at the current tool location.

        Returns:
            numpy.ndarray: A 2D array of velocity on the part surface.
        """
        return np.sqrt(x**2 + y**2) * self.speed
