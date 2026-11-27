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


class ExitLog(unittest.TestCase):
    def test_required_technique(self):
        nodes = function_nodes(practice.exit_log)
        self.assertEqual(len(named_calls(nodes, "exit_log")), 1,
                         "exit_log must call itself once in its recursive case.")
        self.assertFalse(any(isinstance(node, (ast.For, ast.AsyncFor, ast.While, ast.comprehension)) for node in nodes),
                         "exit_log must not use loops.")

    def test_base(self):
        self.assertEqual(practice.exit_log(0), [0])

    def test_order(self):
        self.assertEqual(practice.exit_log(4), [0, 1, 2, 3, 4])

    def test_one(self):
        self.assertEqual(practice.exit_log(1), [0, 1])


class LoopTotal(unittest.TestCase):
    def test_required_technique(self):
        nodes = function_nodes(practice.loop_total)
        self.assertFalse(named_calls(nodes, "loop_total"), "loop_total must not call itself. Use a loop instead.")
        self.assertTrue(any(isinstance(node, ast.While) for node in nodes),
                        "loop_total must use a while loop.")
        self.assertFalse(named_calls(nodes, "sum"), "loop_total must not use sum().")

    def test_empty(self):
        self.assertEqual(practice.loop_total(0), 0)

    def test_small(self):
        self.assertEqual(practice.loop_total(4), 10)

    def test_deep(self):
        self.assertEqual(practice.loop_total(7000), 24503500)


class FastPower(unittest.TestCase):
    def test_required_technique(self):
        nodes = function_nodes(practice.fast_power)
        self.assertEqual(len(named_calls(nodes, "fast_power")), 1,
                         "fast_power must call itself once in its recursive case.")
        self.assertFalse(any(isinstance(node, (ast.For, ast.AsyncFor, ast.While, ast.comprehension)) for node in nodes),
                         "fast_power must not use loops.")
        self.assertFalse(any(isinstance(node, ast.Pow) for node in nodes),
                         "fast_power must not use **.")
        self.assertFalse(named_calls(nodes, "pow"), "fast_power must not use pow().")

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
