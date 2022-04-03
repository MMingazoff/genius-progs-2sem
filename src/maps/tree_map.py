"""
Binary Search Tree.
Node keys on the left are less than the key of a parent node.
Node keys on the right are less than the key of a parent node.
"""
from src.maps.base_map import BaseMap


class Node:
    """
    Node of TreeMap.
    Each node has key, value and references to the left and right nodes
    """
    def __init__(self, key, value, left=None, right=None):
        self.key = key
        self.value = value
        self.left = left
        self.right = right

    def get_key(self):
        """Returns the key of a node"""
        return self.key

    def get_value(self):
        """Returns the value of a node"""
        return self.key


class TreeMap(BaseMap):
    """
    Binary Search Tree class
    """
    def __init__(self, root=None):
        self.root = root
        self.size = 0

    def __setitem__(self, key, value):
        def set_node(node):
            if key > node.key:
                if node.right is None:
                    node.right = Node(key, value)
                else:
                    set_node(node.right)
            elif key < node.key:
                if node.left is None:
                    node.left = Node(key, value)
                else:
                    set_node(node.left)
            elif key == node.key:
                node.value = value
                self.size -= 1

        if self.root is None:
            self.root = Node(key, value)
        else:
            set_node(self.root)
        self.size += 1

    def __getitem__(self, key):
        def get_node(node):
            if node is None:
                raise KeyError('Such key does not exist')
            if key > node.key:
                return get_node(node.right)
            if key < node.key:
                return get_node(node.left)
            return node  # key == node.key
        return get_node(self.root).value

    def __delitem__(self, key):
        def del_node(node, key_, prev_node=None):
            if node is None:
                raise KeyError('Such key does not exist')
            if key_ > node.key:
                del_node(node.right, key_, node)
            elif key_ < node.key:
                del_node(node.left, key_, node)
            else:  # key == node.key
                if node.right is None and node.left is None:  # node has no children
                    if prev_node.right is node:  # "node to be deleted" is on the right
                        prev_node.right = None
                    elif prev_node.left is node:  # "node to be deleted is on the left
                        prev_node.left = None
                    del node
                elif node.right is None or node.left is None:  # node has one child
                    child = node.right if node.right is not None else node.left
                    if prev_node.right is node:  # "node to be deleted" is on the right
                        prev_node.right = child
                    elif prev_node.left is node:  # "node to be deleted" is on the left
                        prev_node.left = child
                    del node
                else:  # node has both children (left and right)
                    curr = node.right
                    prev = node
                    while curr.left is not None:
                        prev = curr
                        curr = curr.left
                    # change k,v of "node to be deleted" on k,v of the least key in the right tree
                    node.key = curr.key
                    node.value = curr.value
                    del_node(curr, curr.key, prev)  # del node with the least key in the right tree

        if self.root is not None and self.root.right is None and self.root.left is None:
            del self.root
            self.root = None
        del_node(self.root, key)
        self.size -= 1

    def __iter__(self):
        def iter_node(node):
            if node is not None:
                yield node
                yield from iter_node(node.left)
                yield from iter_node(node.right)

        yield from iter_node(self.root)

    def __len__(self):
        return self.size


if __name__ == '__main__':
    tree = TreeMap()
    tree[10] = 'root'
    tree[7] = 'left'
    tree[12] = 'right'
    tree[9] = 'left->right'
    tree[8] = 'left->right->left'
    tree[6] = 'left->left'
    del tree[9]
    for el in tree:
        print(el)
