import ast
import inspect
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "exercises"))
import practice


def nodes(function):
    return ast.walk(ast.parse(inspect.getsource(function)))


class HalveRounds(unittest.TestCase):
    def test_contract(self):
        function = practice.halve_rounds
        for n, count in ((0, 0), (1, 0), (2, 1), (12, 3), (1024, 10), (1_000_000, 19)):
            self.assertEqual(function(n), count)
        loops = [node for node in nodes(function) if isinstance(node, ast.While)]
        self.assertTrue(loops, "Use a while loop.")
        self.assertTrue(any(isinstance(node, ast.FloorDiv) for node in ast.walk(loops[0])),
                        "Use whole-number division inside the loop.")


class PlannedVisits(unittest.TestCase):
    def test_contract(self):
        function = practice.planned_visits
        for n in (0, 1, 3, 8, 16, 1_000_000):
            self.assertEqual(function(n), n * max(0, n.bit_length() - 1))
        loops = (ast.For, ast.AsyncFor, ast.While, ast.comprehension)
        self.assertEqual([type(node) for node in nodes(function) if isinstance(node, loops)], [ast.While])


class FirstOverBudget(unittest.TestCase):
    def test_contract(self):
        function = practice.first_over_budget
        for budget, n in ((0, 1), (1, 2), (3, 2), (4, 4), (15, 4), (16, 8), (10_000, 128)):
            self.assertEqual(function(budget), n)
        self.assertTrue(any(isinstance(node, ast.While) for node in nodes(function)), "Use a while loop.")
