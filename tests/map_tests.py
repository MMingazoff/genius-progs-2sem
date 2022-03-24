"""
Module for testing map data structures
"""
import unittest
from abc import ABC


class MapTesting(ABC, unittest.TestCase):
    """
    Abstract class with basic tests for maps
    """
    map_cls = ABC

    def setUp(self):
        """
        Makes a map class instance
        :return: None
        """
        self.map = self.map_cls()

    def test_set_get_item(self):
        """
        Tests set/get item methods
        :return: None
        """
        # test to set first key - value
        self.map[1] = 'first'
        self.assertEqual(self.map[1], 'first')
        # test to set second key - value
        self.map[10] = 'second'
        self.assertEqual(self.map[10], 'second')
        # test to rewrite value of existing key
        self.map[1] = 'rewritten'
        self.assertEqual(self.map[1], 'rewritten')

    def test_raise_key_error(self):
        """
        Checks if error is raised when key doesn't exist
        :return: None
        """
        with self.assertRaises(KeyError):
            non_existing = self.map[0]
            non_existing += 1

    def test_rewrite_value(self):
        """
        Checks if value of element with existing key is rewritten
        and new element is not created
        :return: None
        """
        self.map[1] = 'old value'
        self.map[1] = 'new value'
        self.assertEqual(self.map[1], 'new value')


if __name__ == '__main__':
    pass
