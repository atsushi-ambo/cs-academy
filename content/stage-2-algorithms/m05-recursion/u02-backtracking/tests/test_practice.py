import ast
import inspect
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "exercises"))
import practice


def syntax(function):
    return ast.parse(inspect.getsource(function))


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


def check_search(test, function):
    test.assertTrue(uses_recursion(function), "Explore smaller choices with recursion.")
    test.assertFalse(any(
        isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
        and node.func.attr in {"combinations", "permutations", "product"}
        or isinstance(node, ast.ImportFrom) and node.module == "itertools"
        and any(alias.name in {"combinations", "permutations", "product", "*"}
                for alias in node.names)
        for node in ast.walk(syntax(practice))
    ), "Build the choices yourself instead of using itertools.")


class ServiceGroups(unittest.TestCase):
    def test_technique(self):
        check_search(self, practice.service_groups)

    def test_empty_and_one(self):
        self.assertCountEqual(map(tuple, practice.service_groups([])), [()])
        self.assertCountEqual(map(tuple, practice.service_groups(["api"])), [(), ("api",)])

    def test_two_services_and_input(self):
        services = ["db", "api"]
        groups = practice.service_groups(services)
        self.assertCountEqual(map(tuple, groups), [(), ("db",), ("api",), ("db", "api")])
        self.assertEqual(services, ["db", "api"])

    def test_three_services(self):
        self.assertCountEqual(map(tuple, practice.service_groups(["a", "b", "c"])),
                              [(), ("a",), ("b",), ("c",), ("a", "b"), ("a", "c"),
                               ("b", "c"), ("a", "b", "c")])


class JobOrders(unittest.TestCase):
    def test_technique(self):
        check_search(self, practice.job_orders)

    def test_empty_and_one(self):
        self.assertCountEqual(map(tuple, practice.job_orders([])), [()])
        self.assertCountEqual(map(tuple, practice.job_orders(["x"])), [("x",)])

    def test_two_and_input(self):
        jobs = ["db", "api"]
        self.assertCountEqual(map(tuple, practice.job_orders(jobs)), [("db", "api"), ("api", "db")])
        self.assertEqual(jobs, ["db", "api"])

    def test_three_orders(self):
        self.assertCountEqual(map(tuple, practice.job_orders(["a", "b", "c"])),
                              [("a", "b", "c"), ("a", "c", "b"), ("b", "a", "c"),
                               ("b", "c", "a"), ("c", "a", "b"), ("c", "b", "a")])


class CountBoards(unittest.TestCase):
    def test_technique(self):
        check_search(self, practice.count_boards)

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


if __name__ == "__main__":
    unittest.main()
