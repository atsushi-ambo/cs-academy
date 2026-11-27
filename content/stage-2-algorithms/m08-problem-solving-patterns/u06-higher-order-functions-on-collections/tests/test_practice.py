import ast
import inspect
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'exercises'))
import practice


class MyMap(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(practice.my_map(str, []), [])

    def test_one(self):
        self.assertEqual(practice.my_map(str, (5,)), ['5'])

    def test_order_and_calls(self):
        items = [3, 3, 2]
        seen = []
        def rule(n):
            seen.append(n)
            return n * 2
        self.assertEqual(practice.my_map(rule, items), [6, 6, 4])
        self.assertEqual(seen, items)
        self.assertEqual(items, [3, 3, 2])

    def test_iterator_and_technique(self):
        self.assertEqual(practice.my_map(str, iter([3, 4])), ['3', '4'])
        tree = ast.parse(inspect.getsource(practice.my_map))
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                name = getattr(node.func, 'id', getattr(node.func, 'attr', None))
                self.assertNotEqual(name, 'map', 'Implement map behavior yourself.')
            if isinstance(node, ast.ImportFrom) and node.module in ('builtins', 'functools'):
                self.assertNotIn('map', [alias.name for alias in node.names])


class MyFilter(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(practice.my_filter(bool, []), [])

    def test_one(self):
        self.assertEqual(practice.my_filter(bool, ('x',)), ['x'])

    def test_calls_and_duplicates(self):
        items, calls = [2, 3, 3, 0], []
        def keep(n):
            calls.append(n)
            return n % 2
        self.assertEqual(practice.my_filter(keep, items), [3, 3])
        self.assertEqual(calls, [2, 3, 3, 0])
        self.assertEqual(items, [2, 3, 3, 0])

    def test_iterator_and_technique(self):
        self.assertEqual(practice.my_filter(bool, iter([0, 2])), [2])
        tree = ast.parse(inspect.getsource(practice.my_filter))
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                name = getattr(node.func, 'id', getattr(node.func, 'attr', None))
                self.assertNotEqual(name, 'filter', 'Implement filter behavior yourself.')
            if isinstance(node, ast.ImportFrom) and node.module in ('builtins', 'functools'):
                self.assertNotIn('filter', [alias.name for alias in node.names])


class MyReduce(unittest.TestCase):
    def test_empty(self):
        initial = []
        self.assertIs(practice.my_reduce(lambda a, n: a + n, [], initial), initial)

    def test_one(self):
        self.assertEqual(practice.my_reduce(lambda a, n: a - n, (3,), 2), -1)

    def test_calls_and_order(self):
        items, calls = [2, 2, 3], []
        def combine(a, n):
            calls.append((a, n))
            return a * 10 + n
        self.assertEqual(practice.my_reduce(combine, items, 1), 1223)
        self.assertEqual(calls, [(1, 2), (12, 2), (122, 3)])
        self.assertEqual(items, [2, 2, 3])

    def test_iterator_and_technique(self):
        self.assertEqual(practice.my_reduce(lambda a, n: a - n, iter([2, 3]), 10), 5)
        tree = ast.parse(inspect.getsource(practice.my_reduce))
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                name = getattr(node.func, 'id', getattr(node.func, 'attr', None))
                self.assertNotEqual(name, 'reduce', 'Implement reduce behavior yourself.')
            if isinstance(node, ast.ImportFrom) and node.module in ('builtins', 'functools'):
                self.assertNotIn('reduce', [alias.name for alias in node.names])


class IncidentReport(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(practice.incident_report([]), (0, []))

    def test_one(self):
        self.assertEqual(practice.incident_report([('api', 500, 3)]), (3, [('api', 500, 3)]))

    def test_no_errors(self):
        self.assertEqual(practice.incident_report([('api', 499, 3), ('db', 600, 6)]), (0, []))

    def test_boundaries_and_ties(self):
        logs = [('web', 500, 4), ('db', 599, 4), ('api', 499, 10),
                ('db', 501, 4), ('db', 599, 4), ('api', 502, 8), ('x', 600, 20)]
        original = logs[:]
        self.assertEqual(practice.incident_report(logs),
                         (24, [('api', 502, 8), ('db', 599, 4), ('db', 501, 4),
                               ('db', 599, 4), ('web', 500, 4)]))
        self.assertEqual(logs, original)


if __name__ == "__main__":
    unittest.main()
