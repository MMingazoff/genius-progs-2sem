from linkedList import LinkedElem, LinkedList


class HashMap:

    def __init__(self, _size=10):
        self._inner_list = [None] * _size
        self._size = _size
        self._cnt = 0

    def __getitem__(self, key):
        # if self._inner_list[hash(key) % self._size] is not None:
        #     return self._inner_list[hash(key) % self._size][1]
        # return None

        if self._inner_list[hash(key) % self._size] is not None:
            for node in self._inner_list[hash(key) % self._size]:
                if node.data[0] == key:
                    return node.data[1]
        return None

    def __setitem__(self, key, value):
        if self._inner_list[hash(key) % self._size] is not None:
            self._inner_list[hash(key) % self._size].add_data((key, value))
        else:
            self._inner_list[hash(key) % self._size] = LinkedList(LinkedElem((key, value)))
        self._cnt += 1

        if self._cnt >= 0.6 * self._size:
            self._size = self._size * 2
            # new_inner_list = [None] * self._size
            # for key, value in self._inner_list:
            #     new_inner_list[hash(key) % self._size] = (key, value)
            self._inner_list = self._inner_list + [None for i in range(self._size * 2 - self._cnt)]

    # def __delitem__(self, key):

    def __str__(self):
        string = '{'
        for elem in self._inner_list:
            if elem is not None:
                for node in elem:
                    string += f'{node.data[0]}:{node.data[1]}; '  # key, value
        return string[:-2] + '}'


if __name__ == '__main__':
    hash_map = HashMap()
    hash_map[5] = 1
    hash_map[5.4] = 2
    hash_map['bb'] = 'booba'
    # del hash_map[5]
    print(hash_map)
