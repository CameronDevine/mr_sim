from context import mr_sim
import unittest
import numpy as np


class TestOrbital(unittest.TestCase):
    def test_error(self):
        with self.assertRaises(ValueError):
            mr_sim.Orbital(1, 1)

    def test_init(self):
        orbital = mr_sim.Orbital(1, 1, eccentricity=3)
        self.assertEqual(orbital.eccentricity, 3)

    def test_setter(self):
        orbital = mr_sim.Orbital(1, 1, eccentricity=2)
        orbital.set_speed(rotational_speed=1)
        self.assertEqual(orbital.rotational_speed, 1)
        orbital.set_speed(orbital_speed=2)
        self.assertEqual(orbital.orbital_speed, 2)
        orbital.set_speed(3, 4)
        self.assertEqual(orbital.orbital_speed, 3)
        self.assertEqual(orbital.rotational_speed, 4)
        orbital.set_speed(5)
        self.assertEqual(orbital.orbital_speed, 5)

    def test_velocity(self):
        orbital = mr_sim.Orbital(2, 2, eccentricity=0.01)
        orbital.set_speed(7, 8)
        orbital.set_velocity(2, 3)
        self.assertTrue(
            np.allclose(
                orbital.velocity(orbital.X, orbital.Y),
                np.sqrt(
                    (0.01 * 7) ** 2
                    + (np.sqrt(orbital.X**2 + orbital.Y**2) * 8) ** 2
                ),
            )
        )

    def test_base(self):
        orbital = mr_sim.Orbital(1, 1, eccentricity=1, dt=5)
        self.assertTrue(hasattr(orbital, "X"))
        self.assertTrue(hasattr(orbital, "Y"))
        self.assertTrue(hasattr(orbital, "profile"))
        self.assertTrue(hasattr(orbital, "dt"))
        self.assertEqual(orbital.dt, 5)


class TestBelt(unittest.TestCase):
    def test_init(self):
        belt = mr_sim.Belt(1, 1)
        self.assertTrue(hasattr(belt, "speed"))

    def test_setter(self):
        belt = mr_sim.Belt(1, 1)
        belt.set_speed(2)
        self.assertEqual(belt.speed, 2)

    def test_velocity(self):
        belt = mr_sim.Belt(2, 2)
        belt.set_speed(4)
        belt.set_velocity(5, 7)
        self.assertTrue(np.allclose(belt.velocity(belt.X, belt.Y), 4))

    def test_base(self):
        belt = mr_sim.Belt(1, 1, dt=2)
        self.assertTrue(hasattr(belt, "X"))
        self.assertTrue(hasattr(belt, "Y"))
        self.assertTrue(hasattr(belt, "profile"))
        self.assertTrue(hasattr(belt, "dt"))
        self.assertEqual(belt.dt, 2)


class TestRotary(unittest.TestCase):
    def test_init(self):
        rotary = mr_sim.Rotary(1, 1)
        self.assertTrue(hasattr(rotary, "speed"))

    def test_setter(self):
        rotary = mr_sim.Rotary(1, 1)
        rotary.set_speed(3)
        self.assertEqual(rotary.speed, 3)

    def test_velocity(self):
        rotary = mr_sim.Rotary(2, 2)
        rotary.set_speed(5)
        rotary.set_velocity(4, 2)
        self.assertTrue(
            np.allclose(
                rotary.velocity(rotary.X, rotary.Y),
                np.sqrt(rotary.X**2 + rotary.Y**2) * 5,
            )
        )

    def test_base(self):
        rotary = mr_sim.Rotary(1, 1, dt=3)
        self.assertTrue(hasattr(rotary, "X"))
        self.assertTrue(hasattr(rotary, "Y"))
        self.assertTrue(hasattr(rotary, "profile"))
        self.assertTrue(hasattr(rotary, "dt"))
        self.assertEqual(rotary.dt, 3)
