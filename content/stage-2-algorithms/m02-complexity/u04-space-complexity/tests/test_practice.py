import ast
import inspect
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "exercises"))
import practice


class CountLarge(unittest.TestCase):
    def test_contract(self):
        function = practice.count_large
        values = [3, 8, 5, 8]
        self.assertEqual(function(values, 5), 2)
        self.assertEqual(values, [3, 8, 5, 8])
        self.assertEqual(function([], 0), 0)
        self.assertEqual(function([-1, -2, -1], -2), 2)
        nodes = list(ast.walk(ast.parse(inspect.getsource(function))))
        self.assertEqual(sum(isinstance(node, (ast.For, ast.While)) for node in nodes), 1)
        self.assertFalse(any(isinstance(node, (ast.Call, ast.Slice, ast.List, ast.ListComp,
                                             ast.Set, ast.SetComp, ast.Dict, ast.DictComp,
                                             ast.Tuple, ast.GeneratorExp)) for node in nodes),
                         "Use a loop and a counter only.")


class AboveZero(unittest.TestCase):
    def test_contract(self):
        function = practice.above_zero
        empty = []
        self.assertIsNot(function(empty), empty)
        self.assertEqual(function(empty), [])
        values = [2, 0, -3]
        flags = function(values)
        self.assertEqual(flags, [True, False, False])
        self.assertTrue(all(type(flag) is bool for flag in flags))
        self.assertEqual(values, [2, 0, -3])
        self.assertEqual(function([-1, 4, 4, 0]), [False, True, True, False])
        nodes = ast.walk(ast.parse(inspect.getsource(function)))
        self.assertTrue(any(isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
                            and node.func.attr == "append" for node in nodes))


class PeakOpen(unittest.TestCase):
    def test_contract(self):
        function = practice.peak_open
        for changes, peak in (([], 0), ([1, -1, 1], 1), ([1, 1, -1, -1, 1], 2), ([1] * 200, 200)):
            original = changes[:]
            self.assertEqual(function(changes), peak)
            self.assertEqual(changes, original)
        nodes = list(ast.walk(ast.parse(inspect.getsource(function))))
        self.assertEqual(sum(isinstance(node, (ast.For, ast.While)) for node in nodes), 1)
        self.assertFalse(any(isinstance(node, (ast.List, ast.ListComp, ast.Slice, ast.Set,
                                             ast.SetComp, ast.Dict, ast.DictComp, ast.GeneratorExp))
                             for node in nodes), "Do not save a history of counts.")
        for node in nodes:
            if isinstance(node, ast.Call):
                self.assertTrue(isinstance(node.func, ast.Name) and node.func.id in {"len", "range", "max"})
