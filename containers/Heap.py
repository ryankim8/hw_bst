'''
This file implements the Heap data structure as a subclass of the BinaryTree.
The book implements Heaps using an *implicit* tree with an *explicit* vector implementation,
so the code in the book is likely to be less helpful than the code for the other data structures.
The book's implementation is the traditional implementation because it has a faster constant factor
(but the same asymptotics).
This homework is using an explicit tree implementation to help you get more practice with OOP-style programming and classes.
'''

from containers.BinaryTree import BinaryTree, Node
from collections import deque


class Heap(BinaryTree):
    '''
    FIXME:
    Heap is currently not a subclass of BinaryTree.
    You should make the necessary changes in the class declaration line above
    and in the constructor below.
    '''

    def __init__(self, xs=None):
        '''
        FIXME:
        If xs is a list (i.e. xs is not None),
        then each element of xs needs to be inserted into the Heap.
        '''
        super().__init__()
        if xs:
            self.insert_list(xs)

    def __repr__(self):
        '''
        Notice that in the BinaryTree class,
        we defined a __str__ function,
        but not a __repr__ function.
        Recall that the __repr__ function should return a string that can be used to recreate a valid instance of the class.
        Thus, if you create a variable using the command Heap([1,2,3])
        it's __repr__ will return "Heap([1,2,3])"

        For the Heap, type(self).__name__ will be the string "Heap",
        but for the AVLTree, this expression will be "AVLTree".
        Using this expression ensures that all subclasses of Heap will have a correct implementation of __repr__,
        and that they won't have to reimplement it.
        '''
        return type(self).__name__ + '(' + str(self.to_list('inorder')) + ')'

    def is_heap_satisfied(self):
        '''
        Whenever you implement a data structure,
        the first thing to do is to implement a function that checks whether
        the structure obeys all of its laws.
        This makes it possible to automatically test whether insert/delete functions
        are actually working.
        '''
        if self.root:
            return Heap._is_heap_satisfied(self.root)
        return True

    @staticmethod
    def _is_heap_satisfied(node):
        '''
        FIXME:
        Implement this method.
        '''
        return Heap._is_complete(node) and Heap._is_min_heap(node)

    def _is_complete(node):
        if node is None:
            return True
        queue = deque([node])
        row_missing = False
        while queue:
            node = queue.popleft()
            if node is None:
                row_missing = True
            else:
                if row_missing:
                    return False
                queue.append(node.left)
                queue.append(node.right)
        return True

    def _is_min_heap(node):
        if node is None:
            return True
        if node.left and node.left.value < node.value:
            return False
        if node.right and node.right.value < node.value:
            return False
        return Heap._is_min_heap(node.left) and Heap._is_min_heap(node.right)

    def insert(self, value):
        '''
        Inserts value into the heap.
        '''
        if self.root is None:
            self.root = Node(value)
        else:
            n = len(self) + 1
            binary_path = bin(n)[3:]
            Heap._insert(self.root, value, binary_path)

    @staticmethod
    def _insert(node, value, path):
        if len(path) == 1:
            if path == "0":
                node.left = Node(value)
            else:
                node.right = Node(value)
        else:
            if path[0] == "0":
                nxt = node.left
            else:
                nxt = node.right
            Heap._insert(nxt, value, path[1:])

        if path[0] == "0":
            child = node.left
        else:
            child = node.right
        if child.value < node.value:
            node.value, child.value = child.value, node.value

    def insert_list(self, xs):
        '''
        Given a list xs, insert each element of xs into self.

        FIXME:
        Implement this function.
        '''
        for x in xs:
            self.insert(x)

    def find_smallest(self):
        '''
        Returns the smallest value in the tree.

        FIXME:
        Implement this function.
        '''
        if self.root is None:
            return None
        return self.root.value

    def remove_min(self):
        '''
        Removes the minimum value from the Heap.
        If the heap is empty, it does nothing.
        '''
        if self.root is None:
            return
        n = len(self)
        if n == 1:
            self.root = None
            return
        binary_path = bin(n)[3:]
        last_value = Heap._remove_bottom_right(self.root, binary_path)
        self.root.value = last_value
        Heap._trickle(self.root)

    @staticmethod
    def _remove_bottom_right(node, path):
        '''
        Detach the node at the end of path and return the value.
        '''
        if len(path) == 1:
            if path == "0":
                value = node.left.value
                node.left = None
            else:
                value = node.right.value
                node.right = None
            return value
        if path[0] == "0":
            nxt = node.left
        else:
            nxt = node.right
        return Heap._remove_bottom_right(nxt, path[1:])

    @staticmethod
    def _trickle(node):
        '''
        Swap node's value down with its smallest child until minheap is satisfied
        '''
        smallest = node
        if node.left and node.left.value < smallest.value:
            smallest = node.left
        if node.right and node.right.value < smallest.value:
            smallest = node.right
        if smallest is not node:
            node.value, smallest.value = smallest.value, node.value
            Heap._trickle(smallest)
