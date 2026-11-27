import ast
import inspect
import sys
import unittest
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'exercises'))
import practice


class HopCounts(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(practice.hop_counts({}, 'a'), {})

    def test_isolated(self):
        self.assertEqual(practice.hop_counts({'a': []}, 'a'), {'a': 0})

    def test_short_route_cycle_and_duplicates(self):
        graph = {'a': ['b', 'd', 'd'], 'b': ['c'], 'c': ['d'], 'd': ['a'], 'z': []}
        original = deepcopy(graph)
        self.assertEqual(practice.hop_counts(graph, 'a'), {'a': 0, 'b': 1, 'd': 1, 'c': 2})
        self.assertEqual(graph, original)

    def test_unknown_in_nonempty(self):
        self.assertEqual(practice.hop_counts({'a': []}, 'z'), {})

    def test_implement_traversal(self):
        self.assertEqual(practice.hop_counts({'a': []}, 'a'), {'a': 0})
        tree = ast.parse(inspect.getsource(practice.hop_counts))
        imports = [node for node in ast.walk(tree) if isinstance(node, (ast.Import, ast.ImportFrom))]
        for node in imports:
            modules = [node.module or ''] if isinstance(node, ast.ImportFrom) else [name.name for name in node.names]
            self.assertTrue(all(module.split('.')[0] not in {'networkx', 'igraph', 'scipy', 'graphlib'}
                                for module in modules), 'Implement the graph algorithm yourself.')


class StackReachable(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(practice.stack_reachable({}, 'a'), set())

    def test_one(self):
        self.assertEqual(practice.stack_reachable({'a': ['a']}, 'a'), {'a'})

    def test_branch_then_cycle(self):
        graph = {'a': ['b', 'c', 'c'], 'b': [], 'c': ['a', 'd'], 'd': [], 'z': []}
        original = deepcopy(graph)
        self.assertEqual(practice.stack_reachable(graph, 'a'), {'a', 'b', 'c', 'd'})
        self.assertEqual(graph, original)

    def test_deep_without_recursion(self):
        graph = {i: [i + 1] for i in range(1600)}
        graph[1600] = []
        self.assertEqual(practice.stack_reachable(graph, 0), set(range(1601)))


class ComponentCount(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(practice.component_count({}), 0)

    def test_one(self):
        self.assertEqual(practice.component_count({'a': []}), 1)

    def test_more_than_one_group(self):
        graph = {'a': ['b', 'b'], 'z': [], 'b': ['a', 'a'], 'x': ['y'], 'y': ['x']}
        original = deepcopy(graph)
        self.assertEqual(practice.component_count(graph), 3)
        self.assertEqual(graph, original)


class FloodSize(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(practice.flood_size([], 0, 0), 0)

    def test_single(self):
        self.assertEqual(practice.flood_size([[1]], 0, 0), 1)

    def test_blocked_and_bounds(self):
        self.assertEqual(practice.flood_size([[0, 1]], 0, 0), 0)
        self.assertEqual(practice.flood_size([[1]], -1, 0), 0)
        self.assertEqual(practice.flood_size([[]], 0, 0), 0)

    def test_loop_and_diagonal(self):
        grid = [[1, 1, 0], [1, 1, 0], [0, 0, 1]]
        original = deepcopy(grid)
        self.assertEqual(practice.flood_size(grid, 0, 0), 4)
        self.assertEqual(practice.flood_size(grid, 2, 2), 1)
        self.assertEqual(grid, original)


if __name__ == "__main__":
    unittest.main()
