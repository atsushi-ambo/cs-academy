import ast
import inspect
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'exercises'))
import practice


def function_nodes(function):
    return list(ast.walk(ast.parse(inspect.getsource(function))))


def named_calls(nodes, name):
    return [node for node in nodes if isinstance(node, ast.Call)
            and (isinstance(node.func, ast.Name) and node.func.id == name
                 or isinstance(node.func, ast.Attribute) and node.func.attr == name
                 and isinstance(node.func.value, ast.Name) and node.func.value.id == "builtins")]


class BatchPages(unittest.TestCase):
    def test_required_technique(self):
        nodes = function_nodes(practice.batch_pages)
        self.assertTrue(named_calls(nodes, "batch_pages"),
                        "This exercise must use recursion: batch_pages never calls itself.")
        self.assertFalse(any(isinstance(node, (ast.For, ast.AsyncFor, ast.While, ast.comprehension)) for node in nodes),
                         "batch_pages must not use loops.")
        self.assertFalse(named_calls(nodes, "sum"), "batch_pages must not use sum().")

    def test_zero(self):
        self.assertEqual(practice.batch_pages(0), 0)

    def test_one(self):
        self.assertEqual(practice.batch_pages(1), 1)

    def test_eight(self):
        self.assertEqual(practice.batch_pages(8), 36)


class JobOrders(unittest.TestCase):
    def test_required_technique(self):
        nodes = function_nodes(practice.job_orders)
        self.assertTrue(named_calls(nodes, "job_orders"),
                        "This exercise must use recursion: job_orders never calls itself.")

    def test_empty(self):
        self.assertEqual(practice.job_orders(0), 1)

    def test_one(self):
        self.assertEqual(practice.job_orders(1), 1)

    def test_five(self):
        self.assertEqual(practice.job_orders(5), 120)


class StairRoutes(unittest.TestCase):
    def test_required_technique(self):
        nodes = function_nodes(practice.stair_routes)
        self.assertEqual(len(named_calls(nodes, "stair_routes")), 2,
                         "stair_routes must call itself twice in its recursive case.")

    def test_empty(self):
        self.assertEqual(practice.stair_routes(0), 1)

    def test_one(self):
        self.assertEqual(practice.stair_routes(1), 1)

    def test_two(self):
        self.assertEqual(practice.stair_routes(2), 2)

    def test_seven(self):
        self.assertEqual(practice.stair_routes(7), 21)
