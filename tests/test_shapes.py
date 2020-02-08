from context import mr_sim
import unittest
import numpy as np


class TestRound(unittest.TestCase):
    def test_error(self):
        with self.assertRaises(ValueError):
            mr_sim.Round(1, 1)

    def test_init(self):
        round = mr_sim.Round(1, 1, radius=3)
        self.assertEqual(round.r, 3)
        self.assertAlmostEqual(round.area, 28.27433, 5)
        self.assertAlmostEqual(round.Ix, 63.61725, 5)
        self.assertAlmostEqual(round.Iy, 63.61725, 5)

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
        round = mr_sim.Round(1, 1, radius=1, dt=5)
        self.assertTrue(hasattr(round, "X"))
        self.assertTrue(hasattr(round, "Y"))
        self.assertTrue(hasattr(round, "profile"))
        self.assertTrue(hasattr(round, "dt"))
        self.assertEqual(round.dt, 5)

    def test_shape(self):
        round = mr_sim.Round(6, 6, radius=2)
        self.assertTrue(
            np.all(((round.X ** 2 + round.Y ** 2) < 4)[round.shape(round.X, round.Y)])
        )
        self.assertTrue(
            np.all(((round.X ** 2 + round.Y ** 2) > 4)[~round.shape(round.X, round.Y)])
        )


class TestSquare(unittest.TestCase):
    def test_error(self):
        with self.assertRaises(ValueError):
            mr_sim.Round(1, 1)

    def test_init(self):
        square = mr_sim.Square(1, 1, width=3)
        self.assertEqual(square.width, 3)
        self.assertEqual(square.height, 3)
        self.assertEqual(square.area, 9)
        self.assertAlmostEqual(square.Ix, 6.75)
        self.assertAlmostEqual(square.Iy, 6.75)

    def test_setter(self):
        square = mr_sim.Square(1, 1, width=4)
        square.set_size(5)
        self.assertEqual(square.width, 5)
        self.assertEqual(square.height, 5)
        self.assertEqual(square.area, 25)
        self.assertAlmostEqual(square.Ix, 52.08333, 5)
        self.assertAlmostEqual(square.Iy, 52.08333, 5)

    def test_base(self):
        square = mr_sim.Square(1, 1, width=1, dt=4)
        self.assertTrue(hasattr(square, "X"))
        self.assertTrue(hasattr(square, "Y"))
        self.assertTrue(hasattr(square, "profile"))
        self.assertTrue(hasattr(square, "dt"))
        self.assertEqual(square.dt, 4)

    def test_shape(self):
        square = mr_sim.Square(6, 6, width=2)
        self.assertTrue(
            np.all(
                ((square.X < 1) & (square.X > -1) & (square.Y < 1) & (square.Y > -1))[
                    square.shape(square.X, square.Y)
                ]
            )
        )
        self.assertTrue(
            np.all(
                ((square.X > 1) | (square.X < -1) | (square.Y > 1) | (square.Y < -1))[
                    ~square.shape(square.X, square.Y)
                ]
            )
        )


class TestRectangle(unittest.TestCase):
    def test_error(self):
        with self.assertRaises(ValueError):
            mr_sim.Rectangular(1, 1)
        with self.assertRaises(ValueError):
            mr_sim.Rectangular(1, 1, width=1)
        with self.assertRaises(ValueError):
            mr_sim.Rectangular(1, 1, height=1)

    def test_init(self):
        rectangle = mr_sim.Rectangular(1, 1, width=3, height=5)
        self.assertEqual(rectangle.width, 3)
        self.assertEqual(rectangle.height, 5)
        self.assertEqual(rectangle.area, 15)
        self.assertAlmostEqual(rectangle.Ix, 31.25)
        self.assertAlmostEqual(rectangle.Iy, 11.25)

    def test_setter(self):
        rectangle = mr_sim.Rectangular(1, 1, width=5, height=5)
        rectangle.set_size(6, 4)
        self.assertEqual(rectangle.width, 6)
        self.assertEqual(rectangle.height, 4)
        self.assertEqual(rectangle.area, 24)
        self.assertAlmostEqual(rectangle.Ix, 32)
        self.assertAlmostEqual(rectangle.Iy, 72)

    def test_base(self):
        rectangle = mr_sim.Rectangular(1, 1, width=1, height=1, dt=0.2)
        self.assertTrue(hasattr(rectangle, "X"))
        self.assertTrue(hasattr(rectangle, "Y"))
        self.assertTrue(hasattr(rectangle, "profile"))
        self.assertTrue(hasattr(rectangle, "dt"))
        self.assertEqual(rectangle.dt, 0.2)

    def test_shape(self):
        rectangle = mr_sim.Rectangular(6, 6, width=4, height=3)
        self.assertTrue(
            np.all(
                (
                    (rectangle.X < 2)
                    & (rectangle.X > -2)
                    & (rectangle.Y < 1.5)
                    & (rectangle.Y > -1.5)
                )[rectangle.shape(rectangle.X, rectangle.Y)]
            )
        )
        self.assertTrue(
            np.all(
                (
                    (rectangle.X > 2)
                    | (rectangle.X < -2)
                    | (rectangle.Y > 1.5)
                    | (rectangle.Y < -1.5)
                )[~rectangle.shape(rectangle.X, rectangle.Y)]
            )
        )
