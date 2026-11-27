import ast
import inspect
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "exercises"))
import practice


def syntax(function):
    return ast.parse(inspect.getsource(function))


FORBIDDEN_SORTS = {"sorted", "sort", "heapq", "bisect", "importlib"}


def bound_names(tree):
    names = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            names.add(node.name)
        elif isinstance(node, ast.arg):
            names.add(node.arg)
        elif isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
            names.add(node.id)
    return names


def uses_library_sort(tree):
    bound = bound_names(tree)
    for node in ast.walk(tree):
        if isinstance(node, ast.Name) and node.id in FORBIDDEN_SORTS and node.id not in bound:
            return True
        if isinstance(node, ast.Attribute) and node.attr in FORBIDDEN_SORTS:
            return True
        if isinstance(node, ast.Constant) and isinstance(node.value, str) and node.value in FORBIDDEN_SORTS:
            return True
        if isinstance(node, ast.Import) and any(alias.name.split(".")[0] in FORBIDDEN_SORTS
                                                for alias in node.names):
            return True
        if isinstance(node, ast.ImportFrom) and (node.module or "").split(".")[0] in FORBIDDEN_SORTS:
            return True
    return False


def trace_frames(call):
    """Run call() and report (recursed, calls, max_depth) for frames from practice.py."""
    stack, state = [], {"recursed": False, "calls": 0, "depth": 0}
    own = practice.__file__

    def profile(frame, event, argument):
        if frame.f_code.co_filename != own or frame.f_code.co_name.startswith("<"):
            return
        if event == "call":
            if frame.f_code in stack:
                state["recursed"] = True
            stack.append(frame.f_code)
            state["calls"] += 1
            state["depth"] = max(state["depth"], len(stack))
        elif event == "return" and stack:
            stack.pop()

    sys.setprofile(profile)
    try:
        result = call()
    finally:
        sys.setprofile(None)
    return result, state


class Key(int):
    log = []

    def _compare(name):
        def method(self, other):
            Key.log.append(1)
            return getattr(int, name)(self, other)
        return method

    __lt__ = _compare("__lt__")
    __le__ = _compare("__le__")
    __gt__ = _compare("__gt__")
    __ge__ = _compare("__ge__")
    __hash__ = int.__hash__


class NoPow(int):
    multiplications = 0

    def __pow__(self, *args):
        raise AssertionError("Use multiplication instead of ** or pow().")

    __rpow__ = __pow__

    def __mul__(self, other):
        NoPow.multiplications += 1
        return NoPow(int.__mul__(self, other))

    def __rmul__(self, other):
        NoPow.multiplications += 1
        return NoPow(int.__mul__(self, other))


def brute_inversions(values):
    return sum(1 for i in range(len(values)) for j in range(i + 1, len(values)) if values[i] > values[j])


class PeakDelay(unittest.TestCase):
    def test_technique(self):
        _, state = trace_frames(lambda: practice.peak_delay([3, 1, 4, 1, 5, 9, 2, 6]))
        self.assertTrue(state["recursed"], "Use recursion to split the range.")

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

    def test_full_size_input_splits_into_halves(self):
        import random
        rng = random.Random(1)
        for position in (0, 1023, 511, 512):
            delays = [rng.randint(-50, 50) for _ in range(1024)]
            delays[position] = 99
            before = list(delays)
            result, state = trace_frames(lambda: practice.peak_delay(delays))
            self.assertEqual(result, 99)
            self.assertEqual(delays, before)
            self.assertLessEqual(state["depth"], 30, "Split into two halves, not one item at a time.")
        self.assertEqual(practice.peak_delay([-5] * 1024), -5)
        self.assertEqual(practice.peak_delay(list(range(1024))), 1023)


class FastPower(unittest.TestCase):
    def test_technique(self):
        tree = syntax(practice)
        self.assertFalse(any(isinstance(node, ast.Pow)
                             or isinstance(node, ast.Call) and (
                                 isinstance(node.func, ast.Name) and node.func.id == "pow"
                                 or isinstance(node.func, ast.Attribute) and node.func.attr == "pow")
                             or isinstance(node, ast.Name) and node.id == "pow"
                             or isinstance(node, ast.Attribute) and node.attr in {"pow", "__pow__"}
                             or isinstance(node, ast.Constant) and node.value in {"pow", "__pow__"}
                             or isinstance(node, ast.AugAssign) and isinstance(node.op, ast.Pow)
                             for node in ast.walk(tree)), "Use multiplication to square.")
        _, state = trace_frames(lambda: practice.fast_power(3, 40))
        self.assertTrue(state["recursed"])

    def test_base_and_zero(self):
        self.assertEqual(practice.fast_power(0, 0), 1)
        self.assertEqual(practice.fast_power(0, 8), 0)
        self.assertEqual(practice.fast_power(9, 1), 9)

    def test_even_and_odd(self):
        self.assertEqual(practice.fast_power(-3, 6), 729)
        self.assertEqual(practice.fast_power(-3, 7), -2187)

    def test_large_exponent(self):
        self.assertEqual(practice.fast_power(-2, 9_001), (-2) ** 9_001)

    def test_each_smaller_power_is_computed_once(self):
        for exponent in (9_001, 8_192, 10_000, 4_095):
            NoPow.multiplications = 0
            result, state = trace_frames(lambda: practice.fast_power(NoPow(-3), exponent))
            self.assertEqual(result, (-3) ** exponent)
            self.assertLessEqual(state["calls"], 40, "Reuse one recursive answer.")
            self.assertLessEqual(NoPow.multiplications, 60)

    def test_all_small_cases(self):
        for base in range(-9, 10):
            for exponent in range(0, 13):
                self.assertEqual(practice.fast_power(base, exponent), base ** exponent)


class CountInversions(unittest.TestCase):
    def test_technique(self):
        self.assertFalse(uses_library_sort(syntax(practice)))
        _, state = trace_frames(lambda: practice.count_inversions([4, 3, 2, 1, 5, 0]))
        self.assertTrue(state["recursed"], "Use recursion on halves.")

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

    def test_random_inputs_match_brute_force(self):
        import random
        rng = random.Random(8)
        for _ in range(80):
            values = [rng.randint(-4, 6) for _ in range(rng.randint(0, 30))]
            before = list(values)
            self.assertEqual(practice.count_inversions(values), brute_inversions(before))
            self.assertEqual(values, before)

    def test_comparisons_stay_near_n_log_n(self):
        import random
        rng = random.Random(2)
        for values, expected in (([rng.randint(0, 500) for _ in range(2048)], None),
                                 (list(range(2048, 0, -1)), 2048 * 2047 // 2), ([7] * 2048, 0)):
            if expected is None:
                expected = brute_inversions(values)
            items = [Key(value) for value in values]
            Key.log = []
            result, state = trace_frames(lambda: practice.count_inversions(items))
            self.assertEqual(result, expected)
            self.assertLessEqual(len(Key.log), 2048 * 12 * 2, "Count cross pairs while merging.")
            self.assertLessEqual(state["depth"], 40)


if __name__ == "__main__":
    unittest.main()
