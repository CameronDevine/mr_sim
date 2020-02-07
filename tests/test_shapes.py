from context import mr_sim
import unittest
import numpy as np


class TestRound(unittest.TestCase):
    def test_init(self):
        with self.assertRaises(ValueError):
            mr_sim.Round(1, 1)
        round = mr_sim.Round(1, 1, radius=3)
        self.assertEqual(round.r, 3)
        self.assertAlmostEqual(round.area, 28.27433, 5)
        self.assertAlmostEqual(round.Ix, 63.61725, 5)
        self.assertAlmostEqual(round.Ix, 63.61725, 5)

    def test_setter(self):
        round = mr_sim.Round(1, 1, radius=4)
        round.radius = 5
        self.assertEqual(round.r, 5)
        self.assertAlmostEqual(round.area, 78.53982, 5)
        self.assertAlmostEqual(round.Ix, 490.87385, 5)
        self.assertAlmostEqual(round.Iy, 490.87385, 5)

    def test_getter(self):
        round = mr_sim.Round(1, 1, radius=6)
        self.assertEqual(round.radius, 6)

    def test_base(self):
        round = mr_sim.Round(1, 1, radius=1)
        self.assertTrue(hasattr(round, "X"))
        self.assertTrue(hasattr(round, "Y"))
        self.assertTrue(hasattr(round, "profile"))
        self.assertTrue(hasattr(round, "dt"))

    def test_shape(self):
        round = mr_sim.Round(6, 6, radius=2)
        self.assertTrue(
            np.all((round.X ** 2 + round.Y ** 2)[round.shape(round.X, round.Y)] < 4)
        )
