import ast
import inspect
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'exercises'))
import practice


class FibMisses(unittest.TestCase):
    def test_zero(self):
        self.assertEqual(practice.fib_misses(0), (0, 1))

    def test_one(self):
        self.assertEqual(practice.fib_misses(1), (1, 1))

    def test_shared_subproblems(self):
        self.assertEqual(practice.fib_misses(40), (102334155, 41))

    def test_fresh_across_calls(self):
        self.assertEqual(practice.fib_misses(5), (5, 6))
        self.assertEqual(practice.fib_misses(5), (5, 6))
        self.assertEqual(practice.fib_misses(2), (1, 3))

    def test_recursive(self):
        self.assertEqual(practice.fib_misses(5), (5, 6))
        tree = ast.parse(inspect.getsource(practice.fib_misses))
        self.assertTrue(any(
            isinstance(node, ast.FunctionDef) and any(
                isinstance(call, ast.Call) and isinstance(call.func, ast.Name)
                and call.func.id == node.name for call in ast.walk(node)
            ) for node in ast.walk(tree)
        ), 'Use a recursive call to compute a smaller state.')


class StairWays(unittest.TestCase):
    def test_zero(self):
        self.assertEqual(practice.stair_ways(0), 1)

    def test_one(self):
        self.assertEqual(practice.stair_ways(1), 1)

    def test_larger_and_repeat(self):
        self.assertEqual(practice.stair_ways(35), 14930352)
        self.assertEqual(practice.stair_ways(4), 5)
        self.assertEqual(practice.stair_ways(35), 14930352)

    def test_cached_recursion(self):
        self.assertEqual(practice.stair_ways(3), 3)
        tree = ast.parse(inspect.getsource(practice.stair_ways))
        self.assertTrue(any(
            isinstance(node, ast.FunctionDef) and any(
                isinstance(call, ast.Call) and isinstance(call.func, ast.Name)
                and call.func.id == node.name for call in ast.walk(node)
            ) for node in ast.walk(tree)
        ), 'Use a recursive call to compute a smaller state.')
        self.assertTrue(any(
            isinstance(node, ast.ImportFrom) and node.module == 'functools'
            and any(alias.name == 'lru_cache' for alias in node.names)
            or isinstance(node, ast.Attribute) and node.attr == 'lru_cache'
            for node in ast.walk(tree)
        ), 'Use functools.lru_cache to store stair counts.')


class CoinWays(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(practice.coin_ways([], 0), 1)

    def test_no_coins(self):
        self.assertEqual(practice.coin_ways([], 3), 0)

    def test_one(self):
        self.assertEqual(practice.coin_ways([3], 9), 1)

    def test_impossible(self):
        self.assertEqual(practice.coin_ways([4, 6], 5), 0)

    def test_duplicate_denominations_and_order(self):
        coins = [3, 1, 3]
        self.assertEqual(practice.coin_ways(coins, 4), 2)
        self.assertEqual(coins, [3, 1, 3])

    def test_counts_each_combination_once(self):
        self.assertEqual(practice.coin_ways([1, 2, 5], 10), 10)

    def test_recursive(self):
        self.assertEqual(practice.coin_ways([1], 2), 1)
        tree = ast.parse(inspect.getsource(practice.coin_ways))
        self.assertTrue(any(
            isinstance(node, ast.FunctionDef) and any(
                isinstance(call, ast.Call) and isinstance(call.func, ast.Name)
                and call.func.id == node.name for call in ast.walk(node)
            ) for node in ast.walk(tree)
        ), 'Use a recursive call to compute a smaller state.')


if __name__ == "__main__":
    unittest.main()
