import unittest
from map_tests import MapTesting
from src.tree_map import TreeMap


class BinaryTreeTesting(MapTesting, unittest.TestCase):
    def setUp(self):
        self.map = TreeMap()

    def test_less_in_left(self):
        self.map[8] = 'root'
        self.map[7] = 'left'
        self.assertEqual(self.map[7], self.map.root.left.value)

    def test_more_in_right(self):
        self.map[8] = 'root'
        self.map[10] = 'right'
        self.assertEqual(self.map[10], self.map.root.right.value)

    def test_string_keys(self):
        self.map['b'] = 'root'
        self.map['a'] = 1
        self.assertEqual(self.map['a'], self.map.root.left.value)


if __name__ == '__main__':
    unittest.main()
