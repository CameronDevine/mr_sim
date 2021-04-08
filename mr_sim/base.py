import numpy as np
import matplotlib.pyplot as plt

__all__ = ["Base"]


class Base:
    """The base simulation class.

    This is the base simulation class. It is combined with other classes to define
    other attributes about the simulation.

    Attributes:
        X (numpy.ndarray): A 2D array of the X coordinates of the part with the
            origin at the center of the part surface.
        Y (numpy.ndarray): A 2D array of the Y coordinates of the part with the
            origin at the center of the part surface.
        profile (numpy.ndarray): A 2D array of the depth of material removed from
            the part surface.
        dt (float): The timestep used in the simulation.
        auto_vel (bool): If ``True`` automatically calculate the linear velocity
            of the tool moving over the part surface.
        x (float): The current X location of the center of the tool in relation
            to the center of the part surface.
        y (float): The current Y location of the center of the tool in relation
            to the center of the part surface.
        vl_x (float): The current X direction velocity of the tool moving over the
            part surface.
        vl_y (float): The current Y direction velocity of the tool moving over the
            part surface.

    Note:
        Other classes must be used to include the ``shape`` and ``mrr`` methods needed
        by this class.
    """

    def __init__(self, size_x, size_y, dx=0.001, dy=0.001, dt=1, auto_velocity=False):
        """
        Args:
            size_x (float): The size of the part surface in the X direction.
            size_y (float): The size of the part surface in the Y direction.
            dx (float): The density of points to track in the X direction. Defaults
                to 0.001.
            dy (float): The density of points to track in the Y direction. Defaults
                to 0.001.
            dt (float): The simulation timestep. Defaults to 1.
            auto_velocity (bool): If ``True`` automatically calculate the linear
                velocity of the tool over the part surface.
        """
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
        """Set the current location of the center of the tool.

        Sets the current location of the center of the tool with respect to the
        middle of the part.

        Args:
            x (float): The X location of the tool. Defaults to 0.
            y (float): The Y location of the tool. Defaults to 0.
        """
        if self.auto_vel:
            if self.x is None or self.y is None:
                self.x = x
                self.y = y
            self.vl_x = (x - self.x) / self.dt
            self.vl_y = (y - self.y) / self.dt
        self.x = x
        self.y = y

    def set_velocity(self, x=0, y=0):
        """Sets the current linear velocity of the tool over the part surface.

        Args:
            x (float): The X velocity of the tool. Defaults to 0.
            y (float): The Y velocity of the tool. Defaults to 0.

        Note:
            If ``auto_velocity`` was set to ``True`` this method is not requried.
        """
        self.vl_x = x
        self.vl_y = y

    def local_grid(self):
        """Returns a coordinate system centered at the tool origin.

        Returns:
            numpy.ndarray, numpy.ndarray: The X, Y coordinate system shifted so the
            origin is at the center of the tool.
        """
        return self.X - self.x, self.Y - self.y

    def step(self):
        """Move the simulation forward one timestep."""
        grid = self.local_grid()
        self.profile += self.dt * self.mrr(*grid)

    def plot(self, normalize=False, **kwargs):
        """Plot the simulation result.

        This function uses matplotlib to plot the result of the simulation in the
        current figure.

        Args:
            normalize (bool): Normalize max depth of material removed to 1. Defaults
                to ``False``.
            **kwargs: Keyword arguments to be included in the call to the
                ``matplotlib.pyplot.imshow`` function.

        Returns:
            matplotlib.image.AxesImage: The ``AxesImage`` object of the plotted heatmap.
        """
        data = self.profile
        if normalize:
            data /= data.max()
        return plt.imshow(
            data,
            aspect="equal",
            origin="lower",
            extent=(self.X.min(), self.X.max(), self.Y.min(), self.Y.max()),
            **kwargs
        )
