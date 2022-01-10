import json
from math import ceil, floor

import numpy as np


def add(t1, t2):
    return [t1, t2]


def count_nesting(nr):
    def count(t, cnt):
        if isinstance(t, list):
            if len(t) > 1:
                return [count(t[0], cnt+1), count(t[1], cnt+1)]
            else:
                return count_nesting(t[0], cnt+1)
        else:
            return cnt
    return count(nr, 0)


class TreeNode:
    def __init__(self, left, right, val=None):
        self._left = left
        self._right = right
        self._parent = None
        self._val = val

    def is_leaf(self):
        return self._left is None and self._right is None

    def __str__(self):
        if self.is_leaf():
            return str(self._val)
        else:
            return f"({str(self._left)},{str(self._right)})"

    def explode(self):
        left_val = self._left._val
        self.explode_left(left_val)
        right_val = self._right._val
        self.explode_right(right_val)
        if self._parent._right == self:
            new_node = TreeNode(None, None, 0)
            self._parent._right = new_node
            new_node._parent = self._parent
        else:
            new_node = TreeNode(None, None, 0)
            self._parent._left = new_node
            new_node._parent = self._parent

    def split(self):
        val1 = TreeNode(None, None,int(floor(self._val / 2.)))
        val2 = TreeNode(None, None, int(ceil(self._val / 2)))
        node = TreeNode(
            left=val1,
            right=val2
        )
        val1._parent = node
        val2._parent = node
        if self._parent._left == self:
            self._parent._left = node
        else:
            self._parent._right = node
        node._parent = self._parent

    def explode_left(self, value):
        if self == self._parent._left:
            node = self
            while (node._parent is not None) and (node == node._parent._left):
                node = node._parent
        else:
            node = self
        if node._parent is None:
            print('False')
            return False
        else:
            node = node._parent._left
            while not node.is_leaf():
                node = node._right
            node._val += value
            return True

    def explode_right(self, value):
        if self == self._parent._right:
            node = self
            while (node._parent is not None) and (node == node._parent._right):
                node = node._parent
        else:
            node = self._parent._right
        if node._parent is None:
            return False
        else:
            node = node._parent._right
            while not node.is_leaf():
                node = node._left
            node._val += value
            return True

    def find_explode_node(self, node, depth):
        if node.is_leaf():
            return None
        else:
            res = self.find_explode_node(node._left, depth + 1)
            if res:
                return res
            else:
                if depth >= 4:
                    return node
                else:
                    return self.find_explode_node(node._right, depth + 1)

    def find_split_node(self, node):
        if node.is_leaf():
            if node._val >= 10:
                return node
            else:
                return None
        else:
            res = self.find_split_node(node._left)
            if res:
                return res
            else:
                return self.find_split_node(node._right)

    def to_list(self):
        if self.is_leaf():
            return self._val
        else:
            return [self._left.to_list(), self._right.to_list()]

    def magnitude(self):
        if self.is_leaf():
            return self._val
        else:
            return 3 * self._left.magnitude() + 2 * self._right.magnitude()


def build_tree(t):
    if isinstance(t, list):
        left = build_tree(t[0])
        right = build_tree(t[1])
        node = TreeNode(left, right)
        left._parent = node
        right._parent = node
        return node
    else:
        return TreeNode(None, None, t)


def reduce(tree):
    done = False
    while not done:
        node = tree.find_explode_node(tree, 0)
        if node is not None:
            node.explode()
            continue
        node = tree.find_split_node(tree)
        if node is not None:
            node.split()
        else:
            done = True


def add_all(list_of_nrs):
    total = list_of_nrs[0]
    for nr in list_of_nrs[1:]:
        total = add(total, nr)
        tree = build_tree(total)
        reduce(tree)
        total = tree.to_list()
    return total


def find_largest_sum(list_of_nrs):
    best_so_far = 0
    for idx1 in range(len(list_of_nrs)):
        nr1 = list_of_nrs[idx1]
        for idx2 in range(idx1, len(list_of_nrs)):
            nr2 = list_of_nrs[idx2]
            sum1 = add_all([nr1, nr2])
            mag1 = build_tree(sum1).magnitude()
            sum2 = add_all([nr2, nr1])
            mag2 = build_tree(sum2).magnitude()
            max_mag = max([mag1, mag2])
            if max_mag > best_so_far:
                best_so_far = max_mag
    return best_so_far

if __name__ == '__main__':
    def _main():
        result = []
        with open('../inputs/day18.txt', 'r') as f:
            for line in f:
                result.append(json.loads(line.strip()))


            test = [
                [[[0, [5, 8]], [[1, 7], [9, 6]]], [[4, [1, 2]], [[1, 4], 2]]],
                [[[5, [2, 8]], 4], [5, [[9, 9], 0]]],
                [6, [[[6, 2], [5, 6]], [[7, 6], [4, 7]]]],
                [[[6, [0, 7]], [0, 9]], [4, [9, [9, 0]]]],
                [[[7, [6, 4]], [3, [1, 3]]], [[[5, 5], 1], 9]],
                [[6, [[7, 3], [3, 2]]], [[[3, 8], [5, 7]], 4]],
                [[[[5, 4], [7, 7]], 8], [[8, 3], 8]],
                [[9, 3], [[9, 9], [6, [4, 9]]]],
                [[2, [[7, 7], 7]], [[5, 8], [[9, 3], [0, 2]]]],
                [[[[5, 2], 5], [8, [3, 7]]], [[5, [7, 5]], [4, 4]]]
                ]
            # print(add_all(test))
            # tree=build_tree([[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]])
            # print(tree.magnitude())
            # node = tree.find_explode_node(tree, 0)
            # node.explode()
            # print(tree)
            # node = tree.find_explode_node(tree, 0)
            # print(node)
            # node.explode()
            # print(tree)
            tree = build_tree(add_all(result))
            print(tree.magnitude())
            print(find_largest_sum(result))

    _main()

