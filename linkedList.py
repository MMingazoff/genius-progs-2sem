class LinkedElem:
    def __init__(self, data, next=None):
        self.data = data
        self.next = next


class LinkedList:
    def __init__(self, head):
        self.head = head
        self.length = 1
        self.tail = self.head
        self.iter = self.head

    def __iter__(self):
        return self

    def __next__(self):
        if self.iter is not None:
            res = self.iter
            self.iter = self.iter.next
            return res
        else:
            self.iter = self.head
            raise StopIteration

    def input_data(self):
        new_data = input()
        # current = self.head
        while new_data != '':
            # current.next = LinkedElem(new_data)
            self.add_data(new_data)
            new_data = input()
            # current = current.next
            self.length += 1
        # self.tail = current

    def add_data(self, new_data):
        self.tail.next = LinkedElem(new_data)
        self.tail = self.tail.next
        # for i in range(self.length - 1):
        #     current = current.next
        # current.next = LinkedElem(new_data)

    def print_list(self):
        current = self.head
        while current is not None:
            print(current.data)
            current = current.next

    def max(self):
        current = self.head
        max_value = current.data
        while current is not None:
            try:
                max_value = max(max_value, int(current.data))
            except:
                pass
            current = current.next
        return max_value

    def sum(self):
        current = self.head
        sum_of_values = 0
        while current is not None:
            try:
                sum_of_values += int(current.data)
            except:
                pass
            current = current.next
        return sum_of_values

    def has_negative(self):
        current = self.head
        flag = False
        while current is not None:
            try:
                if current.data < 0:
                    flag = True
            except:
                pass
            if flag:
                return True
            current = current.next
        return flag

    def del_head(self):
        self.head = self.head.next
        self.length -= 1

    def del_last(self):
        current = self.head
        for i in range(self.length - 2):
            current = current.next
        current.next = None
        self.length -= 1

    def del_penultimate(self):
        current = self.head
        for i in range(self.length - 3):
            current = current.next
        current.next = None
        self.length -= 1

    def del_first_by_value(self, value):
        current = self.head
        previous = LinkedElem(None)
        while current is not None and current.data != value:
            previous = current
            current = current.next
        if current is not None:
            previous.next = current.next
            self.length -= 1
        if previous.data is None:
            if self.head.next is not None:
                self.head = self.head.next
            else:
                self.head = None

    def del_all_by_value(self, value):
        current = self.head
        previous = LinkedElem(None)
        while self.head is not None and current.data == value:
            current = current.next
            self.head = current
        while current is not None:
            if current.data == value:
                previous.next = current.next
                self.length -= 1
            else:
                previous = current
            current = current.next

    def ins_value(self, insert, value):
        current = self.head
        previous = LinkedElem(None)
        while current is not None and current.data != value:
            previous = current
            current = current.next
        if current is not None:
            previous.next = LinkedElem(insert, previous.next)
            current.next = LinkedElem(insert, current.next)
            self.length += 2
        if previous.data is None:
            current = self.head
            self.head = LinkedElem(insert, current)

    def input_from_file(self, filename):
        with open(filename) as file:
            line = file.readline()
            while line != '':
                self.add_data(line[:-1])
                line = file.readline()

    def delete_every_second(self):
        current = self.head
        previous = LinkedElem(None)
        pos = 1
        while current is not None:
            if pos % 2 == 0:
                previous.next = current.next
                self.length -= 1
            else:
                previous = current
            pos += 1
            current = current.next


if __name__ == '__name__':
    first = LinkedElem('1')
    linked_list = LinkedList(first)
    linked_list.input_from_file('test.txt')
    # linked_list.input_data()
    linked_list.add_data('5')
    linked_list.add_data('3')
    linked_list.add_data('10')
    linked_list.print_list()
    # linked_list.delete_every_second()
    print()
    linked_list.print_list()
    print()
    for el in linked_list:
        print(el.data, end=' ')

    for el in linked_list:
        print(el.data, end=' ')
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
    # head.input_next_elem()
    # head.print_from_this()
    # third = LinkedElem(3, None)
    # second = LinkedElem(4, third)
    # first = LinkedElem(5, second)
    # first.print_from_this()
    # linked_list.del_first_by_value('3')
    # linked_list.print_list()
    # print()
    # linked_list.del_all_by_value('1')
    # linked_list.print_list()
    # new_data = int(new_data) if new_data.isdigit() or new_data[0] == '-' and new_data[1:].isdigit() else new_data
    # if convert_to_int and (new_data.isdigit() or new_data[0] == '-' and new_data[1:].isdigit()):
    #     new_data = int(new_data)