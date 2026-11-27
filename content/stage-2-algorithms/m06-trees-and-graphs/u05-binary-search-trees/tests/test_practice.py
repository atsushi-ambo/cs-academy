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

def keys(root):
    if root is None:
        return []
    return keys(root.left) + [root.key] + keys(root.right)


class Search(unittest.TestCase):
    def test_empty_and_single(self):
        self.assertFalse(practice.search(None, 1))
        self.assertTrue(practice.search(Node(1), 1))

    def test_paths_and_input(self):
        left = Node(3, None, Node(5))
        root = Node(8, left, Node(12))
        self.assertTrue(practice.search(root, 5))
        self.assertFalse(practice.search(root, 7))
        self.assertIs(root.left, left)
        self.assertEqual(keys(root), [3, 5, 8, 12])


class Insert(unittest.TestCase):
    def test_empty_and_duplicate(self):
        root = practice.insert(None, -2, Node)
        self.assertEqual(keys(root), [-2])
        root = practice.insert(root, -2, Node)
        self.assertEqual(keys(root), [-2])

    def test_both_branches(self):
        root = Node(8)
        for key in [15, 4, 5, 9]:
            root = practice.insert(root, key, Node)
        self.assertEqual(keys(root), [4, 5, 8, 9, 15])
        self.assertEqual(root.key, 8)

    def test_sorted_chain(self):
        root = None
        for key in range(1, 5):
            root = practice.insert(root, key, Node)
        for key in range(1, 5):
            self.assertEqual(root.key, key)
            self.assertIsNone(root.left)
            root = root.right
        self.assertIsNone(root)


class Delete(unittest.TestCase):
    def test_empty_missing_and_leaf(self):
        self.assertIsNone(practice.delete(None, 5))
        self.assertEqual(keys(practice.delete(Node(3), 5)), [3])
        self.assertIsNone(practice.delete(Node(3), 3))

    def test_one_child(self):
        self.assertEqual(keys(practice.delete(Node(8, Node(4)), 8)), [4])
        root = practice.delete(Node(8, Node(4, None, Node(6))), 4)
        self.assertEqual(keys(root), [6, 8])

    def test_two_children_keep_successors_child(self):
        root = Node(20, Node(11), Node(60, Node(35, None, Node(42)), Node(80)))
        result = practice.delete(root, 20)
        self.assertEqual(result.key, 35)
        self.assertEqual(keys(result), [11, 35, 42, 60, 80])
        self.assertEqual(result.right.left.key, 42)

    def test_successor_is_right_child(self):
        root = Node(20, Node(11), Node(35, None, Node(42)))
        result = practice.delete(root, 20)
        self.assertEqual(result.key, 35)
        self.assertEqual(keys(result), [11, 35, 42])


class IsBst(unittest.TestCase):
    def test_empty_and_single(self):
        self.assertTrue(practice.is_bst(None))
        self.assertTrue(practice.is_bst(Node(-1)))

    def test_deep_bounds_and_duplicates(self):
        self.assertFalse(practice.is_bst(Node(20, Node(9, None, Node(25)))))
        self.assertFalse(practice.is_bst(Node(20, None, Node(30, Node(19)))))
        self.assertFalse(practice.is_bst(Node(20, None, Node(30, Node(20)))))

    def test_valid_and_read_only(self):
        left = Node(-10, None, Node(-2))
        root = Node(0, left, Node(7, Node(6)))
        self.assertTrue(practice.is_bst(root))
        self.assertIs(root.left, left)
        self.assertEqual(keys(root), [-10, -2, 0, 6, 7])
