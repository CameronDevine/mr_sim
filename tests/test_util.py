from context import mr_sim
import unittest


class TestUtil(unittest.TestCase):
    def test_create(self):
        class A:
            a = 1

        class B:
            b = 2

        class C:
            c = 3

        Test = mr_sim.create_simulation(A, B)
        test = Test()
        self.assertEqual(test.a, 1)
        self.assertEqual(test.b, 2)
        self.assertFalse(hasattr(test, "c"))
        Test = mr_sim.create_simulation(A, B, C)
        test = Test()
        self.assertEqual(test.a, 1)
        self.assertEqual(test.b, 2)
        self.assertEqual(test.c, 3)
