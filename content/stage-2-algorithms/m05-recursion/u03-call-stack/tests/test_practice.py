import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'exercises'))
import practice


class ExitLog(unittest.TestCase):
    def test_base(self):
        self.assertEqual(practice.exit_log(0), [0])

    def test_order(self):
        self.assertEqual(practice.exit_log(4), [0, 1, 2, 3, 4])

    def test_one(self):
        self.assertEqual(practice.exit_log(1), [0, 1])


class LoopTotal(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(practice.loop_total(0), 0)

    def test_small(self):
        self.assertEqual(practice.loop_total(4), 10)

    def test_deep(self):
        self.assertEqual(practice.loop_total(7000), 24503500)


class FastPower(unittest.TestCase):
    def test_zero(self):
        self.assertEqual(practice.fast_power(0, 0), 1)

    def test_odd(self):
        self.assertEqual(practice.fast_power(-3, 5), -243)

    def test_even(self):
        self.assertEqual(practice.fast_power(-2, 6), 64)

    def test_zero_base(self):
        self.assertEqual(practice.fast_power(0, 6), 0)

    def test_large_exponent(self):
        self.assertEqual(practice.fast_power(2, 10000), 1 << 10000)
