import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'exercises'))
import practice


class BatchPages(unittest.TestCase):
    def test_zero(self):
        self.assertEqual(practice.batch_pages(0), 0)

    def test_one(self):
        self.assertEqual(practice.batch_pages(1), 1)

    def test_eight(self):
        self.assertEqual(practice.batch_pages(8), 36)


class JobOrders(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(practice.job_orders(0), 1)

    def test_one(self):
        self.assertEqual(practice.job_orders(1), 1)

    def test_five(self):
        self.assertEqual(practice.job_orders(5), 120)


class StairRoutes(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(practice.stair_routes(0), 1)

    def test_one(self):
        self.assertEqual(practice.stair_routes(1), 1)

    def test_two(self):
        self.assertEqual(practice.stair_routes(2), 2)

    def test_seven(self):
        self.assertEqual(practice.stair_routes(7), 21)
