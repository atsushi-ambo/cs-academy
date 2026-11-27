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
                 or isinstance(node.func, ast.Attribute) and node.func.attr == name)]


class RackLabels(unittest.TestCase):
    def test_required_technique(self):
        nodes = function_nodes(practice.rack_labels)
        self.assertTrue(any(isinstance(node, ast.For) for node in nodes),
                        "rack_labels must use a for loop.")

    def test_one(self):
        self.assertEqual(practice.rack_labels(0, 0), ['rack-0'])

    def test_interval(self):
        self.assertEqual(practice.rack_labels(6, 8), ['rack-6', 'rack-7', 'rack-8'])

    def test_empty(self):
        self.assertEqual(practice.rack_labels(50, 40), [])


class BatchOffsets(unittest.TestCase):
    def test_required_technique(self):
        nodes = function_nodes(practice.batch_offsets)
        self.assertTrue(any(len(call.args) == 3 for call in named_calls(nodes, "range")),
                        "batch_offsets must call range() with three arguments.")

    def test_exact_stop(self):
        self.assertEqual(practice.batch_offsets(9, 3), [0, 3, 6])

    def test_one(self):
        self.assertEqual(practice.batch_offsets(2, 5), [0])

    def test_empty(self):
        self.assertEqual(practice.batch_offsets(0, 1), [])


class FailedMinutes(unittest.TestCase):
    def test_required_technique(self):
        nodes = function_nodes(practice.failed_minutes)
        self.assertTrue(any(isinstance(node, ast.For) for node in nodes),
                        "failed_minutes must use a for loop.")
        self.assertTrue(named_calls(nodes, "range"), "failed_minutes must use range().")

    def test_empty(self):
        self.assertEqual(practice.failed_minutes([], []), 0)

    def test_none_failed(self):
        self.assertEqual(practice.failed_minutes([10], [False]), 0)

    def test_mixed(self):
        self.assertEqual(practice.failed_minutes([7, 6, 4], [True, False, True]), 11)

    def test_inputs_unchanged(self):
        durations, flags = [7, 2], [False, True]
        self.assertEqual(practice.failed_minutes(durations, flags), 2)
        self.assertEqual((durations, flags), ([7, 2], [False, True]))
