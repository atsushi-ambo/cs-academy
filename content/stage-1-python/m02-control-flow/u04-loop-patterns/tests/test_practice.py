import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'exercises'))
import practice


class ErrorCount(unittest.TestCase):
    def test_boundary(self):
        self.assertEqual(practice.error_count([499, 500, 501, 599]), 3)

    def test_empty(self):
        self.assertEqual(practice.error_count([]), 0)

    def test_no_errors(self):
        self.assertEqual(practice.error_count([200, 404]), 0)


class FirstRecovery(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(practice.first_recovery([]), -1)

    def test_first(self):
        self.assertEqual(practice.first_recovery([200, 200]), 0)

    def test_late(self):
        self.assertEqual(practice.first_recovery([503, 504, 200, 200]), 2)

    def test_miss(self):
        self.assertEqual(practice.first_recovery([404, 500]), -1)


class LargeFiles(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(practice.large_files([], 10), 0)

    def test_empty_rows(self):
        self.assertEqual(practice.large_files([[], []], 0), 0)

    def test_uneven(self):
        self.assertEqual(practice.large_files([[3], [], [2, 9, 2], [8]], 3), 3)

    def test_boundary(self):
        self.assertEqual(practice.large_files([[5, 4], [5]], 5), 2)
