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


def uses_recursion(function):
    # Resolve nested helpers in the scope of their enclosing function.
    def definitions(nodes):
        return {node.name: node for node in nodes if isinstance(node, ast.FunctionDef)}

    def called_names(node):
        for child in ast.iter_child_nodes(node):
            if isinstance(child, ast.FunctionDef):
                continue
            if isinstance(child, ast.Call) and isinstance(child.func, ast.Name):
                yield child.func.id
            yield from called_names(child)

    def has_cycle(node, scope, active):
        if node in active:
            return True
        visible = {**scope, **definitions(node.body)}
        return any(has_cycle(visible[name], visible, active | {node})
                   for name in called_names(node) if name in visible)

    outer = definitions(syntax(practice).body)
    return has_cycle(outer[function.__name__], outer, set())


def check_no_sort(test):
    test.assertFalse(uses_library_sort(syntax(practice)), "Write the sort without sorted() or list.sort().")


class MergeJobs(unittest.TestCase):
    def test_technique(self):
        check_no_sort(self)
        self.assertTrue(any(isinstance(node, (ast.For, ast.While))
                            for node in ast.walk(syntax(practice))))

    def test_empty_and_one(self):
        lone = [(5, "one")]
        result = practice.merge_jobs([], lone)
        self.assertEqual(result, lone)
        self.assertIsNot(result, lone)
        self.assertEqual(practice.merge_jobs([], []), [])

    def test_ties_and_nonmutation(self):
        left = [(1, "z"), (4, "y"), (4, "x")]
        right = [(4, "b"), (6, "a")]
        self.assertEqual(practice.merge_jobs(left, right),
                         [(1, "z"), (4, "y"), (4, "x"), (4, "b"), (6, "a")])
        self.assertEqual(left, [(1, "z"), (4, "y"), (4, "x")])
        self.assertEqual(right, [(4, "b"), (6, "a")])

    def test_interleaved(self):
        self.assertEqual(practice.merge_jobs([(2, "a"), (6, "b")], [(4, "c")]),
                         [(2, "a"), (4, "c"), (6, "b")])


class MergeSort(unittest.TestCase):
    def test_technique(self):
        check_no_sort(self)
        self.assertTrue(uses_recursion(practice.merge_sort))

    def test_empty_and_one(self):
        single = [(4, "x")]
        result = practice.merge_sort(single)
        self.assertEqual(result, single)
        self.assertIsNot(result, single)
        self.assertEqual(practice.merge_sort([]), [])

    def test_ties_across_halves(self):
        events = [(3, "b"), (1, "x"), (3, "a"), (0, "w"), (1, "y")]
        self.assertEqual(practice.merge_sort(events),
                         [(0, "w"), (1, "x"), (1, "y"), (3, "b"), (3, "a")])
        self.assertEqual(events, [(3, "b"), (1, "x"), (3, "a"), (0, "w"), (1, "y")])

    def test_reverse(self):
        events = [(i, "job") for i in range(511, -1, -1)]
        self.assertEqual(practice.merge_sort(events), events[::-1])


class LomutoPartition(unittest.TestCase):
    def test_technique(self):
        check_no_sort(self)
        self.assertTrue(any(isinstance(node, (ast.For, ast.While))
                            for node in ast.walk(syntax(practice))))

    def test_single(self):
        values = [4]
        self.assertEqual(practice.lomuto_partition(values, 0, 0), 0)
        self.assertEqual(values, [4])

    def test_subrange_with_ties(self):
        values = [90, 7, 3, 5, 3, 3, -90]
        pivot_index = practice.lomuto_partition(values, 1, 5)
        self.assertEqual(pivot_index, 3)
        self.assertEqual(values[pivot_index], 3)
        self.assertEqual(values[0], 90)
        self.assertEqual(values[-1], -90)
        self.assertCountEqual(values[1:6], [7, 3, 5, 3, 3])
        self.assertTrue(all(item <= 3 for item in values[1:pivot_index]))
        self.assertTrue(all(item > 3 for item in values[pivot_index + 1:6]))

    def test_smallest_and_largest_pivot(self):
        self.assertEqual(practice.lomuto_partition([7, 4, 0], 0, 2), 0)
        self.assertEqual(practice.lomuto_partition([1, 2, 9], 0, 2), 2)


class HoarePartition(unittest.TestCase):
    def test_technique(self):
        check_no_sort(self)
        self.assertTrue(any(isinstance(node, (ast.For, ast.While))
                            for node in ast.walk(syntax(practice))))

    def assert_partition(self, chunk):
        values = [90] + chunk + [-90]
        pivot = chunk[0]
        cut = practice.hoare_partition(values, 1, len(chunk))
        self.assertTrue(1 <= cut < len(chunk))
        self.assertTrue(all(item <= pivot for item in values[1:cut + 1]))
        self.assertTrue(all(item >= pivot for item in values[cut + 1:-1]))
        self.assertEqual(values[0], 90)
        self.assertEqual(values[-1], -90)
        self.assertCountEqual(values[1:-1], chunk)

    def test_two_items_and_ties(self):
        self.assert_partition([4, 1])
        self.assert_partition([1, 4])
        self.assert_partition([3, 3, 3, 3])

    def test_mixed_subrange(self):
        self.assert_partition([4, 9, 2, 6, 4, 1, 8])
        self.assert_partition([8, 7, 5, 3, 1])


class QuickSort(unittest.TestCase):
    def test_technique(self):
        check_no_sort(self)
        self.assertTrue(uses_recursion(practice.quick_sort))

    def test_empty_and_one(self):
        for values in ([], [8]):
            before = values[:]
            self.assertIsNone(practice.quick_sort(values))
            self.assertEqual(values, before)

    def test_ties_and_negatives(self):
        values = [7, 2, 7, -3, 2, 4, 0]
        self.assertIsNone(practice.quick_sort(values))
        self.assertEqual(values, [-3, 0, 2, 2, 4, 7, 7])

    def test_ordered_reversed_and_equal(self):
        expected = list(range(256))
        for values in (expected[:], expected[::-1], [5] * 256):
            target = expected if values[0] != 5 else [5] * 256
            practice.quick_sort(values)
            self.assertEqual(values, target)


if __name__ == "__main__":
    unittest.main()
