"""
Module for testing map data structures
"""
from test import mapping_tests
from abc import ABC


class MapTesting(ABC, mapping_tests.BasicTestMappingProtocol):
    """
    Abstract class with basic tests for maps
    """
    type2test = ABC

    def setUp(self):
        """
        Makes a map class instance
        :return: None
        """
        self.map = self.type2test()

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

    def test_read_data(self):
        """
        Checks if function reads data from file properly
        :return: None
        """
        filepath = 'files/to_read.txt'
        self.map = self.map.read(filepath)
        self.assertEqual(len(self.map), 3)
        self.assertEqual(self.map['babagi'], 'fortaite')

    def test_write_data(self):
        """
        Checks if function writes data in file properly
        :return: None
        """
        filepath = 'files/to_write.txt'
        self.map[1] = 'first'
        self.map[2] = 'second'
        self.map.write(filepath, 'w')
        with open(filepath, 'r', encoding='utf8') as file:
            line = file.readline()
            while line != '':
                key, value = line.split()
                key = int(key[:-1])
                self.assertEqual(value, self.map[key])
                line = file.readline()


if __name__ == '__main__':
    pass
