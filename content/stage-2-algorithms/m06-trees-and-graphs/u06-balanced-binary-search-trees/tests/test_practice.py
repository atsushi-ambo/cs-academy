import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "exercises"))
import practice


class Node:
    def __init__(self, key, left=None, right=None):
        self.key = key
        self.left = left
        self.right = right
        left_height = 0 if left is None else left.height
        right_height = 0 if right is None else right.height
        self.height = 1 + max(left_height, right_height)
def refresh(node):
    left = 0 if node.left is None else node.left.height
    right = 0 if node.right is None else node.right.height
    node.height = 1 + max(left, right)


def left_turn(root):
    pivot = root.right
    root.right = pivot.left
    pivot.left = root
    refresh(root)
    refresh(pivot)
    return pivot


def right_turn(root):
    pivot = root.left
    root.left = pivot.right
    pivot.right = root
    refresh(root)
    refresh(pivot)
    return pivot


class BalanceFactor(unittest.TestCase):
    def test_empty_and_leaf(self):
        self.assertEqual(practice.balance_factor(None), 0)
        self.assertEqual(practice.balance_factor(Node(4)), 0)

    def test_both_signs_and_no_change(self):
        left = Node(2, Node(1))
        root = Node(3, left)
        self.assertEqual(practice.balance_factor(root), 2)
        self.assertIs(root.left, left)
        self.assertEqual((root.height, left.height), (3, 2))
        self.assertEqual(practice.balance_factor(Node(4, None, Node(5))), -1)


class RotateLeft(unittest.TestCase):
    def test_single_child(self):
        root = practice.rotate_left(Node(2, None, Node(4)))
        self.assertEqual((root.key, root.height, root.left.height), (4, 2, 1))

    def test_middle_branch_and_outer_links(self):
        middle = Node(6, Node(5))
        old = Node(4, Node(2), Node(8, middle, Node(10)))
        pivot = old.right
        result = practice.rotate_left(old)
        self.assertIs(result, pivot)
        self.assertIs(result.left.right, middle)
        self.assertIs(result.left, old)
        self.assertEqual((old.left.key, result.right.key), (2, 10))
        self.assertEqual((old.height, result.height, middle.height), (3, 4, 2))


class RotateRight(unittest.TestCase):
    def test_single_child(self):
        root = practice.rotate_right(Node(4, Node(2)))
        self.assertEqual((root.key, root.height, root.right.height), (2, 2, 1))

    def test_middle_branch_and_outer_links(self):
        middle = Node(6, None, Node(7))
        old = Node(8, Node(4, Node(2), middle), Node(10))
        pivot = old.left
        result = practice.rotate_right(old)
        self.assertIs(result, pivot)
        self.assertIs(result.right.left, middle)
        self.assertIs(result.right, old)
        self.assertEqual((result.left.key, old.right.key), (2, 10))
        self.assertEqual((old.height, result.height, middle.height), (3, 4, 2))


class AvlInsert(unittest.TestCase):
    def checked_insert(self, root, key):
        return practice.avl_insert(root, key, Node, left_turn, right_turn)

    def check_tree(self, root):
        if root is None:
            return [], 0
        left, left_height = self.check_tree(root.left)
        right, right_height = self.check_tree(root.right)
        self.assertLessEqual(abs(left_height - right_height), 1)
        self.assertEqual(root.height, 1 + max(left_height, right_height))
        return left + [root.key] + right, root.height

    def test_single_and_duplicate(self):
        root = self.checked_insert(None, 6)
        self.assertEqual(self.check_tree(root), ([6], 1))
        root = self.checked_insert(root, 6)
        self.assertEqual(self.check_tree(root), ([6], 1))
        root = self.checked_insert(root, 3)
        self.assertEqual(self.check_tree(root), ([3, 6], 2))

    def test_all_four_repairs(self):
        for order in ([30, 20, 10], [10, 20, 30], [30, 10, 20], [10, 30, 20]):
            with self.subTest(order=order):
                root = Node(order[0])
                for key in order[1:]:
                    root = self.checked_insert(root, key)
                self.assertEqual(root.key, 20)
                self.assertEqual(self.check_tree(root), ([10, 20, 30], 2))

    def test_rotation_calls_for_each_case(self):
        expected = {
            (30, 20, 10): [("right", 30)],
            (10, 20, 30): [("left", 10)],
            (30, 10, 20): [("left", 10), ("right", 30)],
            (10, 30, 20): [("right", 30), ("left", 10)],
        }
        for order, calls_wanted in expected.items():
            with self.subTest(order=order):
                calls = []
                made = []

                def spy_left(node):
                    calls.append(("left", node.key))
                    return left_turn(node)

                def spy_right(node):
                    calls.append(("right", node.key))
                    return right_turn(node)

                def spy_node(key):
                    made.append(key)
                    return Node(key)

                root = None
                for key in order:
                    root = practice.avl_insert(root, key, spy_node, spy_left, spy_right)
                self.assertEqual(calls, calls_wanted)
                self.assertEqual(made, list(order))
                self.assertEqual(root.key, 20)

    def test_balanced_inserts_do_not_rotate_or_rebuild(self):
        calls = []
        made = []

        def spy_left(node):
            calls.append(node.key)
            return left_turn(node)

        def spy_right(node):
            calls.append(node.key)
            return right_turn(node)

        def spy_node(key):
            made.append(key)
            return Node(key)

        root = None
        for key in (20, 10, 30, 5, 15, 25, 35, 20, 5):
            root = practice.avl_insert(root, key, spy_node, spy_left, spy_right)
        self.assertEqual(calls, [])
        self.assertEqual(made, [20, 10, 30, 5, 15, 25, 35])

    def test_sorted_stream_and_internal_rotations(self):
        root = Node(0)
        for key in range(1, 40):
            root = self.checked_insert(root, key)
            self.assertEqual(self.check_tree(root)[0], list(range(key + 1)))
