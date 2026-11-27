import sys
import unittest
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'exercises'))
import practice


class WatchedGraph(dict):
    """A graph that records which vertices are looked up and stops runaway searches."""

    def __init__(self, graph, limit):
        super().__init__(graph)
        self.order = []
        self.lookups = 0
        self.limit = limit

    def _note(self, node):
        self.lookups += 1
        if self.lookups > self.limit:
            raise AssertionError('Too many neighbor lookups: visit each vertex only once.')
        if node not in self.order:
            self.order.append(node)

    def __getitem__(self, node):
        self._note(node)
        return super().__getitem__(node)

    def get(self, node, default=None):
        self._note(node)
        return super().get(node, default)


def dense_cycle_graph(size):
    return {i: [(i + 1) % size, (i + 2) % size, (i + 3) % size, i] for i in range(size)}


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

    def test_each_vertex_expanded_once_and_levels_are_correct(self):
        size = 300
        graph = WatchedGraph(dense_cycle_graph(size), 2 * size)
        counts = practice.hop_counts(graph, 0)
        self.assertEqual(counts[0], 0)
        self.assertEqual(len(counts), size)
        self.assertEqual(counts[size - 1], (size - 1 + 2) // 3)
        self.assertEqual(max(counts.values()), (size - 1 + 2) // 3)

    def test_layer_by_layer(self):
        graph = WatchedGraph({'a': ['b', 'c'], 'b': ['d'], 'c': ['e'], 'd': ['f'], 'e': [], 'f': []}, 20)
        self.assertEqual(practice.hop_counts(graph, 'a'), {'a': 0, 'b': 1, 'c': 1, 'd': 2, 'e': 2, 'f': 3})
        self.assertEqual(graph.order[:3], ['a', 'b', 'c'])
        self.assertEqual(set(graph.order[3:5]), {'d', 'e'})


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

    def test_finishes_one_branch_before_the_other(self):
        tree = {'a': ['b', 'c'], 'b': ['d', 'e'], 'c': ['f'], 'd': [], 'e': [], 'f': []}
        graph = WatchedGraph(tree, 20)
        self.assertEqual(practice.stack_reachable(graph, 'a'), set(tree))
        rest = graph.order[1:]
        in_b_first = set(rest[:3]) == {'b', 'd', 'e'} and set(rest[3:]) == {'c', 'f'}
        in_c_first = set(rest[:2]) == {'c', 'f'} and set(rest[2:]) == {'b', 'd', 'e'}
        self.assertTrue(in_b_first or in_c_first, 'Take the newest vertex from the stack: %r' % graph.order)

    def test_each_vertex_expanded_once(self):
        size = 400
        graph = WatchedGraph(dense_cycle_graph(size), 2 * size)
        self.assertEqual(practice.stack_reachable(graph, 0), set(range(size)))


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

    def test_many_vertices_each_expanded_once(self):
        size = 200
        graph = {}
        for group in range(5):
            members = [group * size + i for i in range(size)]
            for index, node in enumerate(members):
                graph[node] = [members[(index + 1) % size], members[(index - 1) % size], node]
        watched = WatchedGraph(graph, 2 * len(graph))
        self.assertEqual(practice.component_count(watched), 5)


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

    def test_wide_tall_and_ragged_shapes(self):
        self.assertEqual(practice.flood_size([[1, 1, 1]], 0, 0), 3)
        self.assertEqual(practice.flood_size([[1], [1], [1]], 0, 0), 3)
        self.assertEqual(practice.flood_size([[1, 1, 1, 1], [0, 0, 0, 1]], 0, 0), 5)
        self.assertEqual(practice.flood_size([[1, 0], [1, 0], [1, 1], [0, 1]], 3, 1), 5)
        self.assertEqual(practice.flood_size([[1, 1, 1]], 0, 3), 0)
        self.assertEqual(practice.flood_size([[1], [1]], 2, 0), 0)

    def test_large_open_grid(self):
        grid = [[1] * 60 for _ in range(60)]
        self.assertEqual(practice.flood_size(grid, 30, 30), 3600)


if __name__ == "__main__":
    unittest.main()
