"""
File: linkedbst.py
Author: Ken Lambert
"""
import math
import random
import time

from abstractcollection import AbstractCollection
from bstnode import BSTNode
from linkedstack import LinkedStack


class LinkedBST(AbstractCollection):
    """An link-based binary search tree implementation."""

    def __init__(self, sourceCollection=None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        self._root = None
        self.random_words = None
        AbstractCollection.__init__(self, sourceCollection)

    # Accessor methods
    def __str__(self):
        """Returns a string representation with the tree rotated
        90 degrees counterclockwise."""

        def recurse(node, level):
            elem = ""
            if node != None:
                elem += recurse(node.right, level + 1)
                elem += "| " * level
                elem += str(node.data) + "\n"
                elem += recurse(node.left, level + 1)
            return elem

        return recurse(self._root, 0)

    def __iter__(self):
        """Supports a preorder traversal on a view of self."""
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self._root)
            while not stack.isEmpty():
                node = stack.pop()
                yield node.data
                if node.right != None:
                    stack.push(node.right)
                if node.left != None:
                    stack.push(node.left)

    def preorder(self):
        """Supports a preorder traversal on a view of self."""
        return None

    def inorder(self):
        """Supports an inorder traversal on a view of self."""
        lyst = list()

        def recurse(node):
            if node != None:
                recurse(node.left)
                lyst.append(node.data)
                recurse(node.right)

        recurse(self._root)
        return iter(lyst)

    def postorder(self):
        """Supports a postorder traversal on a view of self."""
        return None

    def levelorder(self):
        """Supports a levelorder traversal on a view of self."""
        return None

    def __contains__(self, item):
        """Returns True if target is found or False otherwise."""
        return self.find(item) != None

    def find(self, item):
        """If item matches an item in self, returns the
        matched item, or None otherwise."""

        def recurse(node):
            if node is None:
                return None
            elif item == node.data:
                return node.data
            elif item < node.data:
                return recurse(node.left)
            else:
                return recurse(node.right)

        return recurse(self._root)

    # Mutator methods
    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0

    def add(self, item):
        """Adds item to the tree."""

        # Helper function to search for item's position
        def recurse(node):
            # New item is less, go left until spot is found
            if item < node.data:
                if node.left == None:
                    node.left = BSTNode(item)
                else:
                    recurse(node.left)
            # New item is greater or equal,
            # go right until spot is found
            elif node.right == None:
                node.right = BSTNode(item)
            else:
                recurse(node.right)
                # End of recurse

        # Tree is empty, so new item goes at the root
        if self.isEmpty():
            self._root = BSTNode(item)
        # Otherwise, search for the item's spot
        else:
            recurse(self._root)
        self._size += 1

    def remove(self, item):
        """Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self."""
        if not item in self:
            raise KeyError("Item not in tree.""")

        # Helper function to adjust placement of an item
        def lift_max_in_left_subtree_to_top(top):
            # Replace top's datum with the maximum datum in the left subtree
            # Pre:  top has a left child
            # Post: the maximum node in top's left subtree
            #       has been removed
            # Post: top.data = maximum value in top's left subtree
            parent = top
            current_node = top.left
            while current_node.right is not None:
                parent = current_node
                current_node = current_node.right
            top.data = current_node.data
            if parent == top:
                top.left = current_node.left
            else:
                parent.right = current_node.left

        # Begin main part of the method
        if self.isEmpty(): return None

        # Attempt to locate the node containing the item
        item_removed = None
        pre_root = BSTNode(None)
        pre_root.left = self._root
        parent = pre_root
        direction = 'L'
        current_node = self._root
        while not current_node == None:
            if current_node.data == item:
                item_removed = current_node.data
                break
            parent = current_node
            if current_node.data > item:
                direction = 'L'
                current_node = current_node.left
            else:
                direction = 'R'
                current_node = current_node.right

        # Return None if the item is absent
        if item_removed is None: return None

        # The item is present, so remove its node

        # Case 1: The node has a left and a right child
        #         Replace the node's value with the maximum value in the
        #         left subtree
        #         Delete the maximium node in the left subtree
        if current_node.left is not None \
                and current_node.right is not None:
            lift_max_in_left_subtree_to_top(current_node)
        else:

            # Case 2: The node has no left child
            if current_node.left is None:
                new_child = current_node.right

                # Case 3: The node has no right child
            else:
                new_child = current_node.left

                # Case 2 & 3: Tie the parent to the new child
            if direction == 'L':
                parent.left = new_child
            else:
                parent.right = new_child

        # All cases: Reset the root (if it hasn't changed no harm done)
        #            Decrement the collection's size counter
        #            Return the item
        self._size -= 1
        if self.isEmpty():
            self._root = None
        else:
            self._root = pre_root.left
        return item_removed

    def replace(self, item, new_item):
        """
        If item is in self, replaces it with newItem and
        returns the old item, or returns None otherwise."""
        probe = self._root
        while probe != None:
            if probe.data == item:
                old_data = probe.data
                probe.data = new_item
                return old_data
            elif probe.data > item:
                probe = probe.left
            else:
                probe = probe.right
        return None

    def height(self):
        """
        Return the height of tree
        :return: int
        """

        def height1(top):
            """
            Helper function
            :param top:
            :return:
            """
            if top is None:
                return 0
            else:
                return 1 + max(height1(top.right), height1(top.left))

        return height1(self._root) - 1

    def is_balanced(self):
        """
        Return True if tree is balanced
        True if height < 2 * log2(n + 1) - 1,
        n - number of nodes
        :return:
        """

        def number_of_nodes(top):
            if top is None:
                return 1
            length = 0
            for child in [top.left, top.right]:
                length += number_of_nodes(child)
            return length

        if self._root is None:
            nodes = 0
        else:
            nodes = number_of_nodes(self._root) - 1

        return self.height() < 2 * math.log2(nodes + 1) - 1

    def range_find(self, low, high):
        """
        Returns a list of the items in the tree, where low <= item <= high.
        """
        field = []
        for item in list(self.inorder()):
            if low <= item <= high:
                field.append(item)
        return field

    def rebalance(self):
        """
        Rebalances the tree.
        :return:
        """

        def recursive(segment):
            if len(segment) == 0:
                return None
            middle_index = len(segment) // 2
            return BSTNode(segment[middle_index], \
                           recursive(segment[:middle_index]), recursive(segment[middle_index + 1:]))

        self._root = recursive(list(self.inorder()))

    def successor(self, item):
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        elements = list(self.inorder())
        for elem in elements:
            if elem > item:
                return elem
        return None

    def predecessor(self, item):
        """
        Returns the largest item that is smaller than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        elements = list(self.inorder())
        for elem in reversed(elements):
            if elem < item:
                return elem
        return None

    def demo_bst(self, path):
        """
        Demonstration of efficiency binary search tree for the search tasks.
        :param path:
        :type path:
        :return:
        :rtype:
        """
        with open(path, 'r') as file:
            file = file.read().split('\n')
        self.random_words = random.sample(file, 10000)
        tree = LinkedBST(self.random_words)
        tree_shuffle = LinkedBST(random.shuffle(self.random_words))
        tree_balanced = LinkedBST(self.random_words)
        tree_balanced.rebalance()

        time = []
        time.append(self._time_alphabet_list(file))
        time.append(self._time_bst(tree))
        time.append(self._time_bst(tree_shuffle))
        time.append(self._time_bst(tree_balanced))

        message = ['Alphabetically arranged list:       ',
                   'BST (is sorted alphabetically):     ',
                   'BST (is not sorted alphabetically): ',
                   'BST (after balancing):              ']
        return '\n'.join([message[index] + str(time[index]) for index in range(4)])

    def _time_alphabet_list(self, file):
        """
        :param file: list
        :return: int
        """
        start = time.time()
        search = [file.index(word) for word in self.random_words]
        stop = time.time()
        if len(search) == 10000:
            return stop - start
        return None

    def _time_bst(self, tree):
        """
        :param tree: LinkedBTS
        :param words: list
        :return: int
        """
        start = time.time()
        search = [tree.find(word) for word in self.random_words]
        stop = time.time()
        if len(search) == 10000:
            return stop - start
        return None





if __name__ == '__main__':
    bin_tree = LinkedBST()
    # bin_tree.add(4)
    # bin_tree.add(2)
    # bin_tree.add(6)
    # bin_tree.add(7)
    # # bin_tree.add(1)
    # # bin_tree.add(5)
    # bin_tree.add(8)
    # bin_tree.add(3)
    # bin_tree.add(10)
    # bin_tree.add(11)
    #
    # print(bin_tree)
    # print(bin_tree.height())
    # print(bin_tree.is_balanced())
    #
    # bin_tree.rebalance()
    # print(bin_tree)
    # print(bin_tree.is_balanced())
    #
    # print(bin_tree.successor(2))
    # print(bin_tree.predecessor(2))
    # print(bin_tree.range_find(1, 5))

    print(bin_tree.demo_bst('/Users/anastasiaa/Documents/UCU/PY/2_semester/Lab13/binary_search_tree/words.txt'))


