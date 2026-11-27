import ast
import inspect
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "exercises"))
import practice


def sift_up(heap, i):
    while i > 0:
        parent = (i - 1) // 2
        if heap[parent] <= heap[i]:
            break
        heap[i], heap[parent] = heap[parent], heap[i]
        i = parent
def sift_down(heap, i):
    while 2*i + 1 < len(heap):
        child = 2*i + 1
        right = child + 1
        if right < len(heap) and heap[right] < heap[child]:
            child = right
        if heap[i] <= heap[child]:
            break
        heap[i], heap[child] = heap[child], heap[i]
        i = child


FORBIDDEN_NAMES = {"sorted", "__import__", "importlib", "builtins", "eval", "exec", "getattr"}
FORBIDDEN_TEXT = {"sort", "sorted", "heapq", "_heapq"}


def heapq_aliases(tree):
    aliases = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name.split(".")[0] in {"heapq", "_heapq"}:
                    aliases.add((alias.asname or alias.name).split(".")[0])
        if isinstance(node, ast.ImportFrom) and (node.module or "").split(".")[0] in {"heapq", "_heapq"}:
            for alias in node.names:
                aliases.add(alias.asname or alias.name)
    return aliases


def check_manual(test, function=None):
    """Whole-module check: only schedule may touch heapq. No sorting anywhere."""
    tree = ast.parse(inspect.getsource(practice))
    aliases = heapq_aliases(tree)
    scopes = [node for node in tree.body if not (isinstance(node, ast.FunctionDef) and node.name == "schedule")]
    for scope in scopes:
        if isinstance(scope, (ast.Import, ast.ImportFrom)):
            continue
        for node in ast.walk(scope):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                names = [alias.name for alias in node.names] + [getattr(node, "module", None) or ""]
                test.assertFalse(
                    any(name.split(".")[0] in {"heapq", "_heapq", "importlib", "builtins"} for name in names),
                    "Do not import a heap library outside schedule.",
                )
            if isinstance(node, ast.Name):
                test.assertNotIn(node.id, FORBIDDEN_NAMES | aliases)
            if isinstance(node, ast.Attribute):
                test.assertNotIn(node.attr, {"sort", "sorted", "heapify", "heappush", "heappop", "nsmallest"})
            if isinstance(node, ast.Constant) and isinstance(node.value, str):
                test.assertNotIn(node.value, FORBIDDEN_TEXT)


def is_heap_at(heap, root):
    if root >= len(heap):
        return True
    for child in (2 * root + 1, 2 * root + 2):
        if child < len(heap):
            if heap[root] > heap[child] or not is_heap_at(heap, child):
                return False
    return True


