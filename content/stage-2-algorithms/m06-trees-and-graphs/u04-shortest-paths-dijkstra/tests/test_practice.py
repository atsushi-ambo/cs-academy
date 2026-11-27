import heapq
import sys
import unittest
from copy import deepcopy
from pathlib import Path

HEAP_CALLS = {'push': 0, 'pop': 0}
_real_push, _real_pop = heapq.heappush, heapq.heappop


def _counting_push(heap, item):
    HEAP_CALLS['push'] += 1
    return _real_push(heap, item)


def _counting_pop(heap):
    HEAP_CALLS['pop'] += 1
    return _real_pop(heap)


heapq.heappush, heapq.heappop = _counting_push, _counting_pop

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'exercises'))
import practice


class ReadCounter(list):
    reads = None

    def __iter__(self):
        ReadCounter.reads[self.owner] = ReadCounter.reads.get(self.owner, 0) + 1
        return super().__iter__()


def watched(graph):
    ReadCounter.reads = {}
    wrapped = {}
    for node, edges in graph.items():
        reader = ReadCounter(edges)
        reader.owner = node
        wrapped[node] = reader
    return wrapped


def heap_calls_during(call):
    HEAP_CALLS['push'] = HEAP_CALLS['pop'] = 0
    result = call()
    return result, dict(HEAP_CALLS)


STALE_GRAPH = {'a': [('b', 12), ('c', 2)], 'c': [('b', 5)], 'b': [('d', 1)], 'd': [], 'e': []}


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
        result, calls = heap_calls_during(lambda: practice.latencies(STALE_GRAPH, 'a'))
        self.assertEqual(result, {'a': 0, 'c': 2, 'b': 7, 'd': 8})
        self.assertGreaterEqual(calls['push'], 3, 'Use heappush to keep the frontier.')
        self.assertGreaterEqual(calls['pop'], 3, 'Use heappop to take the cheapest candidate.')

    def test_stale_entries_are_not_expanded_again(self):
        graph = watched(STALE_GRAPH)
        self.assertEqual(practice.latencies(graph, 'a'), {'a': 0, 'c': 2, 'b': 7, 'd': 8})
        for node, count in ReadCounter.reads.items():
            self.assertEqual(count, 1, 'Skip old heap entries: %r was expanded %d times.' % (node, count))

    def test_larger_grid_is_correct(self):
        size = 12
        graph = {(r, c): [] for r in range(size) for c in range(size)}
        for r in range(size):
            for c in range(size):
                for dr, dc in ((1, 0), (0, 1), (-1, 0), (0, -1)):
                    if (r + dr, c + dc) in graph:
                        graph[(r, c)].append(((r + dr, c + dc), 1 + (r * 7 + c * 3 + dr) % 5))
        expected = {(0, 0): 0}
        queue = [(0, (0, 0))]
        while queue:
            cost, node = _real_pop(queue)
            if cost != expected[node]:
                continue
            for nxt, weight in graph[node]:
                if nxt not in expected or cost + weight < expected[nxt]:
                    expected[nxt] = cost + weight
                    _real_push(queue, (cost + weight, nxt))
        graph = watched(graph)
        self.assertEqual(practice.latencies(graph, (0, 0)), expected)
        self.assertTrue(all(count == 1 for count in ReadCounter.reads.values()))


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
        graph = {'a': [('b', 12), ('c', 2)], 'c': [('b', 5)], 'b': [('d', 1)], 'd': [], 'e': []}
        result, calls = heap_calls_during(lambda: practice.lowest_latency(graph, 'a', 'd'))
        self.assertEqual(result, (8, ['a', 'c', 'b', 'd']))
        self.assertGreaterEqual(calls['push'], 3, 'Use heappush to keep the frontier.')
        self.assertGreaterEqual(calls['pop'], 3, 'Use heappop to take the cheapest candidate.')

    def test_stale_entries_are_not_expanded_again(self):
        graph = watched(STALE_GRAPH)
        self.assertEqual(practice.lowest_latency(graph, 'a', 'e'), (None, []))
        for node, count in ReadCounter.reads.items():
            self.assertEqual(count, 1, 'Skip old heap entries: %r was expanded %d times.' % (node, count))


if __name__ == "__main__":
    unittest.main()
