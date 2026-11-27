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


def check_manual(test, function):
    source = ast.parse(inspect.getsource(practice))
    for item in source.body:
        if isinstance(item, ast.FunctionDef) and item.name != function.__name__:
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
            repaired.append(i)
            sift_down(heap, i)

        practice.heapify(heap, tracked_sift)
        self.assertEqual(len(repaired), len(heap) // 2)
        self.assertCountEqual(repaired, range(len(heap) // 2))
        self.assertCountEqual(heap, original)
        assert_heap(self, heap)
        check_manual(self, practice.heapify)


class Schedule(unittest.TestCase):
    def test_empty_and_one(self):
        self.assertEqual(practice.schedule([]), [])
        self.assertEqual(practice.schedule([(2, "log")]), ["log"])

    def test_priorities_ties_and_read_only(self):
        jobs = [(3, "report"), (0, "z-check"), (0, "a-check"), (-1, "alert"), (3, "report")]
        snapshot = jobs.copy()
        self.assertEqual(practice.schedule(jobs), ["alert", "z-check", "a-check", "report", "report"])
        self.assertEqual(jobs, snapshot)
