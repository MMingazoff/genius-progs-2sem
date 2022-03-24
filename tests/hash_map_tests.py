"""
Module for testing hash map data structure
"""
import unittest
from map_tests import MapTesting
from src.hash_map import HashMap


class HashMapTesting(MapTesting, unittest.TestCase):
    """
    Class for testing hash map methods
    """
    map_cls = HashMap

    def test_deletion(self):
        """
        Checks if deletion actually deletes element
        :return: None
        """
        self.map[1] = 'first'
        self.map[0] = 'will be deleted'
        del self.map[0]
        with self.assertRaises(KeyError):
            non_existing = self.map[0]
            non_existing += 1

    def test_inner_list_reduction(self):
        """
        Checks if inner list of hash map is reduced
        when less than 30% of list is filled
        :return: None
        """
        self.map[1] = 'first'
        self.map[2] = 'second'
        self.map[3] = 'temp'
        old_capacity = self.map.get_capacity()
        del self.map[3]
        new_capacity = self.map.get_capacity()
        self.assertLess(new_capacity, old_capacity)

    def test_inner_list_expansion(self):
        """
        Checks if inner list of hash map is expanded
        when more than 70% of list is filled
        :return: None
        """
        old_capacity = self.map.get_capacity()
        for i in range(self.map.get_capacity() - 1):
            self.map[i] = i*i
        new_capacity = self.map.get_capacity()
        self.assertLess(old_capacity, new_capacity)

    def test_same_size_when_rewritten(self):
        """
        Checks if size (number of elements) doesn't change
        when element's value is rewritten
        :return: None
        """
        self.map[1] = 'first'
        self.map[2] = 'second'
        old_size = len(self.map)
        self.map[2] = 'new second'
        new_size = len(self.map)
        self.assertEqual(old_size, new_size)


if __name__ == '__main__':
    unittest.main()
