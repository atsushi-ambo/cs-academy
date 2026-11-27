import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'exercises'))
import practice


class SizeTotal(unittest.TestCase):
    def test_base(self):
        self.assertEqual(practice.size_total([7], 1), 0)

    def test_empty(self):
        self.assertEqual(practice.size_total([]), 0)

    def test_suffix(self):
        self.assertEqual(practice.size_total([9, 2, 3], 1), 5)

    def test_all(self):
        self.assertEqual(practice.size_total([9, 0, 3]), 12)


class ReverseLabel(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(practice.reverse_label(""), '')

    def test_one(self):
        self.assertEqual(practice.reverse_label("z"), 'z')

    def test_spaces(self):
        self.assertEqual(practice.reverse_label(" A-2"), '2-A ')

    def test_repeat(self):
        self.assertEqual(practice.reverse_label("abbb"), 'bbba')


class IsMirror(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(practice.is_mirror(""), True)

    def test_case(self):
        self.assertEqual(practice.is_mirror("Aa"), False)

    def test_even(self):
        self.assertEqual(practice.is_mirror("noon"), True)

    def test_inner(self):
        self.assertEqual(practice.is_mirror("xabaz", 1, 3), True)

    def test_mismatch(self):
        self.assertEqual(practice.is_mirror("abda"), False)


class FlattenSizes(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(practice.flatten_sizes([[], []]), [])

    def test_order(self):
        self.assertEqual(practice.flatten_sizes([[7, [8]], 2, [2, [], [4]]]), [7, 8, 2, 2, 4])

    def test_single(self):
        self.assertEqual(practice.flatten_sizes([0]), [0])

    def test_repeat_and_input_unchanged(self):
        source = [1, [2, [3]]]
        first = practice.flatten_sizes(source)
        self.assertEqual(practice.flatten_sizes([4]), [4])
        self.assertEqual(first, [1, 2, 3])
        self.assertEqual(source, [1, [2, [3]]])
