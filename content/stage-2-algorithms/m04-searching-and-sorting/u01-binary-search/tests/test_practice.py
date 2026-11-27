import ast
import inspect
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "exercises"))
import practice


def syntax(function):
    return ast.parse(inspect.getsource(function))


class CountedList(list):
    def __init__(self, values):
        super().__init__(values)
        self.reads = 0

    def __getitem__(self, index):
        if isinstance(index, slice):
            self.reads += len(range(*index.indices(len(self))))
        else:
            self.reads += 1
        return super().__getitem__(index)

    def __iter__(self):
        for index in range(len(self)):
            yield self[index]


def check_search(test):
    nodes = list(ast.walk(syntax(practice)))
    test.assertFalse(any(
        isinstance(node, ast.Import) and any(alias.name in {"bisect", "_bisect"} for alias in node.names)
        or isinstance(node, ast.ImportFrom) and node.module in {"bisect", "_bisect"}
        or isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
        and node.func.attr == "index"
        for node in nodes
    ), "Write the search yourself without bisect or list.index.")
    test.assertTrue(any(
        isinstance(node, (ast.For, ast.While)) for node in nodes
    ), "Use a loop to narrow the search range.")


class FindTime(unittest.TestCase):
    def test_technique(self):
        check_search(self)

    def test_edges(self):
        self.assertEqual(practice.find_time([], 5), -1)
        self.assertEqual(practice.find_time([5], 5), 0)
        self.assertEqual(practice.find_time([5], 3), -1)

    def test_repeated_time(self):
        times = [1, 4, 4, 4, 8]
        self.assertIn(practice.find_time(times, 4), (1, 2, 3))
        self.assertEqual(times, [1, 4, 4, 4, 8])
        self.assertEqual(practice.find_time(times, 7), -1)

    def test_few_reads(self):
        values = CountedList(range(0, 8192, 2))
        self.assertEqual(practice.find_time(values, 8190), 4095)
        self.assertLessEqual(values.reads, 40)


class FirstAtLeast(unittest.TestCase):
    def test_technique(self):
        check_search(self)

    def test_edges(self):
        self.assertEqual(practice.first_at_least([], 3), 0)
        self.assertEqual(practice.first_at_least([3], 3), 0)
        self.assertEqual(practice.first_at_least([3], 4), 1)

    def test_insertion_points(self):
        times = [2, 5, 5, 5, 9]
        self.assertEqual(practice.first_at_least(times, 5), 1)
        self.assertEqual(practice.first_at_least(times, 6), 4)
        self.assertEqual(practice.first_at_least(times, 1), 0)
        self.assertEqual(times, [2, 5, 5, 5, 9])

    def test_few_reads(self):
        times = CountedList(range(0, 8192, 2))
        self.assertEqual(practice.first_at_least(times, 4101), 2051)
        self.assertLessEqual(times.reads, 40)


class SmallestCapacity(unittest.TestCase):
    def test_technique(self):
        check_search(self)

    def test_edges(self):
        self.assertEqual(practice.smallest_capacity([], 3), 0)
        self.assertEqual(practice.smallest_capacity([9], 5), 9)
        self.assertEqual(practice.smallest_capacity([3, 4], 1), 7)

    def test_order_and_exact_fit(self):
        sizes = [5, 2, 2, 5]
        self.assertEqual(practice.smallest_capacity(sizes, 2), 7)
        self.assertEqual(practice.smallest_capacity(sizes, 4), 5)
        self.assertEqual(sizes, [5, 2, 2, 5])
        self.assertEqual(practice.smallest_capacity([4, 3, 2], 2), 5)
        self.assertEqual(practice.smallest_capacity([5, 5, 2, 2], 2), 9)
        self.assertEqual(practice.smallest_capacity([2, 5, 5, 2], 2), 7)

    def test_wide_capacity_range(self):
        sizes = [700_000_000] * 5
        self.assertEqual(practice.smallest_capacity(sizes, 2), 2_100_000_000)


if __name__ == "__main__":
    unittest.main()
