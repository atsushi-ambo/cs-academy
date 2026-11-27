import importlib.util
import os
import pathlib
import unittest

UNIT_DIR = pathlib.Path(__file__).resolve().parent.parent
TARGET = os.environ.get("CS_ACADEMY_TARGET", "exercises")
if TARGET not in {"exercises", "solutions"}:
    raise SystemExit("CS_ACADEMY_TARGET must be 'exercises' or 'solutions'")

_spec = importlib.util.spec_from_file_location(
    "lists_practice", UNIT_DIR / TARGET / "lists_practice.py"
)
m = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(m)


class LastAndFirst(unittest.TestCase):
    def test_normal(self):
        self.assertEqual(m.last_and_first(["a", "b", "c"]), ["c", "a"])

    def test_single_item(self):
        self.assertEqual(m.last_and_first(["only"]), ["only", "only"])

    def test_empty(self):
        self.assertEqual(m.last_and_first([]), [])

    def test_returns_new_list(self):
        items = ["x", "y"]
        result = m.last_and_first(items)
        self.assertIsInstance(result, list)
        self.assertIsNot(result, items)

    def test_does_not_change_input(self):
        items = [1, 2, 3]
        m.last_and_first(items)
        self.assertEqual(items, [1, 2, 3])


class SlowServers(unittest.TestCase):
    def test_keeps_order(self):
        self.assertEqual(
            m.slow_servers(["web01", "web02", "db01", "cache01"], [120, 950, 80, 1500], 500),
            ["web02", "cache01"],
        )

    def test_limit_is_not_slow(self):
        self.assertEqual(m.slow_servers(["a", "b"], [500, 501], 500), ["b"])

    def test_none_slow(self):
        self.assertEqual(m.slow_servers(["a"], [10], 500), [])

    def test_empty(self):
        self.assertEqual(m.slow_servers([], [], 500), [])

    def test_length_mismatch(self):
        with self.assertRaises(ValueError):
            m.slow_servers(["a", "b"], [1], 500)
        with self.assertRaises(ValueError):
            m.slow_servers(["a"], [1, 2], 500)

    def test_does_not_change_input(self):
        servers, times = ["a", "b"], [900, 100]
        m.slow_servers(servers, times, 500)
        self.assertEqual((servers, times), (["a", "b"], [900, 100]))

    def test_returns_list(self):
        self.assertIsInstance(m.slow_servers(["a"], [900], 500), list)


class WithoutDuplicates(unittest.TestCase):
    def test_keeps_first_occurrence(self):
        self.assertEqual(
            m.without_duplicates(["web01", "db01", "web01", "cache01", "db01"]),
            ["web01", "db01", "cache01"],
        )

    def test_does_not_change_input(self):
        items = [3, 3, 1]
        result = m.without_duplicates(items)
        self.assertEqual(items, [3, 3, 1])
        self.assertIsNot(result, items)

    def test_empty(self):
        self.assertEqual(m.without_duplicates([]), [])

    def test_numbers(self):
        self.assertEqual(m.without_duplicates([2, 2, 2]), [2])


class MovingWindowMax(unittest.TestCase):
    def test_example(self):
        self.assertEqual(m.moving_window_max([3, 1, 4, 1, 5, 9, 2], 3), [4, 4, 5, 9, 9])

    def test_window_equals_length(self):
        self.assertEqual(m.moving_window_max([2, 7, 1], 3), [7])

    def test_window_of_one(self):
        self.assertEqual(m.moving_window_max([2, 7, 1], 1), [2, 7, 1])

    def test_negative_values_and_ties(self):
        self.assertEqual(m.moving_window_max([-5, -1, -3], 2), [-1, -1])
        self.assertEqual(m.moving_window_max([4, 4, 4], 2), [4, 4])

    def test_does_not_change_input(self):
        values = [3, 1, 2]
        m.moving_window_max(values, 2)
        self.assertEqual(values, [3, 1, 2])

    def test_invalid_sizes(self):
        self.assertEqual(m.moving_window_max([1, 2], -1), [])
        self.assertEqual(m.moving_window_max([1, 2], 0), [])
        self.assertEqual(m.moving_window_max([1, 2], 3), [])
        self.assertEqual(m.moving_window_max([], 1), [])


if __name__ == "__main__":
    unittest.main()
