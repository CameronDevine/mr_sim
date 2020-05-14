from .base import Base
import numpy as np

__all__ = ["Round", "Rectangular", "Square"]


class BaseShape(Base):
    """A base class for all shapes providing the antialiasing function.

    Attributes:
        antialias (bool): A boolean indicating whether or not to antialias the shape.
        antialias_dist (float): The distance over which to change from covered to
            uncovered by the tool.
    """

    def __init__(self, *args, antialias=True, antialias_dist=None, **kwargs):
        """
        Args:
            *args: Arguments to be passed on to superclasses.
            antialias (bool): Whether the bounds of the tool should be antialiased.
                Defaults to ``True``.
            antialias_dist (float): The distance over which to change from convered
                to uncovered. Defaults to :math:`\sqrt{dx^2+dy^2}`.
            **kwargs: Keyword arguments to be passed on to superclasses.
        """
        super().__init__(*args, **kwargs)
        self.antialias = antialias
        self.antialias_dist = antialias_dist
        if self.antialias_dist is None:
            self.antialias_dist = np.sqrt(self.dx ** 2 + self.dy ** 2)

    def _antialias(self, x):
        """

        Args:
            x (numpy.ndarray): The input array.

        Returns:
            numpy.ndarray: The output array with a value of ``1`` when ``x<0``
            and ``0`` when ``x>0`` with the transition spread over a distance
            ``antialias_dist``.
        """
        if self.antialias:
            return (x < -self.antialias_dist) + (
                x - self.antialias_dist
            ) / self.antialias_dist * (self.antialias_dist > x > -self.antialias_dist)
        else:
            return self.antialias


class Round(BaseShape):
    """A class representing a round tool for material removal simulations.

    This class represents a round tool and calculates the section of the part
    surface which the tool is in contact with.

    Attributes:
        r (float): The tool radius.
        area (float): The area of the tool.
        Ix (float): The second moment of area of the tool in the X direction.
        Iy (float): The second moment of area of the tool in the Y direction.

    Note:
        The class attributes are set automatically when the class is initialized,
        and when the tool radius is set using the ``radius`` property. Setting
        these values manually could lead to simulation errors.
    """

    def __init__(self, *args, radius=None, **kwargs):
        """
        Args:
            *args: Arguments to be passed on to superclasses.
            radius (float): The radius of the tool. Defaults to ``None``.
            **kwargs: Keyword arguments to be passed on to superclasses.

        Raises:
            ValueError: If ``radius`` is not set.
        """
        super().__init__(*args, **kwargs)
        if radius is None:
            raise ValueError("Tool radius must be set.")
        self.radius = radius

    @property
    def radius(self):
        """float: Tool radius."""
        return self.r

    @radius.setter
    def radius(self, r):
        self.r = r
        self.area = np.pi * r ** 2
        self.Ix = np.pi * r ** 4 / 4
        self.Iy = np.pi * r ** 4 / 4

    def shape(self, x, y):
        """This function finds the section of the part the tool is in contact with.

        Args:
            x (numpy.ndarray): A 2D array of the X coordinates of the part centered
                at the current tool location.
            y (numpy.ndarray): A 2D array of the Y coordinates of the part centered
                at the current tool location.

        Returns:
            numpy.ndarray: A 2D array where ``True`` indicates the tool is in contact
            with that portion of the part surface.
        """
        return self._antialias(x ** 2 + y ** 2 - self.r ** 2)


class Rectangular(BaseShape):
    """A class representing a rectangular tool for material removal simulations.

    This class represents a rectangular tool and calculates the section of the
    part surface which the tool is in contact with.

    Attributes:
        width (float): The tool width, in the X direction.
        height (float): The tool height, in the Y direction.
        area (float): The area of the tool.
        Ix (float): The second moment of area of the tool in the X direction.
        Iy (float): The second moment of area of the tool in the Y direction.

    Note:
        The class attributes are set automatically when the class is initialized,
        and when the tool size is set using the ``set_size`` method. Setting
        these values manually could lead to simulation errors.
    """

    def __init__(self, *args, width=None, height=None, **kwargs):
        """
        Args:
            *args: Arguments to be passed on to superclasses.
            width (float): The width of the tool, in the X direction. Defaults to
                ``None``.
            height (float): The height of the tool, in the Y direction. Defaults
                to ``None``.
            **kwargs: Keyword arguments to be passed on to superclasses.

        Raises:
            ValueError: If ``width`` or ``height`` is not set.
        """
        if width is None:
            raise ValueError("Tool width must be set.")
        if height is None:
            raise ValueError("Tool height must be set.")
        super().__init__(*args, **kwargs)
        self._set_size(width, height)

    def _set_size(self, width, height):
        self.width = width
        self.height = height
        self.area = width * height
        self.Ix = width * height ** 3 / 12
        self.Iy = width ** 3 * height / 12

    def set_size(self, width, height):
        """Set the size of the tool.

        Args:
            width (float): The width of the tool, in the X direction.
            height (float): The height of the tool, in the Y direction.
        """
        self._set_size(width, height)

    def shape(self, x, y):
        """This function finds the section of the part the tool is in contact with.

        Args:
            x (numpy.ndarray): A 2D array of the X coordinates of the part centered
                at the current tool location.
            y (numpy.ndarray): A 2D array of the Y coordinates of the part centered
                at the current tool location.

        Returns:
            numpy.ndarray: A 2D array where ``True`` indicates the tool is in contact
            with that portion of the part surface.
        """
        return (
            self._antialias((self.width / 2) + x)
            * self._antialias((self.width / 2) - x)
            * self._antialias((self.height / 2) + y)
            * self._antialias((self.height / 2) - y)
        )


class Square(Rectangular):
    """A class representing a square tool for material removal simulations.

    This class represents a square tool and calculates the section of the
    part surface which the tool is in contact with.

    Note:
        This class simply inherits :class:`.Rectangular` and sets both ``width``
        and ``height`` to the same value.
    """

    def __init__(self, *args, width=None, **kwargs):
        """
        Args:
            *args: Arguments to be passed on to superclasses.
            width (float): The width of the tool. Defaults to
                ``None``.
            **kwargs: Keyword arguments to be passed on to superclasses.

        Raises:
            ValueError: If ``width`` is not set.
        """
        super().__init__(*args, width=width, height=width, **kwargs)

    def set_size(self, width):
        """Set the size of the tool.

        Args:
            width (float): The width of the tool.
        """
        self._set_size(width, width)
