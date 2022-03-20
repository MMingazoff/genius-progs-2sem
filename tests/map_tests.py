from abc import ABC


class MapTesting(ABC):

    map_cls = None

    def setUp(self):
        self.map = map_cls()

    def test_set_get_item(self):
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
        with self.assertRaises(KeyError):
            i = self.map[0]

    def test_rewrite_value(self):
        self.map[1] = 'old value'
        self.map[1] = 'new value'
        self.assertEqual(self.map[1], 'new value')


if __name__ == '__main__':
    pass

