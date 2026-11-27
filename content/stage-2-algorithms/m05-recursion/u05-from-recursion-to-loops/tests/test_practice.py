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
            and isinstance(node.func, ast.Name) and node.func.id == name]


class ReducedPrice(unittest.TestCase):
    def test_required_technique(self):
        nodes = function_nodes(practice.reduced_price)
        self.assertFalse(named_calls(nodes, "reduced_price"), "reduced_price must not call itself. Use a loop instead.")
        self.assertTrue(any(isinstance(node, ast.While) for node in nodes),
                        "reduced_price must use a while loop.")

    def test_round_each_week(self):
        self.assertEqual(practice.reduced_price(94, 2), 75)

    def test_zero_weeks(self):
        self.assertEqual(practice.reduced_price(245, 0), 245)

    def test_deep(self):
        self.assertEqual(practice.reduced_price(10000, 9000), 0)


class UnpackSizes(unittest.TestCase):
    def test_required_technique(self):
        nodes = function_nodes(practice.unpack_sizes)
        self.assertFalse(named_calls(nodes, "unpack_sizes"), "unpack_sizes must not call itself. Use a loop instead.")
        self.assertTrue(any(isinstance(node, ast.While) for node in nodes),
                        "unpack_sizes must use a while loop.")
        self.assertTrue(
            any(isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
                and node.func.attr == "pop" for loop in nodes if isinstance(loop, ast.While)
                for node in ast.walk(loop)),
            "unpack_sizes must pop from an explicit stack inside the loop.",
        )

    def test_empty(self):
        self.assertEqual(practice.unpack_sizes([[], []]), [])

    def test_order(self):
        self.assertEqual(practice.unpack_sizes([7, [8, [9, 9]], 4, [], 0]), [7, 8, 9, 9, 4, 0])

    def test_deep(self):
        batch = [7]
        for _ in range(1499):
            batch = [batch]
        self.assertEqual(practice.unpack_sizes(batch), [7])

    def test_input_unchanged(self):
        batch = [[1, 3], 2]
        self.assertEqual(practice.unpack_sizes(batch), [1, 3, 2])
        self.assertEqual(batch, [[1, 3], 2])


class RouteCount(unittest.TestCase):
    def test_required_technique(self):
        nodes = function_nodes(practice.route_count)
        self.assertFalse(named_calls(nodes, "route_count"), "route_count must not call itself. Use a loop instead.")
        self.assertTrue(any(isinstance(node, (ast.For, ast.While)) for node in nodes),
                        "route_count must use a loop.")

    def test_empty(self):
        self.assertEqual(practice.route_count(0), 1)

    def test_single(self):
        self.assertEqual(practice.route_count(1), 1)

    def test_four(self):
        self.assertEqual(practice.route_count(4), 5)

    def test_twenty(self):
        self.assertEqual(practice.route_count(20), 10946)

    def test_hundred(self):
        self.assertEqual(practice.route_count(100), 573147844013817084101)
