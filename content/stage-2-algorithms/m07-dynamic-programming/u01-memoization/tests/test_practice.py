import importlib.util
import sys
import unittest
from pathlib import Path

EXERCISES = Path(__file__).resolve().parents[1] / 'exercises'
sys.path.insert(0, str(EXERCISES))
import practice


class TooManyCalls(Exception):
    pass


def fresh_practice():
    spec = importlib.util.spec_from_file_location('practice_fresh', EXERCISES / 'practice.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def measure(call, module, max_calls):
    """Run call() and return (result, python call count, deepest nesting) inside the exercise file."""
    path = str(EXERCISES / 'practice.py')
    state = {'calls': 0, 'depth': 0, 'deepest': 0}

    def profiler(frame, event, arg):
        if frame.f_code.co_filename != path:
            return
        if event == 'call':
            state['calls'] += 1
            state['depth'] += 1
            state['deepest'] = max(state['deepest'], state['depth'])
            if state['calls'] > max_calls:
                raise TooManyCalls()
        elif event == 'return':
            state['depth'] -= 1

    sys.setprofile(profiler)
    try:
        result = call()
    except TooManyCalls:
        result = None
        state['calls'] = max_calls + 1
    finally:
        sys.setprofile(None)
    return result, state['calls'], state['deepest']


def coin_reference(coins, amount):
    table = [1] + [0] * amount
    for coin in sorted(set(coins)):
        for total in range(coin, amount + 1):
            table[total] += table[total - coin]
    return table[amount]


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

    def test_recursive_and_cached(self):
        module = fresh_practice()
        result, calls, deepest = measure(lambda: module.fib_misses(30), module, 400)
        self.assertEqual(result, (832040, 31))
        self.assertLessEqual(calls, 150, 'Each fib state should be computed once.')
        self.assertGreaterEqual(deepest, 15, 'Use a recursive call to compute a smaller state.')


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
        module = fresh_practice()
        result, calls, deepest = measure(lambda: module.stair_ways(30), module, 400)
        self.assertEqual(result, 1346269)
        self.assertLessEqual(calls, 150, 'Store each answer so a repeated stair count is not recomputed.')
        self.assertGreaterEqual(deepest, 15, 'Use a recursive call to compute a smaller state.')


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

    def test_matches_reference_on_many_inputs(self):
        for coins, amount in [([2, 5, 3, 6], 10), ([7], 49), ([7], 50), ([1, 1, 2], 6),
                              ([4, 4, 8], 16), ([9, 5, 2], 0)]:
            self.assertEqual(practice.coin_ways(coins, amount), coin_reference(coins, amount))

    def test_recursive_and_each_state_once(self):
        coins, amount = [1, 2, 5], 100
        module = fresh_practice()
        states = len(coins) * (amount + 1)
        result, calls, deepest = measure(lambda: module.coin_ways(coins, amount), module, 4 * states + 50)
        self.assertEqual(result, coin_reference(coins, amount))
        self.assertLessEqual(calls, 4 * states + 50, 'Cache each (index, left) state so it is solved once.')
        self.assertGreaterEqual(deepest, 10, 'Use a recursive call to compute a smaller state.')


if __name__ == "__main__":
    unittest.main()
