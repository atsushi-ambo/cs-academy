import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'exercises'))
import practice


class ChunksThatFit(unittest.TestCase):
    def test_exact(self):
        self.assertEqual(practice.chunks_that_fit(12, 4), 3)

    def test_partial(self):
        self.assertEqual(practice.chunks_that_fit(19, 6), 3)

    def test_empty(self):
        self.assertEqual(practice.chunks_that_fit(0, 5), 0)

    def test_too_small(self):
        self.assertEqual(practice.chunks_that_fit(1, 2), 0)


class ChecksUsed(unittest.TestCase):
    def test_ready_first(self):
        self.assertEqual(practice.checks_used([200, 503], 10), 1)

    def test_empty(self):
        self.assertEqual(practice.checks_used([], 5), 0)

    def test_capped(self):
        self.assertEqual(practice.checks_used([503, 503, 200], 2), 2)

    def test_exhausted(self):
        self.assertEqual(practice.checks_used([503], 10), 1)

    def test_no_budget(self):
        self.assertEqual(practice.checks_used([200], 0), 0)


class RoundsToDrain(unittest.TestCase):
    def test_partial_last(self):
        self.assertEqual(practice.rounds_to_drain(13, 5), 3)

    def test_exact(self):
        self.assertEqual(practice.rounds_to_drain(14, 7), 2)

    def test_empty(self):
        self.assertEqual(practice.rounds_to_drain(0, 7), 0)

    def test_one_round(self):
        self.assertEqual(practice.rounds_to_drain(2, 10), 1)
