import ast
import inspect
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'exercises'))
import practice


class BagValue(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(practice.bag_value([], 5), 0)

    def test_single(self):
        self.assertEqual(practice.bag_value([(2, 5)], 4), 5)

    def test_zero_capacity(self):
        self.assertEqual(practice.bag_value([(1, 5)], 0), 0)

    def test_duplicate_items_are_separate(self):
        items = [(3, 5), (3, 5), (4, 9)]
        self.assertEqual(practice.bag_value(items, 6), 10)
        self.assertEqual(items, [(3, 5), (3, 5), (4, 9)])

    def test_combination_beats_largest_value(self):
        self.assertEqual(practice.bag_value([(2, 4), (3, 7), (4, 10)], 5), 11)
        tree = ast.parse(inspect.getsource(practice.bag_value))
        self.assertTrue(any(isinstance(node, (ast.For, ast.While, ast.comprehension))
                            for node in ast.walk(tree)), 'Fill the table with an iteration.')
        for fn in (node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)):
            self.assertFalse(any(isinstance(call, ast.Call) and isinstance(call.func, ast.Name)
                                 and call.func.id == fn.name for call in ast.walk(fn)),
                             'Use bottom-up iteration instead of recursive calls.')


class MinCoins(unittest.TestCase):
    def test_zero(self):
        self.assertEqual(practice.min_coins([], 0), 0)

    def test_no_coins(self):
        self.assertEqual(practice.min_coins([], 5), -1)

    def test_one(self):
        self.assertEqual(practice.min_coins([2], 6), 3)

    def test_unreachable(self):
        self.assertEqual(practice.min_coins([2], 5), -1)

    def test_duplicate_and_non_greedy(self):
        coins = [5, 1, 4, 4]
        self.assertEqual(practice.min_coins(coins, 8), 2)
        self.assertEqual(coins, [5, 1, 4, 4])


class LcsLength(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(practice.lcs_length('', 'ax'), 0)

    def test_one(self):
        self.assertEqual(practice.lcs_length('a', 'a'), 1)

    def test_order_and_case(self):
        self.assertEqual(practice.lcs_length('ab', 'ba'), 1)
        self.assertEqual(practice.lcs_length('A', 'a'), 0)

    def test_skip_letters_and_count_repeats(self):
        self.assertEqual(practice.lcs_length('axb', 'ayb'), 2)
        self.assertEqual(practice.lcs_length('aaba', 'abaa'), 3)
        tree = ast.parse(inspect.getsource(practice.lcs_length))
        self.assertTrue(any(isinstance(node, (ast.For, ast.While, ast.comprehension))
                            for node in ast.walk(tree)), 'Fill the table with an iteration.')
        for fn in (node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)):
            self.assertFalse(any(isinstance(call, ast.Call) and isinstance(call.func, ast.Name)
                                 and call.func.id == fn.name for call in ast.walk(fn)),
                             'Use bottom-up iteration instead of recursive calls.')


class BagChoices(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(practice.bag_choices([], 4), [])

    def test_one(self):
        self.assertEqual(practice.bag_choices([(2, 9)], 2), [0])

    def test_zero_capacity(self):
        self.assertEqual(practice.bag_choices([(1, 9)], 0), [])

    def test_several_and_unmodified(self):
        items = [(2, 4), (3, 7), (4, 10)]
        self.assertEqual(practice.bag_choices(items, 5), [0, 1])
        self.assertEqual(items, [(2, 4), (3, 7), (4, 10)])

    def test_tied_and_duplicate_items(self):
        items = [(2, 4), (2, 4), (3, 4)]
        self.assertIn(practice.bag_choices(items, 2), [[0], [1]])
        self.assertEqual(practice.bag_choices(items, 4), [0, 1])
        tree = ast.parse(inspect.getsource(practice.bag_choices))
        self.assertTrue(any(isinstance(node, (ast.For, ast.While, ast.comprehension))
                            for node in ast.walk(tree)), 'Fill the table with an iteration.')
        for fn in (node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)):
            self.assertFalse(any(isinstance(call, ast.Call) and isinstance(call.func, ast.Name)
                                 and call.func.id == fn.name for call in ast.walk(fn)),
                             'Use bottom-up iteration instead of recursive calls.')


if __name__ == "__main__":
    unittest.main()
