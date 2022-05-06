"""
testing MappingProtocol
"""
from test import mapping_tests


class GeneralMappingTests(mapping_tests.BasicTestMappingProtocol):
    """
    mocked test_read
    """
    type2test = None

    def test_read(self):
        # Test for read only operations on mapping
        empty_map = self._empty_mapping()
        empty_map1 = dict(empty_map) # workaround for singleton objects
        full_map = self._full_mapping(self.reference)
        if full_map is empty_map:
            empty_map = empty_map1
        #Indexing
        for key, value in self.reference.items():
            self.assertEqual(full_map[key], value)
        knownkey = list(self.other.keys())[0]
        self.assertRaises(KeyError, lambda:full_map[knownkey])
        #len
        self.assertEqual(len(empty_map), 0)
        self.assertEqual(len(full_map), len(self.reference))
        #__contains__
        for k in self.reference:
            self.assertIn(k, full_map)
        for k in self.other:
            self.assertNotIn(k, full_map)
        #cmp
        self.assertEqual(empty_map, empty_map)
        self.assertEqual(full_map, full_map)
        self.assertNotEqual(empty_map, full_map)
        self.assertNotEqual(full_map, empty_map)
        #bool
        if empty_map:
            self.fail("Empty mapping must compare to False")
        if not full_map:
            self.fail("Full mapping must compare to True")

        # keys(), items(), iterkeys() ...
        def check_iterandlist(itr, lst, ref):
            self.assertTrue(hasattr(itr, '__next__'))
            self.assertTrue(hasattr(itr, '__iter__'))
            itr_list = list(itr)
            self.assertTrue(set(itr_list) == set(lst) == set(ref))
        check_iterandlist(iter(full_map.keys()), list(full_map.keys()),
                          self.reference.keys())
        check_iterandlist(iter(full_map.keys()), list(full_map.keys()), self.reference.keys())
        check_iterandlist(iter(full_map.values()), list(full_map.values()),
                          self.reference.values())
        check_iterandlist(iter(full_map.items()), list(full_map.items()),
                          self.reference.items())
        #get
        key, value = next(iter(full_map.items()))
        knownkey, knownvalue = next(iter(self.other.items()))
        self.assertEqual(full_map.get(key, knownvalue), value)
        self.assertEqual(full_map.get(knownkey, knownvalue), knownvalue)
        self.assertNotIn(knownkey, full_map)
