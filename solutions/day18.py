import json
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

    def explode_left(self, value):
        print(f"explode {self}")
        if self == self._parent._left:
            node = self
            while (node._parent is not None) and (node == node._parent._left):
                node = node._parent
        else:
            node = self
        if node._parent is None:
            return False
        else:
            node = node._parent._left
            print(f"{node}{node._parent}{node.is_leaf()}")
            while not node.is_leaf():
                node = node._left
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
            print(f"{node}-{node._parent}-{node.is_leaf()}")
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


if __name__ == '__main__':
    def _main():
        result = []
        with open('../inputs/day18.txt', 'r') as f:
            for line in f:
                result.append(json.loads(line.strip()))
            print(result[-1])
            print(count_nesting(result[-1]))
            lst = json.loads('[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]')
            tree = build_tree(lst)
            print(tree)
            node = tree.find_explode_node(tree, 0)
            node.explode()
            print(tree)
    _main()

