import unittest
from src.hash_map import HashMap
from map_tests import MapTesting


class HashMapTesting(MapTesting, unittest.TestCase):

    def setUp(self):
        self.map = HashMap()

    def test_deletion(self):
        self.map[1] = 'first'
        self.map[0] = 'will be deleted'
        del self.map[0]
        with self.assertRaises(KeyError):
            i = self.map[0]

    def test_inner_list_reduction(self):
        self.map[1] = 'first'
        self.map[2] = 'second'
        self.map[3] = 'temp'
        old_capacity = self.map.get_capacity()
        del self.map[3]
        new_capacity = self.map.get_capacity()
        self.assertLess(new_capacity, old_capacity)

    def test_inner_list_expansion(self):
        old_capacity = self.map.get_capacity()
        for i in range(self.map.get_capacity() - 1):
            self.map[i] = i*i
        new_capacity = self.map.get_capacity()
        self.assertLess(old_capacity, new_capacity)

    def test_same_size_when_rewritten(self):
        self.map[1] = 'first'
        self.map[2] = 'second'
        old_size = len(self.map)
        self.map[2] = 'new second'
        new_size = len(self.map)
        self.assertEqual(old_size, new_size)


if __name__ == '__main__':
    unittest.main()

