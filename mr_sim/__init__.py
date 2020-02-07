from .shapes import *
from .types import *
from .pressure import *
from .models import *


def create_simulation(*classes):
    class Simulation(*classes):
        pass

    return Simulation
