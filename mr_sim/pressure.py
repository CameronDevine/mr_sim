from .base import Base
from .shapes import *
import numpy as np
from scipy.optimize import minimize_scalar, root_scalar
from scipy.interpolate import LinearNDInterpolator
import pymesh
import stl

__all__ = ["Flat", "ConstantCurvature", "Mesh"]


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

class Mesh(Base):
    """A ckass used to calculate the pressure applied to a surface defined by a mesh file.

    This class determines the pressure applied to the surface from the normal
    force by first determining the volume of the intersection between the tool
    and the part surface, then using the profile of this intersection to find the
    pressure distribution.

    Note:
        This class is only able to determine contact pressure distribution for
        round tools.

    Attributes:
        force (float): The normal force applied to the tool.
        stiffness (float): The stiffness of the tool.
            This can be found as the Young's modulus of the tool divided by
            its thickness.
        mesh (pymesh.Mesh): The mesh defining the part surface.
        normals (numpy.ndarray): The part mesh vertex normals.
        thickness (float): The thickness of the tool model used for determining
            intersection volume.
        segments (int): The number of segments to use to generate the tool cylinder.
    """

    def __init__(self, *args, mesh=None, stiffness=None, **kwargs):
        """
        Args:
            *args: Arguments to be passed on to superclasses.
            mesh (str or pymesh.Mesh): Either the filename of the mesh file to use
                or a ``pymesh.Mesh`` instance. Defaults to ``None``.
            stiffness (float): The stiffness of the sanding tool. Defaults to ``None``.
            **kwargs: Keyword arguments to be passed on to superclasses.

        Raises:
            ValueError: If ``stiffness`` or ``mesh`` is ``None``.
            TypeError: If ``mesh`` is not either ``str`` or ``pymesh.Mesh``.
            TypeError: If a superclass inheriting this class does not also inherit
                :class:`.Round`.
        """
        if not isinstance(self, Round):
            raise TypeError("the mesh class is only defined for round tools")
        super().__init__(*args, **kwargs)
        self.force = 0
        if stiffness is None:
            raise ValueError("tool stiffness not set")
        self.stiffness = stiffness
        if mesh is None:
            raise ValueError("part mesh not set")
        if isinstance(mesh, str):
            self.mesh = pymesh.meshio.load_mesh(mesh)
        elif isinstance(mesh, pymesh.Mesh):
            self.mesh = mesh
        else:
            raise TypeError("mesh is not a string or a pymesh.Mesh object")
        self.mesh.add_attribute("vertex_normal")
        self.normals = self.mesh.get_attribute("vertex_normal").reshape(
            self.mesh.vertices.shape
        )
        self.thickness = 0.02
        self.segments = 50

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

        Warning:
            This function only works for tools with a flat bottom, and assumes there
            are no vertices on the bottom of the mesh of the intersection of the tool
            and the part surface which is not necessarily the case even for flat tools.
            With more work this class could be used to determine the pressure
            distribution for tools without a flat bottom, such as spherical tools.
        """
        ind = np.argmin(
            np.linalg.norm(
                self.mesh.vertices[:, :2] - np.array([self.x, self.y]), axis=1
            )
        )
        set_point = np.array([self.x, self.y, self.mesh.vertices[ind, 2]])
        vertex_point = self.mesh.vertices[ind, :].flatten()
        normal = self.normals[ind, :]
        point = np.dot(vertex_point - set_point, normal) * normal + set_point

        def intersection(d):
            tool = pymesh.generate_cylinder(
                point - d * normal,
                point + (self.thickness - d) * normal,
                self.radius,
                self.radius,
                self.segments,
            )
            intersect = pymesh.boolean(self.mesh, tool, "intersection")
            return intersect

        def volume(intersect):
            mesh = stl.mesh.Mesh(np.zeros(intersect.faces.shape[0], dtype=stl.mesh.Mesh.dtype))
            for i, f in enumerate(intersect.faces):
                for j in range(3):
                    mesh.vectors[i][j] = intersect.vertices[f[j], :]
            return mesh.get_mass_properties()[0]

        def objective(d):
            f = self.stiffness * volume(intersection(d))
            print(d, f, self.force, f - self.force)
            return f - self.force

        res = root_scalar(objective, bracket=(0, self.thickness), method='brentq')
        d = res.root
        intersect = intersection(d)
        # intersect, info = pymesh.collapse_short_edges(intersection(d), 1e-3)
        # print(info)
        vx = np.array(
            [[0, 0, -normal[0]], [0, 0, -normal[1]], [normal[0], normal[1], 0]]
        )
        R = np.eye(3) + vx + vx @ vx * (1 - normal[2]) / np.sum(normal[:2] ** 2)
        vertices = (R @ (intersect.vertices - point + normal * d).T).T
        interpolator = LinearNDInterpolator(
            vertices[:, :2], vertices[:, 2].flatten(), fill_value=0, rescale=True
        )
        pressure = self.stiffness * interpolator(
            np.vstack((self.X.reshape(-1), self.Y.reshape(-1))).T
        )
        return pressure.reshape(x.shape)
