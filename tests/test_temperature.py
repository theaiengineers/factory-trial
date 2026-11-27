import unittest

from units import temperature


class Temperature(unittest.TestCase):
    def test_freezing_and_boiling(self):
        self.assertEqual(temperature.c_to_f(0), 32)
        self.assertEqual(temperature.c_to_f(100), 212)

    def test_round_trip(self):
        self.assertAlmostEqual(temperature.f_to_c(temperature.c_to_f(37.5)), 37.5)

    def test_kelvin_round_trip(self):
        self.assertAlmostEqual(temperature.k_to_c(temperature.c_to_k(21.5)), 21.5)
        self.assertAlmostEqual(temperature.k_to_c(0), -273.15)


if __name__ == "__main__":
    unittest.main()
