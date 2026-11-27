import random
import sys
import unittest
from itertools import combinations
from pathlib import Path

EXERCISES = Path(__file__).resolve().parents[1] / 'exercises'
sys.path.insert(0, str(EXERCISES))
import practice

PRACTICE_FILE = str(EXERCISES / 'practice.py')
MAX_LINES = 400000
MAX_NESTING = 6


class BudgetExceeded(Exception):
    pass


def run_measured(call):
    """Run call() and return (result, executed lines, deepest call nesting) for code in practice.py."""
    state = {'lines': 0, 'depth': 0, 'deepest': 0}

    def tracer(frame, event, arg):
        if frame.f_code.co_filename != PRACTICE_FILE:
            return None
        if event == 'call':
            state['depth'] += 1
            state['deepest'] = max(state['deepest'], state['depth'])
        return local_tracer

    def local_tracer(frame, event, arg):
        if event == 'line':
            state['lines'] += 1
            if state['lines'] > MAX_LINES:
                raise BudgetExceeded()
        elif event == 'return':
            state['depth'] -= 1
        return local_tracer

    sys.settrace(tracer)
    try:
        result = call()
    except BudgetExceeded:
        result = None
        state['lines'] = MAX_LINES + 1
    finally:
        sys.settrace(None)
    return result, state['lines'], state['deepest']


def reference_bag(items, capacity):
    best = 0
    for size in range(len(items) + 1):
        for chosen in combinations(range(len(items)), size):
            if sum(items[i][0] for i in chosen) <= capacity:
                best = max(best, sum(items[i][1] for i in chosen))
    return best


def reference_bag_table(items, capacity):
    table = [0] * (capacity + 1)
    for weight, value in items:
        for c in range(capacity, weight - 1, -1):
            table[c] = max(table[c], table[c - weight] + value)
    return table[capacity]


def reference_coins(coins, amount):
    best = [0] + [None] * amount
    for total in range(1, amount + 1):
        options = [best[total - c] + 1 for c in coins if c <= total and best[total - c] is not None]
        best[total] = min(options) if options else None
    return -1 if best[amount] is None else best[amount]


def reference_lcs(left, right):
    table = [[0] * (len(right) + 1) for _ in range(len(left) + 1)]
    for i in range(len(left)):
        for j in range(len(right)):
            table[i + 1][j + 1] = (table[i][j] + 1 if left[i] == right[j]
                                   else max(table[i][j + 1], table[i + 1][j]))
    return table[-1][-1]


def random_items(rng, count, max_weight, max_value):
    return [(rng.randint(1, max_weight), rng.randint(0, max_value)) for _ in range(count)]


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

    def test_needs_three_or_more_items(self):
        self.assertEqual(practice.bag_value([(1, 1)] * 3, 3), 3)
        self.assertEqual(practice.bag_value([(1, 2), (2, 3), (3, 5), (4, 8)], 6), 11)
        self.assertEqual(practice.bag_value([(2, 3)] * 5, 9), 12)

    def test_matches_exhaustive_search_on_random_inputs(self):
        rng = random.Random(41)
        for _ in range(150):
            items = random_items(rng, rng.randint(0, 8), 6, 9)
            capacity = rng.randint(0, 14)
            original = items[:]
            self.assertEqual(practice.bag_value(items, capacity), reference_bag(items, capacity), (items, capacity))
            self.assertEqual(items, original)

    def test_table_not_recursion_on_larger_input(self):
        rng = random.Random(5)
        items = random_items(rng, 24, 9, 40)
        expected = reference_bag_table(items, 60)
        result, lines, deepest = run_measured(lambda: practice.bag_value(items, 60))
        self.assertEqual(result, expected)
        self.assertLessEqual(deepest, MAX_NESTING, 'Use bottom-up iteration instead of recursive calls.')
        self.assertLessEqual(lines, MAX_LINES, 'Fill each table cell once instead of trying every subset.')


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


    def test_matches_reference_on_random_inputs(self):
        rng = random.Random(8)
        for _ in range(150):
            coins = [rng.randint(1, 9) for _ in range(rng.randint(0, 4))]
            amount = rng.randint(0, 30)
            original = coins[:]
            self.assertEqual(practice.min_coins(coins, amount), reference_coins(coins, amount), (coins, amount))
            self.assertEqual(coins, original)

    def test_table_not_recursion_on_larger_input(self):
        coins = [1, 5, 10, 25, 31]
        result, lines, deepest = run_measured(lambda: practice.min_coins(coins, 400))
        self.assertEqual(result, reference_coins(coins, 400))
        self.assertLessEqual(deepest, MAX_NESTING, 'Use bottom-up iteration instead of recursive calls.')
        self.assertLessEqual(lines, MAX_LINES)


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

    def test_matches_reference_on_random_inputs(self):
        rng = random.Random(3)
        for _ in range(150):
            left = ''.join(rng.choice('abc') for _ in range(rng.randint(0, 9)))
            right = ''.join(rng.choice('abc') for _ in range(rng.randint(0, 9)))
            self.assertEqual(practice.lcs_length(left, right), reference_lcs(left, right), (left, right))

    def test_table_not_recursion_on_larger_input(self):
        rng = random.Random(12)
        left = ''.join(rng.choice('abcd') for _ in range(110))
        right = ''.join(rng.choice('abcd') for _ in range(110))
        result, lines, deepest = run_measured(lambda: practice.lcs_length(left, right))
        self.assertEqual(result, reference_lcs(left, right))
        self.assertLessEqual(deepest, MAX_NESTING, 'Use bottom-up iteration instead of recursive calls.')
        self.assertLessEqual(lines, MAX_LINES)


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

    def test_three_items_needed(self):
        self.assertEqual(practice.bag_choices([(1, 1)] * 3, 3), [0, 1, 2])

    def test_best_sets_on_random_inputs(self):
        rng = random.Random(77)
        for _ in range(120):
            items = random_items(rng, rng.randint(0, 8), 6, 9)
            capacity = rng.randint(0, 14)
            original = items[:]
            chosen = practice.bag_choices(items, capacity)
            self.assertEqual(items, original)
            self.assertEqual(chosen, sorted(set(chosen)), (items, capacity))
            self.assertTrue(all(0 <= i < len(items) for i in chosen))
            self.assertLessEqual(sum(items[i][0] for i in chosen), capacity, (items, capacity))
            self.assertEqual(sum(items[i][1] for i in chosen), reference_bag(items, capacity), (items, capacity))

    def test_table_not_recursion_on_larger_input(self):
        rng = random.Random(21)
        items = random_items(rng, 24, 9, 40)
        result, lines, deepest = run_measured(lambda: practice.bag_choices(items, 60))
        self.assertLessEqual(deepest, MAX_NESTING, 'Use bottom-up iteration instead of recursive calls.')
        self.assertLessEqual(lines, MAX_LINES)
        self.assertLessEqual(sum(items[i][0] for i in result), 60)
        self.assertEqual(sum(items[i][1] for i in result), reference_bag_table(items, 60))


if __name__ == "__main__":
    unittest.main()
