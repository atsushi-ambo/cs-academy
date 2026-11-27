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


class MemoizeCount(unittest.TestCase):
    def test_memo(self):
        calls = []

        def compute(key):
            calls.append(key)
            return {"": 0, "gone": None, "api": 4}[key]

        cached = practice.memoize_count(compute)
        second = practice.memoize_count(compute)
        self.assertEqual(calls, [])
        self.assertEqual(cached(""), 0)
        self.assertEqual(cached(""), 0)
        self.assertIsNone(cached("gone"))
        self.assertIsNone(cached("gone"))
        self.assertEqual(cached("api"), 4)
        self.assertEqual(calls, ["", "gone", "api"])
        self.assertEqual(second("api"), 4)
        self.assertEqual(calls, ["", "gone", "api", "api"])
        reject_shortcuts(self, practice.memoize_count, {"cache", "lru_cache"})


class MakeLru(unittest.TestCase):
    def assert_order(self, cache, keys):
        self.assertEqual(set(cache.nodes), set(keys))
        current = cache.head
        previous = None
        for key in keys:
            self.assertIs(current, cache.nodes[key])
            self.assertEqual(current.key, key)
            self.assertIs(current.prev, previous)
            previous = current
            current = current.next
        self.assertIsNone(current)
        self.assertIs(cache.tail, previous)

    def test_hits_updates_and_eviction(self):
        cache = practice.make_lru(2)
        self.assert_order(cache, [])
        self.assertIsNone(cache.get("api"))
        cache.put("api", 0)
        cache.put("db", 8)
        self.assert_order(cache, ["api", "db"])
        self.assertEqual(cache.get("api"), 0)
        self.assert_order(cache, ["db", "api"])
        self.assertIsNone(cache.get("web"))
        self.assert_order(cache, ["db", "api"])
        cache.put("web", 8)
        self.assert_order(cache, ["api", "web"])
        self.assertIsNone(cache.get("db"))
        cache.put("api", 9)
        self.assert_order(cache, ["web", "api"])
        cache.put("log", 3)
        self.assert_order(cache, ["api", "log"])
        self.assertEqual(cache.get("api"), 9)
        self.assert_order(cache, ["log", "api"])
        reject_shortcuts(self, practice.make_lru, {"OrderedDict", "deque", "lru_cache", "move_to_end"})

    def test_middle_node_moves_keep_links(self):
        cache = practice.make_lru(3)
        for key, value in (("a", 1), ("b", 2), ("c", 3)):
            cache.put(key, value)
        self.assertEqual(cache.get("b"), 2)
        self.assert_order(cache, ["a", "c", "b"])
        self.assertIs(cache.nodes["c"].prev, cache.nodes["a"])
        cache.put("c", 9)
        self.assert_order(cache, ["a", "b", "c"])
        cache.put("b", 7)
        self.assert_order(cache, ["a", "c", "b"])
        cache.put("d", 4)
        self.assert_order(cache, ["c", "b", "d"])
        self.assertEqual(cache.get("c"), 9)
        self.assert_order(cache, ["b", "d", "c"])
        self.assertEqual(cache.get("d"), 4)
        self.assert_order(cache, ["b", "c", "d"])
        self.assertEqual(cache.get("d"), 4)
        self.assert_order(cache, ["b", "c", "d"])

    def test_capacity_zero_and_one(self):
        zero = practice.make_lru(0)
        zero.put("api", 4)
        self.assertIsNone(zero.get("api"))
        self.assert_order(zero, [])
        one = practice.make_lru(1)
        one.put("api", 4)
        self.assertEqual(one.get("api"), 4)
        one.put("api", 8)
        one.put("db", 8)
        self.assertIsNone(one.get("api"))
        self.assert_order(one, ["db"])
        self.assertEqual(one.get("db"), 8)


class MakeOrderedLru(unittest.TestCase):
    def test_ordered_lru(self):
        cache = practice.make_ordered_lru(2)
        self.assertIsNone(cache.get("api"))
        cache.put("api", 0)
        cache.put("db", 4)
        self.assertEqual(cache.get("api"), 0)
        cache.put("web", 4)
        self.assertIsNone(cache.get("db"))
        cache.put("api", 5)
        cache.put("log", 4)
        self.assertIsNone(cache.get("web"))
        self.assertEqual(cache.get("api"), 5)

    def test_small_capacities(self):
        empty = practice.make_ordered_lru(0)
        empty.put("api", 4)
        self.assertIsNone(empty.get("api"))
        one = practice.make_ordered_lru(1)
        one.put("api", 4)
        one.put("api", 4)
        self.assertEqual(one.get("api"), 4)
        one.put("db", 4)
        self.assertIsNone(one.get("api"))
        self.assertEqual(one.get("db"), 4)


class BoundedCount(unittest.TestCase):
    def test_wrapped_function(self):
        calls = []

        def compute(key):
            calls.append(key)
            return {"api": 0, "db": 5, "web": None}[key]

        f = practice.bounded_count(compute, 2)
        self.assertEqual(calls, [])
        self.assertEqual([f(key) for key in ["api", "db", "api", "web", "web", "db"]], [0, 5, 0, None, None, 5])
        self.assertEqual(calls, ["api", "db", "web", "db"])
        self.assertEqual(f.cache_info().maxsize, 2)

    def test_zero_and_new_wrapper(self):
        calls = []

        def compute(key):
            calls.append(key)
            return len(key)

        disabled = practice.bounded_count(compute, 0)
        self.assertEqual([disabled(""), disabled("")], [0, 0])
        first = practice.bounded_count(compute, 1)
        second = practice.bounded_count(compute, 1)
        self.assertEqual([first("a"), first("a"), second("a")], [1, 1, 1])
        self.assertEqual(calls, ["", "", "a", "a"])
