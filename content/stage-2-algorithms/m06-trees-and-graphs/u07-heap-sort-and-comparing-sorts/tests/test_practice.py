import ast
import inspect
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "exercises"))
import practice


def sift_down_max(values, i, end):
    while 2*i + 1 < end:
        child = 2*i + 1
        right = child + 1
        if right < end and values[right] > values[child]:
            child = right
        if values[i] >= values[child]:
            break
        values[i], values[child] = values[child], values[i]
        i = child


def check_manual(test, function):
    tree = ast.parse(inspect.getsource(practice))
    for item in tree.body:
        if isinstance(item, ast.FunctionDef) and item.name not in {
            function.__name__, "sift_down_max"
        }:
            continue
        for node in ast.walk(item):
            if isinstance(node, ast.Import):
                test.assertTrue(all(alias.name not in {"heapq", "_heapq"} for alias in node.names))
            if isinstance(node, ast.ImportFrom):
                test.assertNotIn(node.module, {"heapq", "_heapq"})
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    test.assertNotEqual(node.func.id, "sorted")
                if isinstance(node.func, ast.Attribute):
                    test.assertNotIn(node.func.attr, {"sort", "sorted"})


class CountedInt(int):
    comparisons = 0

    def __lt__(self, other):
        CountedInt.comparisons += 1
        return super().__lt__(other)

    def __le__(self, other):
        CountedInt.comparisons += 1
        return super().__le__(other)

    def __gt__(self, other):
        CountedInt.comparisons += 1
        return super().__gt__(other)

    def __ge__(self, other):
        CountedInt.comparisons += 1
        return super().__ge__(other)


class SiftDownMax(unittest.TestCase):
    def test_single_and_no_right_child(self):
        values = [2, 4, 9]
        self.assertIsNone(practice.sift_down_max(values, 0, 1))
        self.assertEqual(values, [2, 4, 9])
        practice.sift_down_max(values, 0, 2)
        self.assertEqual(values, [4, 2, 9])

    def test_multiple_swaps_and_technique(self):
        values = [1, 7, 5, 2, 4, 12]
        practice.sift_down_max(values, 0, 5)
        self.assertEqual(values, [7, 4, 5, 2, 1, 12])
        check_manual(self, practice.sift_down_max)

    def test_subtree_and_duplicates(self):
        values = [10, 1, 9, 6, 6]
        practice.sift_down_max(values, 1, 5)
        self.assertEqual(values[:3], [10, 6, 9])
        self.assertCountEqual(values[3:], [1, 6])


class MoveMax(unittest.TestCase):
    def test_two_items(self):
        values = [4, 4]
        self.assertEqual(practice.move_max(values, 2, sift_down_max), 1)
        self.assertEqual(values, [4, 4])

    def test_shrinks_prefix_and_keeps_suffix(self):
        values = [9, 6, 4, 2, 12]
        result = practice.move_max(values, 4, sift_down_max)
        self.assertEqual(result, 3)
        self.assertEqual(values, [6, 2, 4, 9, 12])


class HeapSort(unittest.TestCase):
    def test_empty_and_single(self):
        for values in ([], [5]):
            with self.subTest(values=values):
                expected = values.copy()
                self.assertIsNone(practice.heap_sort(values))
                self.assertEqual(values, expected)

    def test_order_and_in_place(self):
        for values in ([4, -1, 4, 0], [1, 2, 3, 4, 5], [6, 5, 4, 3, 2, 1], [5, 5, 5]):
            with self.subTest(values=values):
                expected = sorted(values)
                alias = values
                self.assertIsNone(practice.heap_sort(values))
                self.assertEqual(alias, expected)
        check_manual(self, practice.heap_sort)

    def test_comparison_budget(self):
        n = 512
        values = [CountedInt((i * 337) % n) for i in range(n)]
        CountedInt.comparisons = 0
        practice.heap_sort(values)
        self.assertEqual(values, list(range(n)))
        self.assertLess(CountedInt.comparisons, 6 * n * n.bit_length())
