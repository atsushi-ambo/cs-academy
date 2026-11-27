import ast
import inspect
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "exercises"))
import practice


def syntax(function):
    return ast.parse(inspect.getsource(function))


def uses_library_sort(tree):
    return any(
        isinstance(node, ast.Call) and (
            isinstance(node.func, ast.Name) and node.func.id == "sorted"
            or isinstance(node.func, ast.Attribute) and node.func.attr in {"sort", "sorted"}
        )
        or isinstance(node, ast.ImportFrom) and any(
            alias.name in {"sorted", "sort"} for alias in node.names
        )
        for node in ast.walk(tree)
    )


def has_loop(tree):
    return any(isinstance(node, (ast.For, ast.While)) for node in ast.walk(tree))


def check_manual_sort(test):
    tree = syntax(practice)
    test.assertFalse(uses_library_sort(tree), "Write the sort without sorted() or list.sort().")
    test.assertTrue(has_loop(tree), "Compare and move the items in a loop.")


class SelectionReport(unittest.TestCase):
    def test_technique(self):
        tree = syntax(practice)
        self.assertFalse(uses_library_sort(tree))
        self.assertTrue(has_loop(tree))
        self.assertFalse(any(isinstance(node, ast.Call) and (
            isinstance(node.func, ast.Name) and node.func.id == "min"
            or isinstance(node.func, ast.Attribute) and node.func.attr == "min"
        ) for node in ast.walk(tree)), "Find the minimum with your own comparisons.")

    def test_empty_and_one(self):
        self.assertEqual(practice.selection_report([]), ([], 0))
        single = [7]
        result, checks = practice.selection_report(single)
        self.assertIsNot(result, single)
        self.assertEqual((result, checks), ([7], 0))

    def test_duplicate_sizes(self):
        sizes = [5, 2, 3, 2]
        self.assertEqual(practice.selection_report(sizes), ([2, 2, 3, 5], 6))
        self.assertEqual(sizes, [5, 2, 3, 2])

    def test_sorted_still_costs_comparisons(self):
        self.assertEqual(practice.selection_report([1, 2, 3, 4, 5]), ([1, 2, 3, 4, 5], 10))


class InsertionJobs(unittest.TestCase):
    def test_technique(self):
        check_manual_sort(self)

    def test_empty_and_one(self):
        jobs = []
        self.assertEqual(practice.insertion_jobs(jobs), [])
        self.assertIsNot(practice.insertion_jobs(jobs), jobs)
        self.assertEqual(practice.insertion_jobs([(4, "n")]), [(4, "n")])

    def test_ties_and_input(self):
        jobs = [(5, "x"), (2, "z"), (5, "a"), (2, "b"), (-1, "y")]
        self.assertEqual(practice.insertion_jobs(jobs),
                         [(-1, "y"), (2, "z"), (2, "b"), (5, "x"), (5, "a")])
        self.assertEqual(jobs, [(5, "x"), (2, "z"), (5, "a"), (2, "b"), (-1, "y")])

    def test_move_to_start(self):
        self.assertEqual(practice.insertion_jobs([(8, "a"), (3, "b"), (1, "c")]),
                         [(1, "c"), (3, "b"), (8, "a")])


class BubbleReport(unittest.TestCase):
    def test_technique(self):
        check_manual_sort(self)

    def test_empty_and_one(self):
        empty = []
        result, checks = practice.bubble_report(empty)
        self.assertIsNot(result, empty)
        self.assertEqual((result, checks), ([], 0))
        self.assertEqual(practice.bubble_report([1]), ([1], 0))

    def test_unsorted_and_repeats(self):
        values = [3, 2, 1, 2]
        self.assertEqual(practice.bubble_report(values), ([1, 2, 2, 3], 6))
        self.assertEqual(values, [3, 2, 1, 2])

    def test_early_stop(self):
        self.assertEqual(practice.bubble_report([1, 1, 1, 4, 6]), ([1, 1, 1, 4, 6], 4))
        self.assertEqual(practice.bubble_report([2, 1, 3, 4, 5]), ([1, 2, 3, 4, 5], 7))


if __name__ == "__main__":
    unittest.main()
