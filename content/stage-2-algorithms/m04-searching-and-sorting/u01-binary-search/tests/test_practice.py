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

    def __reversed__(self):
        for index in range(len(self) - 1, -1, -1):
            yield self[index]

    def __contains__(self, value):
        return any(item == value for item in self)

    def __add__(self, other):
        self.reads += len(self)
        return list.__add__(self, other)

    def __radd__(self, other):
        self.reads += len(self)
        return other + list(list.__iter__(self))

    def copy(self):
        self.reads += len(self)
        return list(list.__iter__(self))

    def index(self, *args):
        self.reads += len(self)
        return list.index(self, *args)

    def count(self, value):
        self.reads += len(self)
        return list.count(self, value)

    def snapshot(self):
        return list(list.__iter__(self))


class CountedInt(int):
    operations = 0

    def _arith(name):
        def method(self, other):
            CountedInt.operations += 1
            return CountedInt(getattr(int, name)(int(self), other))
        return method

    def _compare(name):
        def method(self, other):
            CountedInt.operations += 1
            return getattr(int, name)(int(self), other)
        return method

    __add__ = _arith("__add__")
    __radd__ = _arith("__radd__")
    __sub__ = _arith("__sub__")
    __rsub__ = _arith("__rsub__")
    __gt__ = _compare("__gt__")
    __ge__ = _compare("__ge__")
    __lt__ = _compare("__lt__")
    __le__ = _compare("__le__")


def check_search(test):
    nodes = list(ast.walk(syntax(practice)))
    test.assertFalse(any(
        isinstance(node, ast.Import) and any(alias.name.split(".")[0] in {"bisect", "_bisect", "importlib"}
                                             for alias in node.names)
        or isinstance(node, ast.ImportFrom) and (node.module or "").split(".")[0] in {"bisect", "_bisect", "importlib"}
        or isinstance(node, ast.Constant) and node.value in {"bisect", "_bisect"}
        for node in nodes
    ), "Write the search yourself without bisect.")
    test.assertTrue(any(
        isinstance(node, (ast.For, ast.While)) for node in nodes
    ), "Use a loop to narrow the search range.")


def brute_capacity(sizes, days):
    capacity = max(sizes)
    while True:
        needed, used = 1, 0
        for size in sizes:
            if used + size > capacity:
                needed += 1
                used = 0
            used += size
        if needed <= days:
            return capacity
        capacity += 1


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
        for target, expected in ((8190, 4095), (0, 0), (4096, 2048)):
            values = CountedList(range(0, 8192, 2))
            self.assertEqual(practice.find_time(values, target), expected)
            self.assertLessEqual(values.reads, 20)
        for target in (-1, 8191, 3001):
            values = CountedList(range(0, 8192, 2))
            self.assertEqual(practice.find_time(values, target), -1)
            self.assertLessEqual(values.reads, 20)

    def test_long_runs_stay_cheap(self):
        times = [1] * 1000 + [2] * 3000 + [3] * 96
        values = CountedList(times)
        found = practice.find_time(values, 2)
        self.assertTrue(1000 <= found < 4000)
        self.assertLessEqual(values.reads, 20)
        self.assertEqual(values.snapshot(), times)

    def test_matches_membership(self):
        times = [0, 0, 3, 5, 5, 5, 9, 12, 12]
        for target in range(-1, 15):
            found = practice.find_time(times, target)
            if target in times:
                self.assertEqual(times[found], target)
            else:
                self.assertEqual(found, -1)


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
        for limit, expected in ((4101, 2051), (-5, 0), (8190, 4095), (9000, 4096), (0, 0)):
            times = CountedList(range(0, 8192, 2))
            self.assertEqual(practice.first_at_least(times, limit), expected)
            self.assertLessEqual(times.reads, 20)

    def test_long_runs_stay_cheap(self):
        data = [1] * 1000 + [2] * 3000 + [3] * 96
        for limit, expected in ((2, 1000), (3, 4000), (1, 0), (4, 4096)):
            times = CountedList(data)
            self.assertEqual(practice.first_at_least(times, limit), expected)
            self.assertLessEqual(times.reads, 20)
            self.assertEqual(times.snapshot(), data)

    def test_matches_linear_scan(self):
        times = [0, 0, 3, 5, 5, 5, 9, 12, 12]
        for limit in range(-1, 15):
            expected = sum(1 for value in times if value < limit)
            self.assertEqual(practice.first_at_least(times, limit), expected)


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

    def test_matches_brute_force(self):
        import random
        rng = random.Random(7)
        for _ in range(150):
            sizes = [rng.randint(1, 12) for _ in range(rng.randint(1, 9))]
            before = list(sizes)
            days = rng.randint(1, 10)
            self.assertEqual(practice.smallest_capacity(sizes, days), brute_capacity(before, days))
            self.assertEqual(sizes, before)

    def test_scan_count_is_logarithmic(self):
        sizes = CountedList([10**9] * 100)
        self.assertEqual(practice.smallest_capacity(sizes, 7), 15 * 10**9)
        self.assertLessEqual(sizes.reads, 6000)
        CountedInt.operations = 0
        heavy = [CountedInt(10**9) for _ in range(100)]
        self.assertEqual(practice.smallest_capacity(heavy, 30), 4 * 10**9)
        self.assertLessEqual(CountedInt.operations, 40000)
        rng_sizes = CountedList([(index * 7919) % 10**9 + 1 for index in range(100)])
        before = rng_sizes.snapshot()
        practice.smallest_capacity(rng_sizes, 13)
        self.assertLessEqual(rng_sizes.reads, 6000)
        self.assertEqual(rng_sizes.snapshot(), before)


if __name__ == "__main__":
    unittest.main()
