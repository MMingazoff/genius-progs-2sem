"""
Hash map.
Every node of hash map has key and value (some data).
Based on default list but key is calculated according to
key's hash value
"""
from src.linked_list import LinkedElem, LinkedList
from random import randint  # for tests


class HashMap:
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
            for node in self._inner_list[hashed_key]:
                if node.data[0] == key:
                    return node.data[1]
        raise KeyError('Such key does not exists')

    def __setitem__(self, key, value):
        hashed_key = hash(key) % self._capacity
        if self._inner_list[hashed_key] is not None:
            to_add = True
            for node in self._inner_list[hashed_key]:
                if node.data[0] == key:
                    node.data[1] = value
                    self._size -= 1  # when the key exists the size shouldn't be increased
                    to_add = False
                    break
            if to_add:
                self._inner_list[hashed_key].add_data([key, value])
        else:
            self._inner_list[hashed_key] = LinkedList(LinkedElem([key, value]))
        self._size += 1

        if self._size >= 0.7 * self._capacity:  # list extension when more than 70% is filled
            self._capacity *= 2
            new_inner_list = [None] * self._capacity
            for elem in self._inner_list:
                if elem is not None:
                    for node in elem:
                        hashed_key = hash(node.data[0]) % self._capacity
                        if new_inner_list[hashed_key] is not None:
                            new_inner_list[hashed_key].add_data(node.data)
                        else:
                            new_inner_list[hashed_key] = LinkedList(LinkedElem(node.data))
            self._inner_list = new_inner_list

    def __delitem__(self, key):
        hashed_key = hash(key) % self._capacity
        value = self[key]
        if self._inner_list[hashed_key] is not None:
            self._inner_list[hashed_key].del_first_by_value([key, value])
            self._size -= 1

        if self._size <= 0.3 * self._capacity:  # list shortening less than 30% is filled
            self._capacity //= 2
            new_inner_list = [None] * self._capacity
            for elem in self._inner_list:
                if elem is not None:
                    for node in elem:
                        hashed_key = hash(node.data[0]) % self._capacity
                        if new_inner_list[hashed_key] is not None:
                            new_inner_list[hashed_key].add_data(node.data)
                        else:
                            new_inner_list[hashed_key] = LinkedList(LinkedElem(node.data))
            self._inner_list = new_inner_list

    def __iter__(self):
        for elem in self._inner_list:
            if elem is not None:
                yield from elem

    def __str__(self):
        string = '{'
        for elem in self._inner_list:
            if elem is not None:
                for node in elem:
                    string += f'{node.data[0]}:{node.data[1]}; '  # key, value
        string = '{  ' if string == '{' else string
        return string[:-2] + '}'

    def sort(self, reverse=False):
        """
        Sorts hash map by values
        :return: sorted list
        """
        return sorted(self, key=lambda el: el.data[1], reverse=reverse)

    def get(self, key, default=None):
        """
        Returns value of key if it exists.
        If not - returns default value.
        :return: value of key or default
        """
        try:
            value = self[key]
        except KeyError:
            return default
        return value

    def to_string(self):  # for serialization
        """
        Method that serializes hash map's data
        :return: string
        """
        string = ''
        for elem in self._inner_list:
            if elem is not None:
                for node in elem:
                    string += f'{node.data[0]}:{node.data[1]} -> '
                string = string[:-4]
            string += '\n'
        return string

    def __len__(self):
        return self._size

    def get_capacity(self):
        """
        Gets inner list's capacity
        :return: int
        """
        return self._capacity

    def write_in_file(self, filename):
        """
        Writes hash map in file in a pretty way
        :return: None
        """
        with open(filename, 'a', encoding='utf8') as file:
            file.write('{')
            for elem in self:
                file.write(f'{elem.data[0]}:{elem.data[1]}; ')
            file.write('}\n')


if __name__ == '__main__':
    hash_map = HashMap()
    for el in 'abcdefghijk':
        hash_map[el] = randint(1, 100)
    print(hash_map.sort())
