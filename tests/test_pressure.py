from context import mr_sim
import unittest
import numpy as np


class TestFlat(unittest.TestCase):
    def test_init(self):
        flat = mr_sim.Flat(1, 1)
        self.assertEqual(flat.force, 0)
        self.assertEqual(flat.torque_x, 0)
        self.assertEqual(flat.torque_y, 0)

    def test_torque_setter(self):
        flat = mr_sim.Flat(1, 1)
        flat.set_torque(x=1)
        self.assertEqual(flat.torque_x, 1)
        flat.set_torque(y=2)
        self.assertEqual(flat.torque_y, 2)
        flat.set_torque(3, 4)
        self.assertEqual(flat.torque_x, 3)
        self.assertEqual(flat.torque_y, 4)
        flat.set_torque(5)
        self.assertEqual(flat.torque_x, 5)

    def test_force_setter(self):
        flat = mr_sim.Flat(1, 1)
        flat.set_force(6)
        self.assertEqual(flat.force, 6)

    def test_pressure(self):
        flat = mr_sim.Flat(1, 1)
        flat.set_force(6)
        flat.set_torque(-2, 3)
        flat.area = 4
        flat.Ix = 2
        flat.Iy = 3
        pressure = flat.pressure(flat.X, flat.Y)
        self.assertTrue(
            np.allclose(
                flat.pressure(flat.X, flat.Y), 6 / 4 + flat.X * 3 / 3 - flat.Y * -2 / 2
            )
        )
        self.assertGreater(pressure[0, -1], pressure[0, 0])
        self.assertGreater(pressure[-1, 0], pressure[0, 0])

    def test_base(self):
        flat = mr_sim.Flat(1, 1, dt=0.5)
        self.assertTrue(hasattr(flat, "X"))
        self.assertTrue(hasattr(flat, "Y"))
        self.assertTrue(hasattr(flat, "profile"))
        self.assertTrue(hasattr(flat, "dt"))
        self.assertEqual(flat.dt, 0.5)


class TestConstantCurvature(unittest.TestCase):
    def test_init(self):
        with self.assertRaises(ValueError):
            cc = mr_sim.ConstantCurvature(1, 1, kx=1, ky=2, dx=0.002, dy=0.002)
        cc = mr_sim.ConstantCurvature(
            1, 1, kx=1, ky=2, stiffness=100, dx=0.002, dy=0.002
        )
        self.assertEqual(cc.force, 0)
        self.assertEqual(cc.kx, 1)
        self.assertEqual(cc.ky, 2)
        self.assertEqual(cc.stiffness, 100)
        self.assertEqual(cc.dx, 0.002)
        self.assertEqual(cc.dy, 0.002)
        self.assertAlmostEqual(cc.X[0, 1] - cc.X[0, 0], 0.002)
        self.assertAlmostEqual(cc.Y[1, 0] - cc.Y[0, 0], 0.002)

    def test_force_setter(self):
        cc = mr_sim.ConstantCurvature(
            1, 1, kx=1, ky=2, stiffness=100, dx=0.002, dy=0.002
        )
        cc.set_force(3)
        self.assertEqual(cc.force, 3)

    def test_curvature_setter(self):
        cc = mr_sim.ConstantCurvature(
            1, 1, kx=1, ky=2, stiffness=100, dx=0.002, dy=0.002
        )
        cc.set_curvature(kx=4)
        self.assertEqual(cc.kx, 4)
        cc.set_curvature(ky=5)
        self.assertEqual(cc.ky, 5)
        cc.set_curvature(6, 7)
        self.assertEqual(cc.kx, 6)
        self.assertEqual(cc.ky, 7)
        cc.set_curvature(8)
        self.assertEqual(cc.kx, 8)

    def test_pressure_square(self):
        dx = 0.0001
        dy = 0.0001
        Sim = mr_sim.create_simulation(mr_sim.Square, mr_sim.ConstantCurvature)
        sim = Sim(0.2, 0.2, kx=0.2, ky=0.4, stiffness=1e7, dx=dx, dy=dy, width=0.1)
        shape = sim.shape(sim.X, sim.Y)
        p = sim.pressure(sim.X, sim.Y)
        self.assertAlmostEqual(np.sum(p) * dx * dy, sim.force)
        self.assertFalse(np.any(p[~shape] != 0))
        sim.set_force(5)
        p = sim.pressure(sim.X, sim.Y)
        self.assertAlmostEqual(np.sum(p) * dx * dy, sim.force, 6)
        self.assertFalse(np.any(p[~shape] != 0))
        sim.set_force(20)
        p = sim.pressure(sim.X, sim.Y)
        self.assertAlmostEqual(np.sum(p) * dx * dy, sim.force, 6)
        self.assertFalse(np.any(p[~shape] != 0))

    def test_pressure_round(self):
        dx = 0.0001
        dy = 0.0001
        Sim = mr_sim.create_simulation(mr_sim.Round, mr_sim.ConstantCurvature)
        sim = Sim(0.2, 0.2, kx=0.2, ky=0.4, stiffness=1e7, dx=dx, dy=dy, radius=0.05)
        shape = sim.shape(sim.X, sim.Y)
        p = sim.pressure(sim.X, sim.Y)
        self.assertAlmostEqual(np.sum(p) * dx * dy, sim.force)
        self.assertFalse(np.any(p[~shape] != 0))
        sim.set_force(5)
        p = sim.pressure(sim.X, sim.Y)
        self.assertAlmostEqual(np.sum(p) * dx * dy, sim.force, 6)
        self.assertFalse(np.any(p[~shape] != 0))
        sim.set_force(20)
        p = sim.pressure(sim.X, sim.Y)
        self.assertAlmostEqual(np.sum(p) * dx * dy, sim.force, 6)
        self.assertFalse(np.any(p[~shape] != 0))
        sim.set_force(60)
        p = sim.pressure(sim.X, sim.Y)
        self.assertAlmostEqual(np.sum(p) * dx * dy, sim.force, 6)
        self.assertFalse(np.any(p[~shape] != 0))

    def test_base(self):
        cc = mr_sim.ConstantCurvature(
            1, 1, kx=1, ky=2, stiffness=100, dx=0.002, dy=0.002, dt=0.2
        )
        self.assertTrue(hasattr(cc, "X"))
        self.assertTrue(hasattr(cc, "Y"))
        self.assertTrue(hasattr(cc, "profile"))
        self.assertTrue(hasattr(cc, "dt"))
        self.assertEqual(cc.dt, 0.2)
