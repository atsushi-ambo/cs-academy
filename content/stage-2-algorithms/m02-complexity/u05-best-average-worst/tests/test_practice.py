import ast
import inspect
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "exercises"))
import practice


class Compared:
    def __init__(self, value, reads):
        self.value = value
        self.reads = reads

    def __eq__(self, other):
        self.reads.append(self.value)
        return self.value == other


class ChecksUntilMatch(unittest.TestCase):
    def test_contract(self):
        function = practice.checks_until_match
        self.assertEqual(function([], 9), 0)
        self.assertEqual(function([3, 8, 3], 8), 2)
        self.assertEqual(function([3, 8, 3], 3), 1)
        self.assertEqual(function([3, 8, 3], 9), 3)
        for target, count in ((1, 1), (2, 200), (3, 200)):
            reads = []
            values = [Compared(1, reads)] * 199 + [Compared(2, reads)]
            original = values[:]
            self.assertEqual(function(values, target), count)
            self.assertEqual(len(reads), count, "Stop comparing at the first match.")
            self.assertEqual([id(value) for value in values], [id(value) for value in original])


class UniformHitCost(unittest.TestCase):
    def test_contract(self):
        function = practice.uniform_hit_cost
        for n, cost in ((1, 1), (2, 1.5), (4, 2.5), (5, 3), (1_000_000, 500000.5)):
            self.assertEqual(function(n), cost)
        nodes = ast.walk(ast.parse(inspect.getsource(function)))
        self.assertFalse(any(isinstance(node, (ast.For, ast.While, ast.comprehension,
                                             ast.List, ast.Set, ast.Dict)) for node in nodes))


class BatchChecks(unittest.TestCase):
    def test_contract(self):
        function = practice.batch_checks
        self.assertEqual(function([3, 8, 4], []), 0)
        self.assertEqual(function([], [3, 8]), 0)
        codes, targets = [3, 8, 4], [3, 9, 8]
        self.assertEqual(function(codes, targets), 6)
        self.assertEqual((codes, targets), ([3, 8, 4], [3, 9, 8]))
        reads = []
        tracked = [Compared(code, reads) for code in codes]
        self.assertEqual(function(tracked, targets), 6)
        self.assertEqual(reads, [3, 3, 8, 4, 3, 8])
