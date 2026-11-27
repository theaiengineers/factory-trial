import unittest

from units import length


class Length(unittest.TestCase):
    def test_a_marathon(self):
        self.assertAlmostEqual(length.miles_to_km(26.21875), 42.195, places=3)

    def test_round_trip(self):
        self.assertAlmostEqual(length.km_to_miles(length.miles_to_km(3)), 3)

    def test_km_to_metres_of_nothing(self):
        self.assertEqual(length.km_to_metres(0), 0)
