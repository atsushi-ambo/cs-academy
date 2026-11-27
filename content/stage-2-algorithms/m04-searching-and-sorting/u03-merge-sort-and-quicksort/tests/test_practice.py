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
    return names


def uses_library_sort(tree):
    bound = bound_names(tree)
    for node in ast.walk(tree):
        if isinstance(node, ast.Name) and node.id in SORT_NAMES and node.id not in bound:
            return True
        if isinstance(node, ast.Attribute) and node.attr in SORT_NAMES:
            return True
        if isinstance(node, ast.Constant) and isinstance(node.value, str) and node.value in SORT_MODULES | SORT_NAMES:
            return True
        if isinstance(node, ast.Import) and any(alias.name.split(".")[0] in SORT_MODULES
                                                for alias in node.names):
            return True
        if isinstance(node, ast.ImportFrom) and (node.module or "").split(".")[0] in SORT_MODULES:
            return True
    return False


class Key(int):
    log = []

    def _compare(name):
        def method(self, other):
            Key.log.append(1)
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


def trace_frames(call):
    stack, state = [], {"recursed": False, "depth": 0}
    own = practice.__file__

    def profile(frame, event, argument):
        if frame.f_code.co_filename != own or frame.f_code.co_name.startswith("<"):
            return
        if event == "call":
            if frame.f_code in stack:
                state["recursed"] = True
            stack.append(frame.f_code)
            state["depth"] = max(state["depth"], len(stack))
        elif event == "return" and stack:
            stack.pop()

    sys.setprofile(profile)
    try:
        result = call()
    finally:
        sys.setprofile(None)
    return result, state


class SliceCountingList(list):
    copies = 0

    def __getitem__(self, index):
        if isinstance(index, slice):
            SliceCountingList.copies += 1
        return super().__getitem__(index)

    def __iter__(self):
        SliceCountingList.copies += 1
        return super().__iter__()

    def copy(self):
        SliceCountingList.copies += 1
        return super().copy()


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

    def test_one_sweep_over_large_runs(self):
        left = [(Key(2 * index), f"l{index}") for index in range(200)]
        right = [(Key(2 * index + 1), f"r{index}") for index in range(200)]
        Key.log = []
        result = practice.merge_jobs(left, right)
        self.assertEqual([int(job[0]) for job in result], list(range(400)))
        self.assertLessEqual(len(Key.log), 400)

    def test_ties_keep_left_first_in_long_runs(self):
        left = [(index // 3, f"l{index}") for index in range(60)]
        right = [(index // 2, f"r{index}") for index in range(40)]
        expected = [job for _, job in sorted(
            [(job[0], (0, i, job)) for i, job in enumerate(left)]
            + [(job[0], (1, i, job)) for i, job in enumerate(right)])]
        self.assertEqual(practice.merge_jobs(left, right), [job[2] for job in expected])
        self.assertEqual(practice.merge_jobs(right, []), right)
        self.assertEqual(practice.merge_jobs([], left), left)


class MergeSort(unittest.TestCase):
    def test_technique(self):
        check_no_sort(self)
        _, state = trace_frames(lambda: practice.merge_sort([(3, "a"), (1, "b"), (2, "c"), (0, "d")]))
        self.assertTrue(state["recursed"], "Use recursion to split the list.")

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

    def test_halves_and_log_comparisons(self):
        import random
        rng = random.Random(3)
        data = [(Key(rng.randint(0, 40)), f"n{index}") for index in range(512)]
        before = list(data)
        Key.log = []
        result = practice.merge_sort(data)
        expected = sorted(before, key=lambda job: int(job[0]))
        self.assertEqual([(int(a), b) for a, b in result], [(int(a), b) for a, b in expected])
        self.assertEqual(data, before)
        self.assertLessEqual(len(Key.log), 512 * 9)

    def test_call_depth_is_logarithmic(self):
        events = [(index % 7, "job") for index in range(512)]
        self.assertLessEqual(trace_frames(lambda: practice.merge_sort(events))[1]["depth"], 25)


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
        _, state = trace_frames(lambda: practice.quick_sort([5, 3, 8, 1, 9, 2]))
        self.assertTrue(state["recursed"], "Use recursion on both sides of the split.")

    def test_empty_and_one(self):
        for values in ([], [8]):
            before = values[:]
            self.assertIsNone(practice.quick_sort(values))
            self.assertEqual(values, before)

    def test_ties_and_negatives(self):
        values = [7, 2, 7, -3, 2, 4, 0]
        self.assertIsNone(practice.quick_sort(values))
        self.assertEqual(values, [-3, 0, 2, 2, 4, 7, 7])

    def test_sorts_in_place_without_copies(self):
        import random
        rng = random.Random(9)
        data = [rng.randint(-20, 20) for _ in range(256)]
        values = SliceCountingList(data)
        SliceCountingList.copies = 0
        self.assertIsNone(practice.quick_sort(values))
        self.assertEqual(list(list.__iter__(values)), sorted(data))
        self.assertEqual(SliceCountingList.copies, 0, "Sort inside the list, without copies.")

    def test_comparison_count_stays_near_n_log_n(self):
        import random
        rng = random.Random(4)
        values = keys(rng.sample(range(1000), 256))
        practice.quick_sort(values)
        self.assertEqual([int(item) for item in values], sorted(int(item) for item in values))
        self.assertLessEqual(len(Key.log), 8000)

    def test_many_ties_and_pattern_inputs(self):
        for values in ([3, 1] * 100, [0] * 50 + [1] * 50, [1] * 50 + [0] * 50,
                       list(range(100)) + list(range(100))[::-1]):
            expected = sorted(values)
            practice.quick_sort(values)
            self.assertEqual(values, expected)

    def test_ordered_reversed_and_equal(self):
        expected = list(range(256))
        for values in (expected[:], expected[::-1], [5] * 256):
            target = expected if values[0] != 5 else [5] * 256
            practice.quick_sort(values)
            self.assertEqual(values, target)


if __name__ == "__main__":
    unittest.main()