def assert_heap(test, heap):
    for i in range(1, len(heap)):
        test.assertLessEqual(heap[(i - 1) // 2], heap[i])


class SiftUp(unittest.TestCase):
    def test_single_and_equal_parent(self):
        heap = [4]
        self.assertIsNone(practice.sift_up(heap, 0))
        self.assertEqual(heap, [4])
        heap = [4, 4]
        practice.sift_up(heap, 1)
        self.assertEqual(heap, [4, 4])

    def test_multiple_swaps_and_technique(self):
        heap = [2, 7, 5, 1]
        practice.sift_up(heap, 3)
        self.assertEqual(heap, [1, 2, 5, 7])
        check_manual(self, practice.sift_up)

    def test_stops_midway_after_append(self):
        heap = [1, 4, 3, 8, 6, 2]
        practice.sift_up(heap, 5)
        self.assertEqual(heap, [1, 4, 2, 8, 6, 3])
        heap = [1, 4, 3, 8, 6, 5]
        practice.sift_up(heap, 5)
        self.assertEqual(heap, [1, 4, 3, 8, 6, 5])


class Push(unittest.TestCase):
    def test_empty_and_duplicate(self):
        heap = []
        self.assertIsNone(practice.push(heap, 4, sift_up))
        practice.push(heap, 4, sift_up)
        self.assertEqual(heap, [4, 4])

    def test_root_move_and_technique(self):
        heap = [5, 7, 8]
        practice.push(heap, 3, sift_up)
        self.assertEqual(heap, [3, 5, 8, 7])
        check_manual(self, practice.push)

    def test_uses_given_sift_up(self):
        calls = []

        def spy(heap, i):
            calls.append((id(heap), i, list(heap)))

        heap = [5, 7, 8]
        practice.push(heap, 3, spy)
        self.assertEqual(calls, [(id(heap), 3, [5, 7, 8, 3])])
        self.assertEqual(heap, [5, 7, 8, 3])


class SiftDown(unittest.TestCase):
    def test_one_and_left_child_only(self):
        heap = [3]
        self.assertIsNone(practice.sift_down(heap, 0))
        self.assertEqual(heap, [3])
        heap = [3, -1]
        practice.sift_down(heap, 0)
        self.assertEqual(heap, [-1, 3])

    def test_right_child_and_multiple_swaps(self):
        heap = [10, 6, 3, 7, 9, 4]
        practice.sift_down(heap, 0)
        self.assertEqual(heap, [3, 6, 4, 7, 9, 10])
        check_manual(self, practice.sift_down)

    def test_long_path_and_right_child(self):
        heap = [20, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
        practice.sift_down(heap, 0)
        self.assertEqual(heap, [3, 5, 4, 9, 6, 7, 8, 20, 10, 11, 12, 13, 14, 15, 16])
        heap = [1, 5, 7, 4, 2, 6, 3, 99]
        practice.sift_down(heap, 2)
        self.assertEqual(heap, [1, 5, 3, 4, 2, 6, 7, 99])

    def test_subtree(self):
        heap = [1, 9, 3, 5, 5, 8]
        practice.sift_down(heap, 1)
        self.assertEqual(heap[0:3:2], [1, 3])
        self.assertCountEqual(heap, [1, 9, 3, 5, 5, 8])
        assert_heap(self, heap)


class PopMin(unittest.TestCase):
    def test_empty_and_one(self):
        heap = []
        self.assertIsNone(practice.pop_min(heap, sift_down))
        heap.append(1)
        self.assertEqual(practice.pop_min(heap, sift_down), 1)
        self.assertEqual(heap, [])

    def test_repeated_pops_and_technique(self):
        heap = [1, 2, 1, 5, 3, 4]
        for key in [1, 1, 2, 3, 4, 5]:
            self.assertEqual(practice.pop_min(heap, sift_down), key)
            assert_heap(self, heap)
        self.assertEqual(heap, [])
        check_manual(self, practice.pop_min)

    def test_uses_given_sift_down(self):
        calls = []

        def spy(heap, i):
            calls.append((id(heap), i))
            sift_down(heap, i)

        heap = [2, 3, 4, 7]
        self.assertEqual(practice.pop_min(heap, spy), 2)
        self.assertEqual(calls, [(id(heap), 0)])
        assert_heap(self, heap)
        self.assertCountEqual(heap, [3, 4, 7])


class Heapify(unittest.TestCase):
    def test_empty_and_one(self):
        heap = []
        self.assertIsNone(practice.heapify(heap, sift_down))
        self.assertEqual(heap, [])
        heap = [1]
        practice.heapify(heap, sift_down)
        self.assertEqual(heap, [1])

    def test_heap_order_and_elements(self):
        heap = [9, 7, 2, 6, 1, 1, 0, -3, 8]
        original = heap.copy()
        repaired = []
        original_heap = heap

        def tracked_sift(heap, i):
            self.assertIs(heap, original_heap)
            self.assertGreaterEqual(i, 0)
            self.assertLess(i, len(heap) // 2)
            for child in (2 * i + 1, 2 * i + 2):
                self.assertTrue(is_heap_at(heap, child), "Repair children before their parent.")
            repaired.append(i)
            sift_down(heap, i)

        practice.heapify(heap, tracked_sift)
        self.assertEqual(len(repaired), len(heap) // 2)
        self.assertCountEqual(repaired, range(len(heap) // 2))
        self.assertCountEqual(heap, original)
        assert_heap(self, heap)
        check_manual(self, practice.heapify)

    def test_children_are_repaired_before_parents(self):
        heap = [9, 7, 8, 6, 5, -10, 4, -3, 8]
        original = heap.copy()

        def ordered_sift(heap, i):
            for child in (2 * i + 1, 2 * i + 2):
                self.assertTrue(is_heap_at(heap, child), "Repair children before their parent.")
            sift_down(heap, i)

        practice.heapify(heap, ordered_sift)
        assert_heap(self, heap)
        self.assertEqual(heap[0], -10)
        self.assertCountEqual(heap, original)


class Schedule(unittest.TestCase):
    def test_empty_and_one(self):
        self.assertEqual(practice.schedule([]), [])
        self.assertEqual(practice.schedule([(2, "log")]), ["log"])

    def test_priorities_ties_and_read_only(self):
        jobs = [(3, "report"), (0, "z-check"), (0, "a-check"), (-1, "alert"), (3, "report")]
        snapshot = jobs.copy()
        self.assertEqual(practice.schedule(jobs), ["alert", "z-check", "a-check", "report", "report"])
        self.assertEqual(jobs, snapshot)

    def test_uses_heapq_push_and_pop(self):
        import heapq
        import importlib

        counts = {"push": 0, "pop": 0, "heapify": 0}
        real = (heapq.heappush, heapq.heappop, heapq.heapify)

        def push(heap, item):
            counts["push"] += 1
            real[0](heap, item)

        def pop(heap):
            counts["pop"] += 1
            return real[1](heap)

        def build(heap):
            counts["heapify"] += 1
            real[2](heap)

        heapq.heappush, heapq.heappop, heapq.heapify = push, pop, build
        try:
            module = importlib.reload(practice)
            jobs = [(2, "log"), (1, "alert"), (2, "sync"), (0, "page")]
            self.assertEqual(module.schedule(jobs), ["page", "alert", "log", "sync"])
        finally:
            heapq.heappush, heapq.heappop, heapq.heapify = real
            importlib.reload(practice)
        self.assertGreaterEqual(counts["pop"], 4)
        self.assertGreater(counts["push"] + counts["heapify"], 0)
