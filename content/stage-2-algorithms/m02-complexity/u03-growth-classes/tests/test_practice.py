import ast
import inspect
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "exercises"))
import practice


class HalfPath(unittest.TestCase):
    def test_contract(self):
        function = practice.half_path

        def profile(frame, event, arg):
            if event == "call" and frame.f_code is function.__code__:
                visits.append(frame.f_locals[frame.f_code.co_varnames[0]])

        for size, count in ((1, 0), (2, 1), (3, 1), (18, 4), (1024, 10), (1_000_000, 19)):
            visits = []
            previous_profile = sys.getprofile()
            sys.setprofile(profile)
            try:
                self.assertEqual(function(size), count)
            finally:
                sys.setprofile(previous_profile)
            self.assertEqual(visits, [size >> level for level in range(count + 1)])
        nodes = list(ast.walk(ast.parse(inspect.getsource(function))))
        self.assertFalse(any(isinstance(node, (ast.For, ast.While, ast.comprehension)) for node in nodes))


class OrderCount(unittest.TestCase):
    def test_contract(self):
        function = practice.order_count
        for n, count in ((0, 1), (1, 1), (4, 24), (6, 720), (12, 479001600)):
            self.assertEqual(function(n), count)
        nodes = list(ast.walk(ast.parse(inspect.getsource(function))))
        self.assertEqual(sum(isinstance(node, (ast.For, ast.While, ast.comprehension))
                             for node in nodes), 1, "Use one loop over the factors.")
        self.assertFalse(any(isinstance(node, ast.Name) and node.id == "factorial"
                             or isinstance(node, ast.Attribute) and node.attr == "factorial"
                             or isinstance(node, ast.alias) and node.name == "factorial"
                             for node in nodes), "Multiply the factors without a factorial helper.")


class TripleChecks(unittest.TestCase):
    def test_contract(self):
        function = practice.triple_checks
        for n in (0, 1, 2, 7, 30, 500):
            self.assertEqual(function(n), n ** 3)
        nodes = list(ast.walk(ast.parse(inspect.getsource(function))))
        self.assertFalse(any(isinstance(node, (ast.For, ast.While, ast.comprehension))
                             for node in nodes), "Compute the count without enumerating triples.")
