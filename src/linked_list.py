"""
Linked list.
Every node has data and reference to the next_ node.
"""


class LinkedElem:
    """
    Class for one-direction nodes
    """
    def __init__(self, data, next_=None):
        self.data = data
        self.next_ = next_

    def get_data(self):
        """
        Returns node's data
        :return: any_type
        """
        return self.data

    def has_next(self):
        """
        Tells if node has reference to the next node
        :return: bool
        """
        return self.next_ is not None


class LinkedList:
    """
    Linked list structure
    """
    def __init__(self, head):
        self.head = head
        self.length = 1
        self.tail = self.head
        self.iter = None

    def __iter__(self):
        self.iter = self.head
        return self

    def __next__(self):
        if self.iter is not None:
            res = self.iter
            iter_next = self.iter.next_
            self.iter = iter_next
            return res
        raise StopIteration

    def input_data(self):
        """
        Adds new elements to hash map.
        User inputs data throughout console till blank line is given.
        Each line represents an element.
        :return: None
        """
        new_data = input()
        while new_data != '':
            self.add_data(new_data)
            new_data = input()
            self.length += 1

    def add_data(self, new_data):
        """
        Adds an element to the end of list.
        :param new_data: data you want to add
        :return: None
        """
        self.tail.next_ = LinkedElem(new_data)
        self.tail = self.tail.next_

    def print_list(self):
        """
        Prints whole linked list
        :return: None
        """
        current = self.head
        while current is not None:
            print(current.data)
            current = current.next_

    def __str__(self):
        string_out = ''
        for node in self:
            string_out += str(node.data) + ' -> '
        return string_out[:-4]

    def max(self):
        """
        Finds max element
        :return: int
        """
        current = self.head
        max_value = current.data
        while current is not None:
            try:
                max_value = max(max_value, int(current.data))
            except TypeError:
                pass
            current = current.next_
        return max_value

    def sum(self):
        """
        Calculates linked list's element sum
        :return: int
        """
        current = self.head
        sum_of_values = 0
        while current is not None:
            try:
                sum_of_values += int(current.data)
            except TypeError:
                pass
            current = current.next_
        return sum_of_values

    def has_negative(self):
        """
        Checks if linked list has a negative value
        :return: bool
        """
        current = self.head
        flag = False
        while current is not None:
            try:
                if current.data < 0:
                    flag = True
            except TypeError:
                pass
            if flag:
                return True
            current = current.next_
        return flag

    def del_head(self):
        """
        Deletes head
        :return: None
        """
        self.head = self.head.next_
        self.length -= 1

    def del_last(self):
        """
        Deletes last element
        :return: None
        """
        current = self.head
        last_index = 0  # made to pass pylint tests :)
        for elem_index in range(self.length - 2):
            last_index = elem_index
            current = current.next_
        current.next_ = None
        self.length -= 1
        last_index -= 1

    def del_penultimate(self):
        """
        Deletes penultimate element
        :return: None
        """
        current = self.head
        last_index = 0  # made to pass pylint tests :)
        for elem_index in range(self.length - 3):
            last_index = elem_index
            current = current.next_
        current.next_ = None
        self.length -= 1
        last_index += 1

    def del_first_by_value(self, value):
        """
        Deletes the first found element with given value
        :param value: value of element
        :return: None
        """
        current = self.head
        previous = LinkedElem(None)
        while current is not None and current.data != value:
            previous = current
            current = current.next_
        if current is not None:
            previous.next_ = current.next_
            del current
            self.length -= 1
        if previous.data is None:
            if self.head.next_ is not None:
                tmp = self.head.next_
                del self.head
                self.head = tmp
            else:
                self.head = None

    def del_all_by_value(self, value):
        """
        Deletes every element with given value
        :param value: value of element
        :return: None
        """
        current = self.head
        previous = LinkedElem(None)
        while self.head is not None and current.data == value:
            current = current.next_
            self.head = current
        while current is not None:
            if current.data == value:
                previous.next_ = current.next_
                self.length -= 1
            else:
                previous = current
            current = current.next_

    def ins_value(self, insert, value):
        """
        Inserts element before element with given value
        :param insert: value of inserted element
        :param value: value of searchable element
        :return: None
        """
        current = self.head
        previous = LinkedElem(None)
        while current is not None and current.data != value:
            previous = current
            current = current.next_
        if current is not None:
            previous.next_ = LinkedElem(insert, previous.next_)
            current.next_ = LinkedElem(insert, current.next_)
            self.length += 2
        if previous.data is None:
            current = self.head
            self.head = LinkedElem(insert, current)

    def input_from_file(self, filename):
        """
        Fills linked list with data given in file
        :param filename: name of file with data
        :return: None
        """
        with open(filename, 'r', encoding='utf8') as file:
            line = file.readline()
            while line != '':
                self.add_data(line[:-1])
                line = file.readline()

    def delete_every_second(self):
        """
        Deletes every second element
        :return: None
        """
        current = self.head
        previous = LinkedElem(None)
        pos = 1
        while current is not None:
            if pos % 2 == 0:
                previous.next_ = current.next_
                self.length -= 1
            else:
                previous = current
            pos += 1
            current = current.next_


if __name__ == '__main__':
    first = LinkedElem([1, 2])
    linked_list = LinkedList(first)
    # linked_list.input_from_file('test.txt')
    # linked_list.input_data()
    linked_list.add_data('5')
    linked_list.add_data('3')
    linked_list.add_data('10')
    print(linked_list)
    # linked_list.delete_every_second()
    linked_list.del_first_by_value([1, 2])
    print(linked_list)
    for el in linked_list:
        print(el.data, end=' -> ')
    # linked_list.ins_value('new', '4')
    # linked_list.print_list()
    # linked_list.add_data('new_data')
    # linked_list.print_list()
    # print(linked_list.max())
    # print(linked_list.sum())
    # print(linked_list.has_negative())
    # linked_list.del_last()
    # linked_list.print_list()
    # head = LinkedElem(1)
    # head.input_next__elem()
    # head.print_from_this()
    # third = LinkedElem(3, None)
    # second = LinkedElem(4, third)
    # first = LinkedElem(5, second)
    # first.print_from_this()
    # linked_list.del_first_by_value('3')
    # linked_list.print_list()
    # print()
    # linked_list.del_all_by_value('1')
