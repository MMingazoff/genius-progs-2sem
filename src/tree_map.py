class Node:
    def __init__(self, key, value, left=None, right=None):
        self.key = key
        self.value = value
        self.left = left
        self.right = right


class TreeMap:
    def __init__(self, root=None):
        self.root = root

    def __setitem__(self, key, value):
        curr = self.root
        while curr is not None:
            if key > curr.key:
                if curr.right is None:
                    curr.right = Node(key, value)
                    return True
                else:
                    curr = curr.right
            elif key < curr.key:
                if curr.left is None:
                    curr.left = Node(key, value)
                    return True
                else:
                    curr = curr.left
            else:
                curr.value = value
                return True
        self.root = Node(key, value)

    def __getitem__(self, key):
        curr = self.root
        while curr is not None and key != curr.key:
            if key > curr.key:
                curr = curr.right
            else:
                curr = curr.left
        if curr is None:
            raise KeyError('Such key does not exist')
        else:
            return curr.value


if __name__ == '__main__':
    tree = TreeMap()
    tree[13] = 'second'
    print(tree[13], tree.root.value)
    tree[7] = 'third'
    # print(tree[7], tree.root.left, tree.root.right)
    # tree[6] = 'forth'
    # print(tree[6], tree.root.left.left.key, tree.root.right)

