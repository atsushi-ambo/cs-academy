import ast
import inspect
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "exercises"))
import practice


class ShelfChecks(unittest.TestCase):
    def test_contract(self):
        function = practice.shelf_checks
        self.assertEqual(function([], "A"), 0)
        codes = ["A", "B", "A"]
        self.assertEqual(function(codes, "A"), 5)
        self.assertEqual(codes, ["A", "B", "A"])
        self.assertEqual(function(["B"] * 200, "A"), 200)
        nodes = list(ast.walk(ast.parse(inspect.getsource(function))))
        loops = (ast.For, ast.AsyncFor, ast.While, ast.comprehension)
        self.assertEqual(sum(isinstance(node, loops) for node in nodes), 1)
        self.assertFalse(any(isinstance(node, ast.Attribute) and node.attr == "count"
                             for node in nodes))


class PairChecks(unittest.TestCase):
    def test_contract(self):
        function = practice.pair_checks
        for n in (0, 1, 2, 5, 100):
            self.assertEqual(function(n), n * (n - 1) // 2)
        nodes = ast.walk(ast.parse(inspect.getsource(function)))
        self.assertTrue(any(isinstance(node, ast.For) and any(isinstance(child, ast.For)
                            for stmt in node.body for child in ast.walk(stmt))
                            for node in nodes), "Use nested for loops.")


class SharedShelfPairs(unittest.TestCase):
    def test_contract(self):
        function = practice.shared_shelf_pairs
        returns, records = ["A", "A"], ["A", "B", "A"]
        self.assertEqual(function(returns, records), 4)
        self.assertEqual((returns, records), (["A", "A"], ["A", "B", "A"]))
        self.assertEqual(function([], records), 0)
        self.assertEqual(function(returns, []), 0)
        self.assertEqual(function(["A", "B", "C"], ["C"]), 1)
        self.assertEqual(function(["C"], ["A"]), 0)
