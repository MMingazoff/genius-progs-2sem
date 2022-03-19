from linkedList import LinkedElem, LinkedList


class HashMap:

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
        return None

    def __setitem__(self, key, value):
        hashed_key = hash(key) % self._capacity
        if self._inner_list[hashed_key] is not None:
            to_add = True
            for node in self._inner_list[hashed_key]:
                if node.data[0] == key:
                    node.data[1] = value
                    to_add = False
                    break
            if to_add:
                self._inner_list[hashed_key].add_data([key, value])
        else:
            self._inner_list[hashed_key] = LinkedList(LinkedElem([key, value]))
            self._size += 1

        if self._size >= 0.6 * self._capacity:  # list extension when 60% is filled
            self._capacity *= 2
            new_inner_list = [None] * self._capacity
            for key, value in self._inner_list:
                new_inner_list[hash(key) % self._capacity] = [key, value]

    def __delitem__(self, key):
        hashed_key = hash(key) % self._capacity
        value = self[hashed_key]
        if self._inner_list[hashed_key] is not None:
            self._inner_list[hashed_key].del_first_by_value([key, value])
            self._size -= 1

        # if self._size <= 0.2 * self._capacity:
        #     self._capacity //= 2
        #     new_inner_list = [None] * self._capacity
        #     for elem in self._inner_list:
        #         new_inner_list[hash()]

    # def __iter__(self):
    #     # self.iter = None
    #     return self
    #
    # def __next__(self):
    #     for elem in self._inner_list:
    #         if elem is not None:
    #             for node in elem:
    #                 yield node

    def __str__(self):
        string = '{'
        for elem in self._inner_list:
            if elem is not None:
                for node in elem:
                    string += f'{node.data[0]}:{node.data[1]}; '  # key, value
        string = '{  ' if string == '{' else string
        return string[:-2] + '}'

    def __repr__(self):  # типо сериализация
        string = ''
        for elem in self._inner_list:
            if elem is not None:
                for node in elem:
                    string += f'{node.data[0]}:{node.data[1]} -> '
                string = string[:-4]
            string += '\n'
        return string


if __name__ == '__main__':
    hash_map = HashMap()
    hash_map[5] = 1
    hash_map[5.4] = 2
    hash_map['bb'] = 'aboba'
    hash_map['bb'] = 'notaboba'
    hash_map['last'] = 'ultralast'
    # print(hash_map.__repr__())
    print(hash_map)
    del hash_map[5]
    print('----------')
    for el in hash_map:
        print(el)
    # print(hash_map.__repr__())
    # print(hash_map._inner_list[hash('bb') % hash_map._size])
