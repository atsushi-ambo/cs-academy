import ast
import inspect
import sys
import textwrap
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "exercises"))
import practice


class TrackedSlots(list):
    def __init__(self, items):
        super().__init__(items)
        self.reads = 0

    def __getitem__(self, index):
        result = super().__getitem__(index)
        self.reads += len(result) if isinstance(index, slice) else 1
        return result

    def __iter__(self):
        for index in range(len(self)):
            yield self[index]


class ReadCell(unittest.TestCase):
    def test_contract(self):
        function = practice.read_cell
        cells = [4, 5, 6, 7, 8, 9]
        self.assertEqual(function(cells, 3, 1, 0), 7)
        self.assertEqual(function(cells, 3, 0, 2), 6)
        self.assertEqual(function(cells, 2, 2, 1), 9)
        self.assertEqual(function([8], 1, 0, 0), 8)
        self.assertEqual(cells, [4, 5, 6, 7, 8, 9])
        tracked = TrackedSlots(cells)
        self.assertEqual(function(tracked, 3, 1, 2), 9)
        self.assertEqual(tracked.reads, 1)
        nodes = ast.walk(ast.parse(inspect.getsource(function)))
        self.assertFalse(any(isinstance(node, (ast.For, ast.While, ast.comprehension))
                             for node in nodes), "Find the slot directly.")


class CopiesForAppends(unittest.TestCase):
    def test_contract(self):
        function = practice.copies_for_appends
        for count, copies in ((0, 0), (1, 0), (2, 1), (4, 3), (5, 7), (8, 7),
                              (9, 15), (1_000_000, 1_048_575)):
            self.assertEqual(function(count), copies)
        nodes = list(ast.walk(ast.parse(inspect.getsource(function))))
        loops = (ast.For, ast.While, ast.comprehension)
        loop, = (node for node in nodes if isinstance(node, loops))
        self.assertIsInstance(loop, (ast.For, ast.While), "Loop over resizes only.")
        self.assertFalse(any(isinstance(node, (ast.List, ast.Dict, ast.Set)) for node in nodes))


class MakeArray(unittest.TestCase):
    def test_contract(self):
        array = practice.make_array()
        other = practice.make_array()
        self.assertEqual((array.size, array.copies, array.slots), (0, 0, [None]))
        self.assertIsNot(array.slots, other.slots)
        self.assertEqual(type(array).__name__, "DynamicArray")
        values = [5, 8, 2, None, object()] + list(range(95))
        copies = 0
        capacity = 1
        for i, value in enumerate(values):
            old = TrackedSlots(array.slots)
            array.slots = old
            if i == capacity:
                copies += capacity
                capacity *= 2
                expected_reads = i
            else:
                expected_reads = 0
            array.append(value)
            self.assertEqual((array.size, array.copies, len(array.slots)), (i + 1, copies, capacity))
            self.assertEqual(old.reads, expected_reads, "Copy existing slots only on a resize.")
            self.assertEqual(array.slots, values[:i + 1] + [None] * (capacity - i - 1))
            if expected_reads:
                self.assertIsNot(array.slots, old)
            else:
                self.assertIs(array.slots, old)
        self.assertEqual((other.size, other.copies, other.slots), (0, 0, [None]))
        nodes = ast.walk(ast.parse(textwrap.dedent(inspect.getsource(array.append))))
        for node in nodes:
            self.assertNotIsInstance(node, ast.Slice)
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
                self.assertNotIn(node.func.attr, {"append", "extend", "insert", "copy"})
