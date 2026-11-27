import ast
import inspect
import sys
import unittest
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'exercises'))
import practice


class Latencies(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(practice.latencies({}, 'api'), {})

    def test_single(self):
        self.assertEqual(practice.latencies({'api': [('api', 0)]}, 'api'), {'api': 0})

    def test_weighted_shortcut_and_duplicates(self):
        graph = {'a': [('b', 12), ('b', 12), ('c', 3)],
                 'b': [('d', 0)], 'c': [('b', 4)], 'd': [('a', 1)], 'z': []}
        original = deepcopy(graph)
        self.assertEqual(practice.latencies(graph, 'a'), {'a': 0, 'c': 3, 'b': 7, 'd': 7})
        self.assertEqual(graph, original)

    def test_uses_heap(self):
        self.assertEqual(practice.latencies({'a': []}, 'a'), {'a': 0})
        tree = ast.parse(inspect.getsource(practice.latencies))
        imports = [node for node in ast.walk(tree) if isinstance(node, (ast.Import, ast.ImportFrom))]
        operations = set()
        for node in imports:
            if isinstance(node, ast.ImportFrom) and node.module == 'heapq':
                operations.update(name.name for name in node.names)
            if isinstance(node, ast.Import):
                for name in node.names:
                    if name.name == 'heapq':
                        alias = name.asname or name.name
                        operations.update(attr.attr for attr in ast.walk(tree)
                                          if isinstance(attr, ast.Attribute)
                                          and isinstance(attr.value, ast.Name) and attr.value.id == alias)
        self.assertTrue({'heappop', 'heappush'} <= operations, 'Use heapq to maintain the frontier.')


class TraceRoute(unittest.TestCase):
    def test_missing(self):
        self.assertEqual(practice.trace_route({}, 'a', 'b'), [])

    def test_one(self):
        self.assertEqual(practice.trace_route({}, 'a', 'a'), ['a'])

    def test_branches(self):
        parent = {'d': 'c', 'b': 'a', 'c': 'a'}
        self.assertEqual(practice.trace_route(parent, 'a', 'd'), ['a', 'c', 'd'])
        self.assertEqual(parent, {'d': 'c', 'b': 'a', 'c': 'a'})


class LowestLatency(unittest.TestCase):
    def test_empty_or_unreachable(self):
        self.assertEqual(practice.lowest_latency({}, 'a', 'b'), (None, []))
        self.assertEqual(practice.lowest_latency({'a': [], 'b': []}, 'a', 'b'), (None, []))

    def test_start_is_target(self):
        self.assertEqual(practice.lowest_latency({'a': []}, 'a', 'a'), (0, ['a']))

    def test_updates_route(self):
        graph = {'a': [('b', 12), ('c', 2), ('c', 2)], 'b': [], 'c': [('b', 3), ('a', 0)]}
        original = deepcopy(graph)
        self.assertEqual(practice.lowest_latency(graph, 'a', 'b'), (5, ['a', 'c', 'b']))
        self.assertEqual(graph, original)

    def test_allows_ties(self):
        graph = {'a': [('b', 0), ('c', 0)], 'b': [('d', 1)], 'c': [('d', 1)], 'd': []}
        self.assertIn(practice.lowest_latency(graph, 'a', 'd'),
                      [(1, ['a', 'b', 'd']), (1, ['a', 'c', 'd'])])

    def test_uses_heap(self):
        self.assertEqual(practice.lowest_latency({'a': []}, 'a', 'a'), (0, ['a']))
        tree = ast.parse(inspect.getsource(practice.lowest_latency))
        imports = [node for node in ast.walk(tree) if isinstance(node, (ast.Import, ast.ImportFrom))]
        operations = set()
        for node in imports:
            if isinstance(node, ast.ImportFrom) and node.module == 'heapq':
                operations.update(name.name for name in node.names)
            if isinstance(node, ast.Import):
                for name in node.names:
                    if name.name == 'heapq':
                        alias = name.asname or name.name
                        operations.update(attr.attr for attr in ast.walk(tree)
                                          if isinstance(attr, ast.Attribute)
                                          and isinstance(attr.value, ast.Name) and attr.value.id == alias)
        self.assertTrue({'heappop', 'heappush'} <= operations, 'Use heapq to maintain the frontier.')


if __name__ == "__main__":
    unittest.main()
