from .base import Base
from .shapes import *
import numpy as np
from scipy.optimize import minimize_scalar, root_scalar
from scipy.interpolate import NearestNDInterpolator, LinearNDInterpolator
import trimesh
from io import IOBase

__all__ = ["Flat", "ConstantCurvature", "STL"]


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
        ) * self.shape(x, y)


class ConstantCurvature(Base):
    """A class used to calculate the pressure applied to a surface with constant curvature.

    This class determines the pressure applied to the surface from the
    normal force.

    Note:
        This class models the contact pressure as a paraboloid with the specified
        curvature at the tool origin.

    Attributes:
        force (float): The normal force applied to the tool.
        kx (float): The curvature in the x direction.
        ky (float): The curvature in the y direction.
        dx (float): The x direction spacing of the grid.
        dy (float): The y direction spacing of the grid.
        stiffness (float): The stiffness of the tool.
            This can be found as the Young's modulus of the tool divided by
            its thickness.
    """

    def __init__(self, *args, kx=0, ky=0, stiffness=None, dx=0.001, dy=0.001, **kwargs):
        """
        Args:
            *args: Arguments to be passed on to superclasses.
            kx (float): The curvature in the x direction. Defaults to 0.
            ky (float): The curvature in the y direction. Defaults to 0.
            stiffness (float): The stiffness of the sanding tool. Defaults to ``None``.
                This can be found as the Young's modulus of the tool divided by
                its thickness.
            dx (float): The x direction spacing of the grid. Defaults to 0.001.
            dy (float): The y direction spacing of the grid. Defaults to 0.001.
            **kwargs: Keyword arguments to be passed on to superclasses.

        Raises:
            ValueError: If ``stiffness`` is ``None``.
        """
        super().__init__(*args, dx=dx, dy=dy, **kwargs)
        self.force = 0
        self.kx = kx
        self.ky = ky
        if stiffness is None:
            raise ValueError("tool stiffness must be set")
        self.stiffness = stiffness
        self.dx = dx
        self.dy = dy

    def set_curvature(self, kx=0, ky=0):
        """Set the curvature of the surface.

        Args:
            kx (float): The curvature in the x direction. Defaults to 0.
            ky (float): The curvature in the y direction. Defaults to 0.
        """
        self.kx = kx
        self.ky = ky

    def set_force(self, force):
        """Set the current normal force applied to the tool.

        Args:
            force (float): The current normal force.
        """
        self.force = force

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

        Note:
            This function uses closed form solutions if the shape is :class:`.Round`,
            otherwise it uses :meth:`scipy.optimize.minimize_scalar` which is slow.
        """
        shape = self.shape(x, y)

        def pressure(d):
            p = self.stiffness * (d - self.kx * x ** 2 / 2 - self.ky * y ** 2 / 2)
            p *= shape * (p > 0)
            return p

        if isinstance(self, Round):
            d = np.sqrt(
                self.force * np.sqrt(self.kx * self.ky) / (self.stiffness * np.pi)
            )
            if self.radius >= np.sqrt(2 * d / min(self.kx, self.ky)):
                return pressure(d)
            d = (
                self.force / (self.stiffness * np.pi * self.radius ** 2)
                + self.radius ** 2 * (self.kx + self.ky) / 8
            )
            if self.radius <= np.sqrt(2 * d / max(self.kx, self.ky)):
                return pressure(d)

        def objective(d):
            return (np.sum(pressure(d)) * self.dx * self.dy - self.force) ** 2

        start = self.force / (self.area * self.stiffness)

        res = minimize_scalar(objective, bracket=(start, 2 * start))

        return pressure(res.x)


class STL(Base):
    """A class for calculating pressure distribution on an STL file defined surface.

    This class calculates a pressure distribution by linearly interpolating over
    the STL verticies and determining pressure distribution with the tool stiffness.

    Attributes:
        force (float): The normal force applied to the tool.
        dx (float): The x direction spacing of the grid.
        dy (float): The y direction spacing of the grid.
        stiffness (float): The stiffness of the tool.
            This can be found as the Young's modulus of the tool divided by its
            thickness.
        mesh (trimesh.Trimesh): The mesh of the part surface.
    """
    def __init__(self, *args, dx=0.001, dy=0.001, stiffness=None, mesh=None, **kwargs):
        """
        Args:
            *args: Arguments to be passed on to superclasses.
            dx (float): The x direction spacing of the grid. Defaults to 0.001.
            dy (float): The y direction spacing of the grid. Defaults to 0.001.
            stiffness (float): The stiffness of the sanding tool. Defaults to ``None``.
                This can be found as the Young's modulus of the tool divided by
                its thickness.
            mesh (trimesh.Trimesh, str, or a file like object): The mesh of the
                part surface. Either a ``stl.mesh.Mesh`` object, the filename of
                a STL file, or a file like object of an STL file.
            **kwargs: Keyword arguments to be passed on to superclasses.

        Raises:
            ValueError: If ``stiffness`` or ``mesh`` is ``None``.
            TypeError: If ``mesh`` is not a string, a file like object, or as
                ``trimesh.Trimesh`` object.
        """
        super().__init__(*args, dx=dx, dy=dy, **kwargs)
        self.force = 0
        self.dx = dx
        self.dy = dy
        if stiffness is None:
            raise ValueError("tool stiffness not set")
        self.stiffness = stiffness
        if mesh is None:
            raise ValueError("part mesh not set")
        if isinstance(mesh, (str, IOBase)):
            self.mesh = trimesh.load_mesh(mesh)
        elif isinstance(mesh, trimesh.Trimesh):
            self.mesh = mesh
        else:
            raise TypeError("mesh is not a string or a stl.mesh.Mesh object")

    def set_force(self, force):
        """Set the current normal force applied to the tool.

        Args:
            force (float): The current normal force.
        """
        self.force = force

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
        interpolator = NearestNDInterpolator(self.mesh.vertices[:, :2], np.hstack((self.mesh.vertices, self.mesh.vertex_normals)))
        data = interpolator(np.array([self.x, self.y])).flatten()
        vertex_point = data[:3]
        set_point = np.array([self.x, self.y, vertex_point[2]])
        normal = data[3:]
        point = np.dot(vertex_point - set_point, normal) * normal + set_point
        # https://math.stackexchange.com/a/476311
        vx = np.array(
            [[0, 0, -normal[0]], [0, 0, -normal[1]], [normal[0], normal[1], 0]]
        )
        R = np.eye(3) + vx + vx @ vx * (1 - normal[2]) / np.sum(normal[:2] ** 2)
        transform = np.eye(4)
        transform[:3, :3] = R
        transform[:3, 3] = (R @ -point.reshape(-1, 1)).flatten()
        shape = self.shape(x, y)

        def pressure(d):
            mesh = self.mesh.copy()
            d_transform = transform.copy()
            d_transform[2, 3] += d
            mesh.apply_transform(d_transform)
            interpolator = LinearNDInterpolator(mesh.vertices[:, :2], mesh.vertices[:, 2], fill_value=0)
            p = self.stiffness * interpolator(np.vstack((x.reshape(-1), y.reshape(-1))).T).reshape(x.shape)
            return p * (p > 0) * shape

        def objective(d):
            return pressure(d).sum() * self.dx * self.dy - self.force

        res = root_scalar(objective, bracket=(0, 0.01), method='brentq')

        return pressure(res.root)
