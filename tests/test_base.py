from context import mr_sim, Base
import unittest
import numpy as np


class TestBase(unittest.TestCase):
    def test_init_default(self):
        base = Base(1, 2)
        self.assertEqual(base.dt, 1)
        self.assertFalse(base.auto_vel)
        self.assertTrue(np.all(base.profile == 0))
        size = (2 / 0.001, 1 / 0.001)
        self.assertEqual(base.profile.shape, size)
        self.assertEqual(base.X.shape, size)
        self.assertEqual(base.Y.shape, size)

    def test_init(self):
        base = Base(4, 3, dx=0.005, dy=0.002, auto_velocity=True, dt=0.01)
        self.assertEqual(base.dt, 0.01)
        self.assertTrue(base.auto_vel)
        self.assertTrue(np.all(base.profile == 0))
        size = (3 / 0.002, 4 / 0.005)
        self.assertEqual(base.profile.shape, size)
        self.assertEqual(base.X.shape, size)
        self.assertEqual(base.Y.shape, size)

    def teset_location_setter_auto(self):
        base = Base(1, 1, dt=0.1, auto_velocity=True)
        self.assertEqual(self.vl_x, 0)
        self.assertEqual(self.vl_y, 0)
        base.set_location(3, 6)
        self.assertEqual(self.x, 3)
        self.assertEqual(self.y, 6)
        self.assertEqual(self.vl_x, 0)
        self.assertEqual(self.vl_y, 0)
        base.set_location(1, 7)
        self.assertEqual(self.x, 1)
        self.assertEqual(self.y, 7)
        self.assertEqual(self.vl_x, -0.2)
        self.assertEqual(self.vl_y, 0.1)

    def test_location_setter(self):
        base = Base(1, 1)
        base.set_location(x=1)
        self.assertEqual(base.x, 1)
        base.set_location(y=2)
        self.assertEqual(base.y, 2)
        base.set_location(3, 4)
        self.assertEqual(base.x, 3)
        self.assertEqual(base.y, 4)
        base.set_location(5)
        self.assertEqual(base.x, 5)

    def test_velocity_setter(self):
        base = Base(1, 1)
        base.set_velocity(x=1)
        self.assertEqual(base.vl_x, 1)
        base.set_velocity(y=2)
        self.assertEqual(base.vl_y, 2)
        base.set_velocity(3, 4)
        self.assertEqual(base.vl_x, 3)
        self.assertEqual(base.vl_y, 4)
        base.set_velocity(5)
        self.assertEqual(base.vl_x, 5)

    def test_local_grid(self):
        base = Base(2, 1)
        base.set_location(0.75, 0.25)
        local_grid = base.local_grid()
        self.assertTrue(np.allclose(local_grid[0], base.X - 0.75))
        self.assertTrue(np.allclose(local_grid[1], base.Y - 0.25))

    def test_step(self):
        class Test(Base):
            def mrr(self, x, y):
                return x + 0.2 * y

        test = Test(1, 1, dt=0.1)
        test.set_location()
        self.assertTrue(np.allclose(test.profile, 0))
        test.step()
        self.assertTrue(np.allclose(test.profile, ((test.X + 0.2 * test.Y) * 0.1)))
