import ast
import inspect
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "exercises"))
import practice


def syntax(function):
    return ast.parse(inspect.getsource(function))


GENERATORS = {"combinations", "permutations", "product", "combinations_with_replacement"}


def trace_frames(call):
    stack, state = [], {"recursed": False, "calls": 0}
    own = practice.__file__

    def profile(frame, event, argument):
        if frame.f_code.co_filename != own or frame.f_code.co_name.startswith("<"):
            return
        if event == "call":
            if frame.f_code in stack:
                state["recursed"] = True
            stack.append(frame.f_code)
            state["calls"] += 1
        elif event == "return" and stack:
            stack.pop()

    sys.setprofile(profile)
    try:
        result = call()
    finally:
        sys.setprofile(None)
    return result, state


def check_search(test, call):
    _, state = trace_frames(call)
    test.assertTrue(state["recursed"], "Explore smaller choices with recursion.")
    test.assertFalse(any(
        isinstance(node, ast.Attribute) and node.attr in GENERATORS
        or isinstance(node, ast.Name) and node.id in GENERATORS
        or isinstance(node, ast.Constant) and node.value in GENERATORS | {"itertools"}
        or isinstance(node, ast.Import) and any(alias.name.split(".")[0] in {"itertools", "importlib"}
                                                for alias in node.names)
        or isinstance(node, ast.ImportFrom) and (node.module or "").split(".")[0] in {"itertools", "importlib"}
        for node in ast.walk(syntax(practice))
    ), "Build the choices yourself instead of using itertools.")


def queens_reference(n):
    def place(row, columns, down, up):
        if row == n:
            return 1
        return sum(place(row + 1, columns | {col}, down | {row - col}, up | {row + col})
                   for col in range(n)
                   if col not in columns and row - col not in down and row + col not in up)
    return place(0, frozenset(), frozenset(), frozenset())


class ServiceGroups(unittest.TestCase):
    def test_technique(self):
        check_search(self, lambda: practice.service_groups(["a", "b", "c"]))

    def test_empty_and_one(self):
        self.assertCountEqual(map(tuple, practice.service_groups([])), [()])
        self.assertCountEqual(map(tuple, practice.service_groups(["api"])), [(), ("api",)])

    def test_two_services_and_input(self):
        services = ["db", "api"]
        groups = practice.service_groups(services)
        self.assertCountEqual(map(tuple, groups), [(), ("db",), ("api",), ("db", "api")])
        self.assertEqual(services, ["db", "api"])

    def test_eight_services_have_no_duplicates(self):
        services = [f"s{i}" for i in range(8)]
        groups = [tuple(group) for group in practice.service_groups(services)]
        self.assertEqual(len(groups), 256)
        self.assertEqual(len(set(groups)), 256)
        for group in groups:
            self.assertEqual(list(group), [item for item in services if item in group])

    def test_results_are_independent_lists(self):
        groups = practice.service_groups(["a", "b", "c"])
        self.assertEqual(len({id(group) for group in groups}), 8)
        groups[0].append("changed")
        self.assertEqual(sum(1 for group in groups if "changed" in group), 1)

    def test_three_services(self):
        self.assertCountEqual(map(tuple, practice.service_groups(["a", "b", "c"])),
                              [(), ("a",), ("b",), ("c",), ("a", "b"), ("a", "c"),
                               ("b", "c"), ("a", "b", "c")])


class JobOrders(unittest.TestCase):
    def test_technique(self):
        check_search(self, lambda: practice.job_orders(["a", "b", "c"]))

    def test_empty_and_one(self):
        self.assertCountEqual(map(tuple, practice.job_orders([])), [()])
        self.assertCountEqual(map(tuple, practice.job_orders(["x"])), [("x",)])

    def test_two_and_input(self):
        jobs = ["db", "api"]
        self.assertCountEqual(map(tuple, practice.job_orders(jobs)), [("db", "api"), ("api", "db")])
        self.assertEqual(jobs, ["db", "api"])

    def test_seven_jobs_each_order_once(self):
        import math
        jobs = [f"j{i}" for i in range(7)]
        orders = [tuple(order) for order in practice.job_orders(jobs)]
        self.assertEqual(len(orders), math.factorial(7))
        self.assertEqual(len(set(orders)), math.factorial(7))
        self.assertTrue(all(sorted(order) == jobs for order in orders))
        self.assertEqual(jobs, [f"j{i}" for i in range(7)])

    def test_orders_are_independent_lists(self):
        orders = practice.job_orders(["a", "b", "c"])
        self.assertEqual(len({id(order) for order in orders}), 6)

    def test_three_orders(self):
        self.assertCountEqual(map(tuple, practice.job_orders(["a", "b", "c"])),
                              [("a", "b", "c"), ("a", "c", "b"), ("b", "a", "c"),
                               ("b", "c", "a"), ("c", "a", "b"), ("c", "b", "a")])


class CountBoards(unittest.TestCase):
    def test_technique(self):
        check_search(self, lambda: practice.count_boards(5))

    def test_empty_and_one(self):
        self.assertEqual(practice.count_boards(0), 1)
        self.assertEqual(practice.count_boards(1), 1)

    def test_impossible_boards(self):
        self.assertEqual(practice.count_boards(2), 0)
        self.assertEqual(practice.count_boards(3), 0)

    def test_multiple_branches_and_calls(self):
        self.assertEqual(practice.count_boards(4), 2)
        self.assertEqual(practice.count_boards(5), 10)
        self.assertEqual(practice.count_boards(4), 2)

    def test_eight(self):
        self.assertEqual(practice.count_boards(8), 92)

    def test_all_sizes_match_reference(self):
        for n in range(0, 9):
            self.assertEqual(practice.count_boards(n), queens_reference(n))

    def test_conflicts_are_skipped_before_recursing(self):
        for n, limit in ((6, 1400), (7, 6000), (8, 20000)):
            count, state = trace_frames(lambda: practice.count_boards(n))
            self.assertEqual(count, queens_reference(n))
            self.assertLessEqual(state["calls"], limit, "Skip a clashing square before the next call.")


if __name__ == "__main__":
    unittest.main()
