import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'exercises'))
import practice


class ApplyEach(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(practice.apply_each([], lambda n: n), [])

    def test_one(self):
        self.assertEqual(practice.apply_each([3], str), ['3'])

    def test_order_and_calls(self):
        readings = [3, 3, 1]
        calls = []
        def rule(n):
            calls.append(n)
            return n + 2
        self.assertEqual(practice.apply_each(readings, rule), [5, 5, 3])
        self.assertEqual(calls, [3, 3, 1])
        self.assertEqual(readings, [3, 3, 1])


class Slowest(unittest.TestCase):
    def test_empty(self):
        self.assertIsNone(practice.slowest([]))

    def test_one(self):
        self.assertEqual(practice.slowest([('web', 0)]), ('web', 0))

    def test_first_tie(self):
        logs = [('api', 1), ('web', 9), ('db', 9), ('web', 9)]
        self.assertEqual(practice.slowest(logs), ('web', 9))
        self.assertEqual(logs, [('api', 1), ('web', 9), ('db', 9), ('web', 9)])


class IncidentOrder(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(practice.incident_order([]), [])

    def test_one(self):
        logs = [('db', 1, 0)]
        result = practice.incident_order(logs)
        self.assertEqual(result, logs)
        self.assertIsNot(result, logs)

    def test_all_three_keys(self):
        logs = [('web', 20, 1), ('db', 8, 3), ('db', 4, 0),
                ('db', 8, 1), ('db', 8, 1)]
        original = logs[:]
        self.assertEqual(practice.incident_order(logs),
                         [('db', 8, 1), ('db', 8, 1), ('db', 8, 3),
                          ('db', 4, 0), ('web', 20, 1)])
        self.assertEqual(logs, original)


if __name__ == "__main__":
    unittest.main()
