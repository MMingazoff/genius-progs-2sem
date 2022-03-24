"""
Hash map.
Every node of hash map has key and value (some data).
Based on default list but key is calculated according to
key's hash value
"""
from src.linked_list import LinkedElem, LinkedList


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

    def __str__(self):
        string = '{'
        for elem in self._inner_list:
            if elem is not None:
                for node in elem:
                    string += f'{node.data[0]}:{node.data[1]}; '  # key, value
        string = '{  ' if string == '{' else string
        return string[:-2] + '}'

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


if __name__ == '__main__':
    hash_map = HashMap()
    hash_map[5] = 1
    hash_map[5.4] = 2
    hash_map['bb'] = 'aboba'
    hash_map['bb'] = 'notaboba'
    hash_map['last'] = 'ultralast'
    print(hash_map)
    print(len(hash_map))
    for letter in 'abcdefgh':
        hash_map[letter] = ord(letter)
    print('---extension---')
    print(hash_map)
    print(len(hash_map))
    del hash_map['bb']
    for letter in 'abcdefgh':
        del hash_map[letter]
    print('---deletion---')
    print(hash_map)
    print(len(hash_map))
    del hash_map[5.1]
    print(0)
