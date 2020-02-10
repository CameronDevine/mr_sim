from .shapes import *
from .types import *
from .pressure import *
from .models import *


def create_simulation(*classes):
    """A helper method to combine classes.

    This method combines classes representing different elements of a material
    removal simulation. This allows different simulations to be easily constructed.

    Args:
        *classes: Variable length argument list of classes to subclass.

    Returns:
        A class which is a subclass of all classes provided as arguments.

    Examples:
        For example, to use the Preston equation to simulate a round orbital sander
        sanding a flat surface, the following can be used.

        >>> from mr_sim import *
        >>> Simulation = create_simulation(Flat, Round, Orbital, Preston)
        >>> simulation = Simulation(0.3, 0.1, radius=0.05, eccentricity=0.005, dt=0.001, kp=1e-9)

        In this example ``radius`` sets the radius of the sander defined in the
        ``Round`` class, ``eccentricity`` sets the eccentricity of the orbital
        sander defined in the ``Orbital`` class, ``dt`` sets the timestep in the
        ``Base`` class, which is a superclass of all other classes, and ``kp``
        sets the constant in the Preston Equation class, ``Preston``.

        The same result can be accomplished manually.

        >>> from mr_sim import *
        >>> Simulation(Flat, Round, Orbital, Preston):
        >>>     pass
        >>> simulation = Simulation(0.3, 0.1, radius=0.05, eccentricity=0.005, dt=0.001, kp=1e-9)

        This approach would be particularly useful if additional functionality
        needs to be added to the simulation class.
    """

    class Simulation(*classes):
        pass

    return Simulation
