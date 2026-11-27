import ast
import inspect
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "exercises"))
import practice


def recursive_calls(nodes, name):
    return [node for node in nodes if isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name) and node.func.id == name]


class HalfPath(unittest.TestCase):
    def test_contract(self):
        function = practice.half_path
        for size, count in ((1, 0), (2, 1), (3, 1), (18, 4), (1024, 10), (1_000_000, 19)):
            self.assertEqual(function(size), count)
        nodes = list(ast.walk(ast.parse(inspect.getsource(function))))
        self.assertEqual(len(recursive_calls(nodes, "half_path")), 1)
        self.assertFalse(any(isinstance(node, (ast.For, ast.While, ast.comprehension)) for node in nodes))


class OrderCount(unittest.TestCase):
    def test_contract(self):
        function = practice.order_count
        for n, count in ((0, 1), (1, 1), (4, 24), (6, 720), (12, 479001600)):
            self.assertEqual(function(n), count)
        calls = [node for node in ast.walk(ast.parse(inspect.getsource(function)))
                 if isinstance(node, ast.Call)]
        self.assertTrue(all(isinstance(node.func, ast.Name) and node.func.id == "range"
                            for node in calls), "Only call range(). Multiply the factors yourself.")
        self.assertTrue(any(isinstance(node, (ast.For, ast.While))
                            for node in ast.walk(ast.parse(inspect.getsource(function)))))


class TripleChecks(unittest.TestCase):
    def test_contract(self):
        function = practice.triple_checks
        for n in (0, 1, 2, 7, 30, 500):
            self.assertEqual(function(n), n ** 3)
        nodes = list(ast.walk(ast.parse(inspect.getsource(function))))
        self.assertFalse(any(isinstance(node, (ast.For, ast.While, ast.comprehension, ast.Call))
                             for node in nodes), "Compute the count directly.")
        self.assertTrue(any(isinstance(node, (ast.Mult, ast.Pow)) for node in nodes))
