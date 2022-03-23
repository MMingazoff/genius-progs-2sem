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

    def test_del_leaf(self):
        self.map[5] = 'root'
        self.map[8] = 'right'
        self.map[4] = 'left'
        self.map[12] = 'right->right'
        del self.map[12]
        self.assertEqual(self.map.root.right.right, None)

    def test_del_node_with_one_child(self):
        self.map[33] = 'root'
        self.map[35] = 'right'
        self.map[5] = 'left'
        self.map[17] = 'left->right'
        self.map[18] = 'left->right->right'
        self.map[1] = 'left->left'
        self.map[4] = 'left->left->right'
        del self.map[17]
        self.assertEqual(self.map.root.left.right.value, self.map[18])
        del self.map[1]
        self.assertEqual(self.map.root.left.left.value, 'left->left->right')

    def test_del_node_with_two_children(self):
        self.map[10] = 'root'
        self.map[7] = 'left'
        self.map[12] = 'right'
        self.map[9] = 'left->right'
        self.map[8] = 'left->right->left'
        self.map[6] = 'left->left'
        del self.map[7]
        self.assertEqual(self.map.root.left.value, 'left->right->left')
        self.assertEqual(self.map.root.left.right.value, 'left->right')
        self.assertIs(self.map.root.left.right.left, None)


if __name__ == '__main__':
    unittest.main()
