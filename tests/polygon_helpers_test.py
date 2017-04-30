from unittest import TestCase
from unittest.mock import MagicMock

from server import polygons

class PolygonsTestCase(TestCase):

    def test_is_close_enough(self):
        known_input = [
            MagicMock(longitude=55.749982, latitude=37.612350),
            MagicMock(longitude=55.749992, latitude=37.612779),
            MagicMock(longitude=55.749582, latitude=37.611974),
            MagicMock(longitude=55.748264, latitude=37.452187),
            MagicMock(longitude=55.748827, latitude=37.451842),
            MagicMock(longitude=55.746306, latitude=37.711178)
        ]
        self.assertTrue(polygons.is_close_enough(known_input[0], known_input[1]))
        self.assertTrue(polygons.is_close_enough(known_input[1], known_input[2]))
        self.assertTrue(polygons.is_close_enough(known_input[0], known_input[2]))
        self.assertTrue(polygons.is_close_enough(known_input[3], known_input[4]))
        self.assertFalse(polygons.is_close_enough(known_input[2], known_input[3]))
        self.assertFalse(polygons.is_close_enough(known_input[4], known_input[5]))
        self.assertFalse(polygons.is_close_enough(known_input[0], known_input[5]))
            

    def test_group_fire_spots_by_distance(self):
        known_input = [
            MagicMock(longitude=55.749982, latitude=37.612350),
            MagicMock(longitude=55.749992, latitude=37.612779),
            MagicMock(longitude=55.749582, latitude=37.611974),
            MagicMock(longitude=55.748264, latitude=37.452187),
            MagicMock(longitude=55.748827, latitude=37.451842),
            MagicMock(longitude=55.746306, latitude=37.711178)
        ]
        known_output_len = 3
        known_output_set0 = set(known_input[:3])
        known_output_set1 = set(known_input[3:5])
        known_output_set2 = set(known_input[5:])
        output = polygons.group_fire_spots_by_distance(known_input)
        print(known_input)
        print(output)
        self.assertEqual(len(output), known_output_len)
        self.assertEqual(set(output[0]), known_output_set0)
        self.assertEqual(set(output[1]), known_output_set1)
        self.assertEqual(set(output[2]), known_output_set2)

