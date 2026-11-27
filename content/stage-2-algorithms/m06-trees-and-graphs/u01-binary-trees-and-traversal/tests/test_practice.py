import ast
import inspect
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "exercises"))
import practice


class Node:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

def uses_recursion(function):
    tree = ast.parse(inspect.getsource(practice))
    graph = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            graph[node.name] = {
                call.func.id if isinstance(call.func, ast.Name) else call.func.attr
                for call in ast.walk(node)
                if isinstance(call, ast.Call) and isinstance(call.func, (ast.Name, ast.Attribute))
            }

    def has_cycle(name, active):
        if name in active:
            return True
        return any(has_cycle(child, active | {name}) for child in graph.get(name, ()))

    return has_cycle(function.__name__, set())


def sample():
    return Node(4, Node(9, None, Node(4)), Node(2, Node(7)))


class MakeNode(unittest.TestCase):
    def test_empty_links(self):
        node = practice.make_node(4)
        self.assertEqual((node.value, node.left, node.right), (4, None, None))

    def test_child_identity(self):
        child = Node(4)
        left = practice.make_node(4, child)
        right = practice.make_node(4, right=child)
        self.assertIs(left.left, child)
        self.assertIs(right.right, child)
        self.assertIsNot(left, right)


class Preorder(unittest.TestCase):
    def test_empty_and_single(self):
        self.assertEqual(practice.preorder(None), [])
        self.assertEqual(practice.preorder(Node(3)), [3])

    def test_order_and_input(self):
        root = sample()
        left, right = root.left, root.right
        result = practice.preorder(root)
        self.assertEqual(result, [4, 9, 4, 2, 7])
        self.assertEqual(practice.preorder(Node(8)), [8])
        self.assertEqual(result, [4, 9, 4, 2, 7])
        self.assertIs(root.left, left)
        self.assertIs(root.right, right)
        self.assertEqual((root.value, left.right.value, right.left.value), (4, 4, 7))

    def test_recursion(self):
        self.assertTrue(uses_recursion(practice.preorder), "Visit subtrees with recursion.")


class Inorder(unittest.TestCase):
    def test_empty_and_single(self):
        self.assertEqual(practice.inorder(None), [])
        self.assertEqual(practice.inorder(Node(3)), [3])

    def test_order_and_input(self):
        root = sample()
        left, right = root.left, root.right
        result = practice.inorder(root)
        self.assertEqual(result, [9, 4, 4, 7, 2])
        self.assertEqual(practice.inorder(Node(8)), [8])
        self.assertEqual(result, [9, 4, 4, 7, 2])
        self.assertIs(root.left, left)
        self.assertIs(root.right, right)
        self.assertEqual((root.value, left.right.value, right.left.value), (4, 4, 7))

    def test_recursion(self):
        self.assertTrue(uses_recursion(practice.inorder), "Visit subtrees with recursion.")


class Postorder(unittest.TestCase):
    def test_empty_and_single(self):
        self.assertEqual(practice.postorder(None), [])
        self.assertEqual(practice.postorder(Node(3)), [3])

    def test_order_and_input(self):
        root = sample()
        left, right = root.left, root.right
        result = practice.postorder(root)
        self.assertEqual(result, [4, 9, 7, 2, 4])
        self.assertEqual(practice.postorder(Node(8)), [8])
        self.assertEqual(result, [4, 9, 7, 2, 4])
        self.assertIs(root.left, left)
        self.assertIs(root.right, right)
        self.assertEqual((root.value, left.right.value, right.left.value), (4, 4, 7))

    def test_recursion(self):
        self.assertTrue(uses_recursion(practice.postorder), "Visit subtrees with recursion.")


class LevelOrder(unittest.TestCase):
    def test_empty_and_single(self):
        self.assertEqual(practice.level_order(None), [])
        self.assertEqual(practice.level_order(Node(3)), [3])

    def test_order_and_input(self):
        root = sample()
        left, right = root.left, root.right
        result = practice.level_order(root)
        self.assertEqual(result, [4, 9, 2, 4, 7])
        self.assertEqual(practice.level_order(Node(8)), [8])
        self.assertEqual(result, [4, 9, 2, 4, 7])
        self.assertIs(root.left, left)
        self.assertIs(root.right, right)
        self.assertEqual((root.value, left.right.value, right.left.value), (4, 4, 7))


class TreeStats(unittest.TestCase):
    def test_empty_and_single(self):
        self.assertEqual(practice.tree_stats(None), (0, 0))
        self.assertEqual(practice.tree_stats(Node(9)), (1, 1))

    def test_one_child_and_duplicate_values(self):
        left = Node(4, Node(4), Node(4))
        root = Node(4, left)
        self.assertEqual(practice.tree_stats(root), (3, 2))
        self.assertIs(root.left, left)
        self.assertIsNone(root.right)

    def test_recursion(self):
        self.assertTrue(uses_recursion(practice.tree_stats), "Measure subtrees with recursion.")
