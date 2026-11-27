import ast
import inspect
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "exercises"))
import practice

class MakeDeque(unittest.TestCase):
    def test_both_ends(self):
        dq = practice.make_deque(3)
        slots = dq.slots
        self.assertIsNone(dq.pop_left())
        self.assertIsNone(dq.pop_right())
        self.assertIs(dq.push_left(4), True)
        self.assertIs(dq.push_left(0), True)
        self.assertIs(dq.push_right(4), True)
        self.assertIs(dq.push_right(9), False)
        self.assertIs(dq.push_left(9), False)
        self.assertEqual(dq.pop_left(), 0)
        self.assertIs(dq.push_right(7), True)
        self.assertEqual([dq.pop_right(), dq.pop_right(), dq.pop_left()], [7, 4, 4])
        self.assertIs(dq.slots, slots)
        self.assertEqual(dq.slots, [None, None, None])

    def test_single_slot_and_technique(self):
        dq = practice.make_deque(1)
        other = practice.make_deque(1)
        self.assertIs(dq.push_left(0), True)
        self.assertIs(dq.push_right(8), False)
        self.assertIsNone(other.pop_right())
        self.assertEqual(dq.pop_right(), 0)
        self.assertIs(dq.push_right(8), True)
        self.assertEqual(dq.pop_left(), 8)
        self.assertIsNone(dq.pop_left())
        nodes = list(ast.walk(ast.parse(inspect.getsource(practice.make_deque))))
        aliases = {
            alias.asname or alias.name
            for node in nodes if isinstance(node, ast.Import)
            for alias in node.names if alias.name == "collections"
        }
        for node in nodes:
            if isinstance(node, ast.ImportFrom) and node.module == "collections":
                self.assertNotIn("deque", {alias.name for alias in node.names})
            if isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name):
                if node.value.id in aliases:
                    self.assertNotEqual(node.attr, "deque")


class OfferIndex(unittest.TestCase):
    def test_offer(self):
        from collections import deque

        values = [9, 4, 7, 9]
        candidates = deque()
        practice.offer_index(values, candidates, 0)
        self.assertEqual(list(candidates), [0])
        practice.offer_index(values, candidates, 1)
        self.assertEqual(list(candidates), [0, 1])
        practice.offer_index(values, candidates, 2)
        self.assertEqual(list(candidates), [0, 2])
        practice.offer_index(values, candidates, 3)
        self.assertEqual(list(candidates), [3])
        self.assertEqual(values, [9, 4, 7, 9])


class WindowMaxima(unittest.TestCase):
    def test_windows(self):
        cases = (
            ([], 1, []), ([4], 1, [4]), ([1, 3], 0, []), ([1, 3], 3, []),
            ([9, 4, 7, 7], 2, [9, 7, 7]), ([8, 6, 4, 2], 2, [8, 6, 4]),
            ([-8, -6, -4], 2, [-6, -4]), ([2, 1, 2], 3, [2]),
        )
        for values, k, expected in cases:
            before = values[:]
            result = practice.window_maxima(values, k)
            self.assertEqual(result, expected)
            self.assertIsNot(result, values)
            self.assertEqual(values, before)

    def test_linear_reads(self):
        class CountedList(list):
            reads = 0

            def __getitem__(self, index):
                item = super().__getitem__(index)
                self.reads += len(item) if isinstance(index, slice) else 1
                return item

            def __iter__(self):
                for index in range(len(self)):
                    yield self[index]

        values = CountedList(range(400, 0, -1))
        self.assertEqual(practice.window_maxima(values, 150), list(range(400, 149, -1)))
        self.assertLessEqual(values.reads, 16 * len(values), "Keep candidates across windows.")
