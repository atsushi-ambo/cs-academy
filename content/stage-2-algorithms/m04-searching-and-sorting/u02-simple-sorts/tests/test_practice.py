import ast
import inspect
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "exercises"))
import practice


def syntax(function):
    return ast.parse(inspect.getsource(function))


SORT_NAMES = {"sorted", "sort", "insort", "insort_left", "insort_right", "nsmallest", "nlargest"}
SORT_MODULES = {"heapq", "bisect", "importlib"}


def bound_names(tree):
    names = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            names.add(node.name)
        elif isinstance(node, ast.arg):
            names.add(node.arg)
        elif isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
            names.add(node.id)
        elif isinstance(node, (ast.Import, ast.ImportFrom)):
            names.update((alias.asname or alias.name).split(".")[0] for alias in node.names)
    return names


def reachable(tree, entry):
    functions = {node.name: node for node in tree.body if isinstance(node, ast.FunctionDef)}
    seen, pending = [], [entry]
    while pending:
        name = pending.pop()
        if name in functions and name not in seen:
            seen.append(name)
            pending.extend(node.id for node in ast.walk(functions[name]) if isinstance(node, ast.Name))
    module = ast.Module(body=[functions[name] for name in seen], type_ignores=[])
    return module


def uses_names(tree, forbidden, scope=None):
    bound = bound_names(tree)
    if scope is not None:
        tree = reachable(tree, scope)
    for node in ast.walk(tree):
        if isinstance(node, ast.Name) and node.id in forbidden and node.id not in bound:
            return True
        if isinstance(node, ast.Attribute) and node.attr in forbidden:
            return True
        if isinstance(node, ast.Constant) and isinstance(node.value, str) and node.value in forbidden:
            return True
        if isinstance(node, ast.Import) and any(alias.name.split(".")[0] in SORT_MODULES
                                                for alias in node.names):
            return True
        if isinstance(node, ast.ImportFrom) and (node.module or "").split(".")[0] in SORT_MODULES:
            return True
    return False


def uses_library_sort(tree):
    return uses_names(tree, SORT_NAMES)


def has_loop(tree):
    return any(isinstance(node, (ast.For, ast.While)) for node in ast.walk(tree))


def check_manual_sort(test):
    tree = syntax(practice)
    test.assertFalse(uses_library_sort(tree), "Write the sort without sorted() or list.sort().")
    test.assertTrue(has_loop(tree), "Compare and move the items in a loop.")


class Key(int):
    log = []

    def _compare(name):
        def method(self, other):
            Key.log.append(frozenset((id(self), id(other))))
            return getattr(int, name)(self, other)
        return method

    __lt__ = _compare("__lt__")
    __le__ = _compare("__le__")
    __gt__ = _compare("__gt__")
    __ge__ = _compare("__ge__")

    __hash__ = int.__hash__


def keys(values):
    Key.log = []
    return [Key(value) for value in values]


def pairs_of(items):
    return [frozenset((id(items[i]), id(items[i + 1]))) for i in range(len(items) - 1)]


def reference_bubble(values):
    result = list(values)
    checks = 0
    for end in range(len(result) - 1, 0, -1):
        swapped = False
        for j in range(end):
            checks += 1
            if result[j] > result[j + 1]:
                result[j], result[j + 1] = result[j + 1], result[j]
                swapped = True
        if not swapped:
            break
    return result, checks


def random_lists():
    import random
    rng = random.Random(11)
    for _ in range(60):
        yield [rng.randint(-5, 9) for _ in range(rng.randint(0, 14))]


class SelectionReport(unittest.TestCase):
    def test_technique(self):
        tree = syntax(practice)
        self.assertFalse(uses_library_sort(tree))
        self.assertFalse(uses_names(tree, {"min"}, "selection_report"), "Find the minimum with your own comparisons.")
        self.assertTrue(has_loop(tree))

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

    def test_each_pass_tracks_one_candidate(self):
        items = keys(range(1, 9))
        result, checks = practice.selection_report(items)
        self.assertEqual(checks, 28)
        self.assertEqual(len(Key.log), 28)
        position = 0
        for start in range(7):
            chunk = Key.log[position:position + 7 - start]
            self.assertEqual(len(chunk), 7 - start)
            self.assertTrue(all(id(items[start]) in pair for pair in chunk),
                            "Compare every later item with the best item of this pass.")
            position += 7 - start

    def test_comparisons_match_values_on_mixed_inputs(self):
        for values in random_lists():
            items = keys(values)
            result, checks = practice.selection_report(items)
            self.assertEqual([int(item) for item in result], sorted(values))
            self.assertEqual(sorted(map(id, result)), sorted(map(id, items)))
            self.assertEqual(checks, len(values) * (len(values) - 1) // 2)
            self.assertEqual(len(Key.log), checks)
            self.assertEqual([int(item) for item in items], values)

    def test_larger_input(self):
        values = list(range(200, 0, -1))
        result, checks = practice.selection_report(values)
        self.assertEqual(result, sorted(values))
        self.assertEqual(checks, 19900)


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

    def test_shifts_from_the_right(self):
        count = 60
        ordered = list(zip(keys(range(count)), "x" * count))
        practice.insertion_jobs(ordered)
        self.assertLessEqual(len(Key.log), 2 * count)
        reverse = list(zip(keys(range(count, 0, -1)), "x" * count))
        result = practice.insertion_jobs(reverse)
        self.assertEqual([int(key) for key, _ in result], list(range(1, count + 1)))
        self.assertGreaterEqual(len(Key.log), count * (count - 1) // 4)

    def test_stable_on_larger_mixed_input(self):
        import random
        rng = random.Random(5)
        jobs = [(rng.randint(0, 6), f"n{i}") for i in range(150)]
        before = list(jobs)
        expected = sorted(jobs, key=lambda job: job[0])
        self.assertEqual(practice.insertion_jobs(jobs), expected)
        self.assertEqual(jobs, before)


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

    def test_compares_neighbors_in_order(self):
        items = keys(range(1, 9))
        practice.bubble_report(items)
        self.assertEqual(Key.log, pairs_of(items))

    def test_counts_match_real_comparisons(self):
        for values in random_lists():
            items = keys(values)
            result, checks = practice.bubble_report(items)
            expected, expected_checks = reference_bubble(values)
            self.assertEqual([int(item) for item in result], expected)
            self.assertEqual(checks, expected_checks)
            self.assertEqual(len(Key.log), checks)
            self.assertEqual([int(item) for item in items], values)

    def test_larger_input(self):
        values = list(range(200, 0, -1))
        self.assertEqual(practice.bubble_report(values), (sorted(values), 19900))
        ordered = list(range(200))
        self.assertEqual(practice.bubble_report(ordered), (ordered, 199))


if __name__ == "__main__":
    unittest.main()
