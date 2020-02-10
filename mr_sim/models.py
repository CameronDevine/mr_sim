from .base import Base

__all__ = ["Preston"]


class Preston(Base):
    r"""A class implementing the Preston Equation for material removal simulation.

    This class calculates material removal rate using the Preston Equation,

    $\dot{h}=k_ppv$,

    where $\dot{h}$ is the depth of material removed per unit time, $k_p$ is a
    constant known as the Preston coefficient, $p$ is the contact pressure between
    the tool and the workpiece, and $v$ is the total speed of the tool rubbing the
    workpiece.

    Note:
        This class must be subclassed by a class providing the ``pressure`` and
        ``velocity`` functions.

    Attributes:
        kp (float): The value of the Preston coefficient, $k_p$.
    """

    def __init__(self, *args, kp=1, **kwargs):
        """
        Args:
            *args: Arguments to be passed on to superclasses.
            kp (float): The Preston coefficient, $k_p$. Defaults to 1.
            **kwargs: Keyword arguments to be passed on to superclasses.
        """
        super().__init__(*args, **kwargs)
        self.kp = kp

    def mrr(self, x, y):
        """Calculates the material removal rate.

        This function returns the material removal rate for all locations on the
        part surface using the Preston Equation.

        x (numpy.ndarray): A 2D array of the X coordinates of the part centered
            at the current tool location.
        y (numpy.ndarray): A 2D array of the Y coordinates of the part centered
            at the current tool location.

        returns:
            numpy.ndarray: The material removal rate at all locations on the part
            surface.
        """
        return self.kp * self.pressure(x, y) * self.velocity(x, y)
