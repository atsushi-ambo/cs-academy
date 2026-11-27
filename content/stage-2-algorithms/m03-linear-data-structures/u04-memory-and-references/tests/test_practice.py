import ast
import inspect
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "exercises"))
import practice


class SameList(unittest.TestCase):
    def test_contract(self):
        function = practice.same_list
        a, b = [4], [4]
        self.assertIs(function(a, a), True)
        self.assertIs(function(a, b), False)
        self.assertIs(function([], []), False)
        self.assertEqual((a, b), ([4], [4]))
        self.assertTrue(any(isinstance(node, ast.Is)
                            for node in ast.walk(ast.parse(inspect.getsource(function)))))


class BlankGrid(unittest.TestCase):
    def test_contract(self):
        function = practice.blank_grid
        self.assertEqual(function(0, 3), [])
        empty_rows = function(2, 0)
        self.assertEqual(empty_rows, [[], []])
        self.assertIsNot(empty_rows[0], empty_rows[1])
        grid = function(3, 2)
        self.assertEqual(grid, [[0, 0], [0, 0], [0, 0]])
        grid[0][1] = 8
        self.assertEqual(grid, [[0, 8], [0, 0], [0, 0]])
        self.assertEqual(function(1, 1), [[0]])


class HeadView(unittest.TestCase):
    def test_contract(self):
        function = practice.head_view
        data = bytearray([5, 1, 3])
        view = function(data, 2)
        self.assertIsInstance(view, memoryview)
        self.assertEqual(list(view), [5, 1])
        self.assertEqual(list(data), [5, 1, 3])
        view[1] = 9
        self.assertEqual(list(data), [5, 9, 3])
        data[0] = 4
        self.assertEqual(view[0], 4)
        self.assertEqual(len(function(data, 3)), 3)
        self.assertEqual(len(function(data, 0)), 0)
        self.assertEqual(len(function(bytearray(), 0)), 0)
