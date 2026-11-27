import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "exercises"))
import practice



def reject_shortcuts(test, function, names):
    import ast
    import inspect

    for node in ast.walk(ast.parse(inspect.getsource(function))):
        if isinstance(node, ast.Call):
            name = node.func
            if isinstance(name, ast.Name):
                test.assertNotIn(name.id, names)
            elif isinstance(name, ast.Attribute):
                test.assertNotIn(name.attr, names)
        elif isinstance(node, (ast.Import, ast.ImportFrom)):
            for imported in node.names:
                test.assertNotIn(imported.name, names)


class CountCodes(unittest.TestCase):
    def test_counts(self):
        self.assertEqual(practice.count_codes([]), {})
        self.assertEqual(practice.count_codes([200]), {200: 1})
        codes = [503, 200, 503, 503, 0]
        self.assertEqual(practice.count_codes(codes), {503: 3, 200: 1, 0: 1})
        self.assertEqual(codes, [503, 200, 503, 503, 0])
        reject_shortcuts(self, practice.count_codes, {"Counter", "count", "collections.Counter"})


class GroupTimes(unittest.TestCase):
    def test_groups(self):
        self.assertEqual(practice.group_times([]), {})
        self.assertEqual(practice.group_times([("api", 4)]), {"api": [4]})
        rows = [("api", 4), ("db", 9), ("api", 2), ("api", 4)]
        before = rows[:]
        groups = practice.group_times(rows)
        self.assertEqual(groups, {"api": [4, 2, 4], "db": [9]})
        groups["api"].append(7)
        self.assertEqual(groups["db"], [9])
        self.assertEqual(practice.group_times(rows), {"api": [4, 2, 4], "db": [9]})
        self.assertEqual(rows, before)

    def test_order_inside_group(self):
        rows = [("api", 503), ("db", 7), ("api", 200), ("api", 503), ("db", 3)]
        self.assertEqual(practice.group_times(rows), {"api": [503, 200, 503], "db": [7, 3]})


class TwoSum(unittest.TestCase):
    def test_pair(self):
        for values, target, expected in (
            ([], 5, None), ([5], 10, None), ([5, 5], 10, (0, 1)),
            ([4, 4, 6], 10, (0, 2)), ([4, 2, 8, 6], 10, (1, 2)),
            ([-5, 7, 0], 2, (0, 1)), ([0, 4, 8], 11, None),
        ):
            before = values[:]
            self.assertEqual(practice.two_sum(values, target), expected)
            self.assertEqual(values, before)

    def test_lookup_work(self):
        class ReadList(list):
            reads = 0

            def __getitem__(self, index):
                value = super().__getitem__(index)
                self.reads += len(value) if isinstance(index, slice) else 1
                return value

            def __iter__(self):
                for i in range(len(self)):
                    yield self[i]

        values = ReadList(range(1, 201))
        self.assertIsNone(practice.two_sum(values, -1))
        self.assertLessEqual(values.reads, 6 * len(values), "Use earlier positions in a dict.")

    def test_arithmetic_work_is_linear(self):
        class Counted(int):
            ops = 0

            def _count(self):
                Counted.ops += 1

            def __add__(self, other):
                self._count()
                return int(self) + int(other)

            def __radd__(self, other):
                self._count()
                return int(other) + int(self)

            def __sub__(self, other):
                self._count()
                return int(self) - int(other)

            def __rsub__(self, other):
                self._count()
                return int(other) - int(self)

            def __eq__(self, other):
                self._count()
                return int(self) == int(other)

            def __ne__(self, other):
                self._count()
                return int(self) != int(other)

            __hash__ = int.__hash__

        size = 300
        for target, expected in ((-1, None), (2 * size - 1, (size - 2, size - 1))):
            Counted.ops = 0
            values = [Counted(n) for n in range(1, size + 1)]
            self.assertEqual(practice.two_sum(values, target), expected)
            self.assertLessEqual(Counted.ops, 8 * size, "Use a dict instead of comparing every pair.")
