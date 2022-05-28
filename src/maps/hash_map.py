"""
Hash map.
Every node of hash map has key and value (some data).
Based on default list but key is calculated according to
key's hash value
"""
from random import randint  # for tests
from maps.linked_list import LinkedElem, LinkedList
from maps.base_map import BaseMap


class HashMap(BaseMap):
    """
    Hash map data structure class
    """
    def __init__(self, _capacity=10):
        self._inner_list = [None] * _capacity
        self._capacity = _capacity
        self._size = 0

    def __getitem__(self, key):
        hashed_key = hash(key) % self._capacity
        if self._inner_list[hashed_key] is not None:
            for node_key, node_value in self._inner_list[hashed_key]:
                if node_key == key:
                    return node_value
        raise KeyError('Such key does not exists')

    def __setitem__(self, key, value):
        hashed_key = hash(key) % self._capacity
        if self._inner_list[hashed_key] is not None:
            to_add = True
            for node_key, node_value in self._inner_list[hashed_key]:
                if node_key == key:
                    self._inner_list[hashed_key].set_data(key, value)
                    self._size -= 1  # when the key exists the _size shouldn't be increased
                    to_add = False
                    break
            if to_add:
                self._inner_list[hashed_key].add_data(key, value)
        else:
            self._inner_list[hashed_key] = LinkedList(LinkedElem(key, value))
        self._size += 1

        if self._size >= 0.7 * self._capacity:  # list extension when more than 70% is filled
            self._capacity *= 2
            new_inner_list = [None] * self._capacity
            for elem in self._inner_list:
                if elem is not None:
                    for node_key, node_value in elem:
                        hashed_key = hash(node_key) % self._capacity
                        if new_inner_list[hashed_key] is not None:
                            new_inner_list[hashed_key].add_data(node_key, node_value)
                        else:
                            new_inner_list[hashed_key] \
                                = LinkedList(LinkedElem(node_key, node_value))
            self._inner_list = new_inner_list

    def __delitem__(self, key):
        hashed_key = hash(key) % self._capacity
        if self._inner_list[hashed_key] is not None:
            self._inner_list[hashed_key].del_first_by_key(key)
            self._size -= 1
        else:
            raise KeyError

        if self._size <= 0.3 * self._capacity:  # list shortening less than 30% is filled
            self._capacity //= 2
            new_inner_list = [None] * self._capacity
            for elem in self._inner_list:
                if elem is not None:
                    for node_key, node_value in elem:
                        hashed_key = hash(node_key) % self._capacity
                        if new_inner_list[hashed_key] is not None:
                            new_inner_list[hashed_key].add_data(node_key, node_value)
                        else:
                            new_inner_list[hashed_key] \
                                = LinkedList(LinkedElem(node_key, node_value))
            self._inner_list = new_inner_list

    def __iter__(self):
        for elem in self._inner_list:
            if elem is not None:
                yield from elem or []

    def __str__(self):
        string = ', '.join(f'{key}: {value}' for key, value in self)
        return '{' + string + '}'

    __repr__ = __str__

    def __len__(self) -> int:
        return self._size

    def sort(self, reverse=False):
        """
        Sorts hash map by keys
        :return: sorted list
        """
        return sorted(self, key=lambda elem: elem[0], reverse=reverse)

    def clear(self):
        """Clears hash map"""
        self._capacity = 10
        self._inner_list = [None] * self._capacity
        self._size = 0

    def to_string(self):  # for serialization
        """
        Method that serializes hash map's data
        :return: string
        """
        string = '\n'.join(' -> '.join(f'{key}:{value}' for key, value in elem)
                           for elem in self._inner_list if elem is not None)
        return string

    def get_capacity(self):
        """
        Gets inner list's capacity
        :return: int
        """
        return self._capacity

    def write_in_line(self, filename):
        """
        Writes hash map in file in a pretty way
        :return: None
        """
        with open(filename, 'a', encoding='utf8') as file:
            file.write(str(self))


if __name__ == '__main__':
    hash_map = HashMap()
    for el in 'abcdefghijk':
        hash_map[el] = randint(1, 100)
    print(hash_map)
    print(hash_map.to_string())
