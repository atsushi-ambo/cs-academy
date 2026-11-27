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


class SizeTotal(unittest.TestCase):
    def test_required_technique(self):
        nodes = function_nodes(practice.size_total)
        self.assertTrue(named_calls(nodes, "size_total"),
                        "This exercise must use recursion: size_total never calls itself.")
        self.assertFalse(any(isinstance(node, ast.Slice) for node in nodes),
                         "size_total must not use slices.")

    def test_base(self):
        self.assertEqual(practice.size_total([7], 1), 0)

    def test_empty(self):
        self.assertEqual(practice.size_total([]), 0)

    def test_suffix(self):
        self.assertEqual(practice.size_total([9, 2, 3], 1), 5)

    def test_all(self):
        self.assertEqual(practice.size_total([9, 0, 3]), 12)


class ReverseLabel(unittest.TestCase):
    def test_required_technique(self):
        nodes = function_nodes(practice.reverse_label)
        self.assertTrue(named_calls(nodes, "reverse_label"),
                        "This exercise must use recursion: reverse_label never calls itself.")
        self.assertTrue(any(isinstance(node, ast.Slice) for node in nodes),
                        "reverse_label must use slices.")
        self.assertFalse(named_calls(nodes, "reversed"), "reverse_label must not use reversed().")
        self.assertFalse(any(isinstance(node, ast.Slice) and isinstance(node.step, ast.UnaryOp)
                             and isinstance(node.step.op, ast.USub) for node in nodes),
                         "reverse_label must not use a negative slice step.")

    def test_empty(self):
        self.assertEqual(practice.reverse_label(""), '')

    def test_one(self):
        self.assertEqual(practice.reverse_label("z"), 'z')

    def test_spaces(self):
        self.assertEqual(practice.reverse_label(" A-2"), '2-A ')

    def test_repeat(self):
        self.assertEqual(practice.reverse_label("abbb"), 'bbba')


class IsMirror(unittest.TestCase):
    def test_required_technique(self):
        nodes = function_nodes(practice.is_mirror)
        self.assertTrue(named_calls(nodes, "is_mirror"),
                        "This exercise must use recursion: is_mirror never calls itself.")
        self.assertFalse(any(isinstance(node, ast.Slice) for node in nodes),
                         "is_mirror must not use slices.")

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
    def test_required_technique(self):
        nodes = function_nodes(practice.flatten_sizes)
        self.assertTrue(named_calls(nodes, "flatten_sizes"),
                        "This exercise must use recursion: flatten_sizes never calls itself.")

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
