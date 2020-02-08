from context import mr_sim
import unittest
import numpy as np


class TestPreston(unittest.TestCase):
    def test_init_default(self):
        preston = mr_sim.Preston(1, 1)
        self.assertEqual(preston.kp, 1)

    def test_init(self):
        preston = mr_sim.Preston(1, 1, kp=2)
        self.assertEqual(preston.kp, 2)

    def test_mrr(self):
        class MRRTest(mr_sim.Preston):
            def pressure(self, x, y):
                return 0.5 * self.X + 0.15 * self.Y

            def velocity(self, x, y):
                return 0.1 * self.Y ** 2

        preston = MRRTest(1, 1, kp=4)
        preston.set_location()
        self.assertTrue(
            np.allclose(
                preston.mrr(),
                4 * (0.5 * preston.X + 0.15 * preston.Y) * (0.1 * preston.Y ** 2),
            )
        )

    def test_base(self):
        preston = mr_sim.Preston(1, 1, dt=0.1)
        self.assertTrue(hasattr(preston, "X"))
        self.assertTrue(hasattr(preston, "Y"))
        self.assertTrue(hasattr(preston, "profile"))
        self.assertTrue(hasattr(preston, "dt"))
        self.assertEqual(preston.dt, 0.1)
