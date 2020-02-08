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
