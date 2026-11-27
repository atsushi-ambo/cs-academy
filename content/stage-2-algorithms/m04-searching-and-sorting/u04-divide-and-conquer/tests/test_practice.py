import ast
import inspect
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "exercises"))
import practice


def syntax(function):
    return ast.parse(inspect.getsource(function))


def uses_library_sort(tree):
    return any(
        isinstance(node, ast.Call) and (
            isinstance(node.func, ast.Name) and node.func.id == "sorted"
            or isinstance(node.func, ast.Attribute) and node.func.attr in {"sort", "sorted"}
        )
        or isinstance(node, ast.ImportFrom) and any(
            alias.name in {"sorted", "sort"} for alias in node.names
        )
        for node in ast.walk(tree)
    )


def uses_recursion(function):
    # Resolve nested helpers in the scope of their enclosing function.
    def definitions(nodes):
        return {node.name: node for node in nodes if isinstance(node, ast.FunctionDef)}

    def called_names(node):
        for child in ast.iter_child_nodes(node):
            if isinstance(child, ast.FunctionDef):
                continue
            if isinstance(child, ast.Call) and isinstance(child.func, ast.Name):
                yield child.func.id
            yield from called_names(child)

    def has_cycle(node, scope, active):
        if node in active:
            return True
        visible = {**scope, **definitions(node.body)}
        return any(has_cycle(visible[name], visible, active | {node})
                   for name in called_names(node) if name in visible)

    outer = definitions(syntax(practice).body)
    return has_cycle(outer[function.__name__], outer, set())


class PeakDelay(unittest.TestCase):
    def test_technique(self):
        self.assertTrue(uses_recursion(practice.peak_delay), "Use recursion to split the range.")

    def test_empty_and_one(self):
        self.assertIsNone(practice.peak_delay([]))
        self.assertEqual(practice.peak_delay([-9]), -9)

    def test_odd_length_and_ties(self):
        delays = [-2, -4, -1, -7, -1]
        self.assertEqual(practice.peak_delay(delays), -1)
        self.assertEqual(delays, [-2, -4, -1, -7, -1])

    def test_peak_on_each_side(self):
        self.assertEqual(practice.peak_delay([24, 0, 3, 2]), 24)
        self.assertEqual(practice.peak_delay([3, 2, 0, 24]), 24)


class FastPower(unittest.TestCase):
    def test_technique(self):
        self.assertTrue(uses_recursion(practice.fast_power))
        self.assertFalse(any(isinstance(node, ast.Pow)
                             or isinstance(node, ast.Call) and (
                                 isinstance(node.func, ast.Name) and node.func.id == "pow"
                                 or isinstance(node.func, ast.Attribute) and node.func.attr == "pow"
                             ) for node in ast.walk(syntax(practice))), "Use multiplication to square.")

    def test_base_and_zero(self):
        self.assertEqual(practice.fast_power(0, 0), 1)
        self.assertEqual(practice.fast_power(0, 8), 0)
        self.assertEqual(practice.fast_power(9, 1), 9)

    def test_even_and_odd(self):
        self.assertEqual(practice.fast_power(-3, 6), 729)
        self.assertEqual(practice.fast_power(-3, 7), -2187)

    def test_large_exponent(self):
        self.assertEqual(practice.fast_power(-2, 9_001), (-2) ** 9_001)


class CountInversions(unittest.TestCase):
    def test_technique(self):
        self.assertTrue(uses_recursion(practice.count_inversions))
        self.assertFalse(uses_library_sort(syntax(practice)))

    def test_empty_and_one(self):
        self.assertEqual(practice.count_inversions([]), 0)
        self.assertEqual(practice.count_inversions([9]), 0)

    def test_ties_and_input(self):
        values = [7, 3, 3, 5]
        self.assertEqual(practice.count_inversions(values), 3)
        self.assertEqual(values, [7, 3, 3, 5])
        self.assertEqual(practice.count_inversions([4, 4, 4]), 0)

    def test_cross_and_inner_pairs(self):
        self.assertEqual(practice.count_inversions([5, 2, 6, 1, 3]), 6)
        size = 2048
        self.assertEqual(practice.count_inversions(list(range(size, 0, -1))),
                         size * (size - 1) // 2)


if __name__ == "__main__":
    unittest.main()
