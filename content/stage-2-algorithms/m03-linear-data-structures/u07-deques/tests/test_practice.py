import ast
import collections
import inspect
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "exercises"))
import practice

def reject_library_deque(test):
    module = ast.parse(inspect.getsource(practice))
    functions = {node.name: node for node in module.body if isinstance(node, ast.FunctionDef)}
    module_aliases, deque_aliases = set(), set()

    def collect(nodes):
        for node in nodes:
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name == "collections":
                        module_aliases.add((alias.asname or alias.name).split(".")[0])
            elif isinstance(node, ast.ImportFrom) and node.module == "collections":
                for alias in node.names:
                    if alias.name in ("deque", "*"):
                        deque_aliases.add(alias.asname or alias.name)

    collect(module.body)
    reachable, pending = set(), ["make_deque"]
    while pending:
        name = pending.pop()
        if name in reachable or name not in functions:
            continue
        reachable.add(name)
        collect(ast.walk(functions[name]))
        for node in ast.walk(functions[name]):
            if isinstance(node, ast.Name) and node.id in functions:
                pending.append(node.id)
    for name in reachable:
        for node in ast.walk(functions[name]):
            if isinstance(node, ast.Name):
                test.assertNotIn(node.id, deque_aliases - {"*"}, "Do not use collections.deque.")
                test.assertNotIn(node.id, {"__import__", "importlib"})
            if isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name):
                if node.value.id in module_aliases:
                    test.assertNotEqual(node.attr, "deque", "Do not use collections.deque.")
            if isinstance(node, ast.Constant) and node.value == "collections":
                test.fail("Do not import collections here.")
    test.assertNotIn("*", deque_aliases)


class MakeDeque(unittest.TestCase):
    def test_both_ends(self):
        dq = practice.make_deque(3)
        slots = dq.slots
        self.assertIsNone(dq.pop_left())
        self.assertIsNone(dq.pop_right())
        self.assertIs(dq.push_left(4), True)
        self.assertIs(dq.push_left(0), True)
        self.assertIs(dq.push_right(4), True)
        self.assertIs(dq.push_right(9), False)
        self.assertIs(dq.push_left(9), False)
        self.assertEqual(dq.pop_left(), 0)
        self.assertIs(dq.push_right(7), True)
        self.assertEqual([dq.pop_right(), dq.pop_right(), dq.pop_left()], [7, 4, 4])
        self.assertIs(dq.slots, slots)
        self.assertEqual(dq.slots, [None, None, None])

    def test_single_slot_and_technique(self):
        dq = practice.make_deque(1)
        other = practice.make_deque(1)
        self.assertIs(dq.push_left(0), True)
        self.assertIs(dq.push_right(8), False)
        self.assertIsNone(other.pop_right())
        self.assertEqual(dq.pop_right(), 0)
        self.assertIs(dq.push_right(8), True)
        self.assertEqual(dq.pop_left(), 8)
        self.assertIsNone(dq.pop_left())

    def test_technique(self):
        for capacity in (1, 3):
            dq = practice.make_deque(capacity)
            self.assertNotIsInstance(dq, collections.deque)
            for value in vars(dq).values():
                self.assertNotIsInstance(value, collections.deque)
        reject_library_deque(self)

    def test_slots_follow_every_operation(self):
        import random

        rng = random.Random(7)
        capacity = 5
        dq = practice.make_deque(capacity)
        slots = dq.slots
        model = []
        for step in range(400):
            action = rng.choice(["pl", "pr", "ql", "qr"])
            value = rng.randint(0, 3)
            if action == "pl":
                expected = len(model) < capacity
                self.assertIs(dq.push_left(value), expected)
                if expected:
                    model.insert(0, value)
            elif action == "pr":
                expected = len(model) < capacity
                self.assertIs(dq.push_right(value), expected)
                if expected:
                    model.append(value)
            elif action == "ql":
                expected = model.pop(0) if model else None
                self.assertEqual(dq.pop_left(), expected)
            else:
                expected = model.pop() if model else None
                self.assertEqual(dq.pop_right(), expected)
            self.assertIs(dq.slots, slots)
            self.assertEqual(len(slots), capacity)
            stored = sorted(item for item in slots if item is not None)
            self.assertEqual(stored, sorted(model), "Keep every item in slots.")


class OfferIndex(unittest.TestCase):
    def test_offer(self):
        from collections import deque

        values = [9, 4, 7, 9]
        candidates = deque()
        practice.offer_index(values, candidates, 0)
        self.assertEqual(list(candidates), [0])
        practice.offer_index(values, candidates, 1)
        self.assertEqual(list(candidates), [0, 1])
        practice.offer_index(values, candidates, 2)
        self.assertEqual(list(candidates), [0, 2])
        practice.offer_index(values, candidates, 3)
        self.assertEqual(list(candidates), [3])
        self.assertEqual(values, [9, 4, 7, 9])


class WindowMaxima(unittest.TestCase):
    def test_windows(self):
        cases = (
            ([], 1, []), ([4], 1, [4]), ([1, 3], 0, []), ([1, 3], 3, []),
            ([9, 4, 7, 7], 2, [9, 7, 7]), ([8, 6, 4, 2], 2, [8, 6, 4]),
            ([-8, -6, -4], 2, [-6, -4]), ([2, 1, 2], 3, [2]),
        )
        for values, k, expected in cases:
            before = values[:]
            result = practice.window_maxima(values, k)
            self.assertEqual(result, expected)
            self.assertIsNot(result, values)
            self.assertEqual(values, before)

    def test_linear_reads(self):
        class CountedList(list):
            reads = 0

            def __getitem__(self, index):
                item = super().__getitem__(index)
                self.reads += len(item) if isinstance(index, slice) else 1
                return item

            def __iter__(self):
                for index in range(len(self)):
                    yield self[index]

        values = CountedList(range(400, 0, -1))
        self.assertEqual(practice.window_maxima(values, 150), list(range(400, 149, -1)))
        self.assertLessEqual(values.reads, 16 * len(values), "Keep candidates across windows.")

    def test_comparisons_are_linear(self):
        class Counted(int):
            ops = 0

            def _tick(self):
                Counted.ops += 1

            def __lt__(self, other):
                self._tick()
                return int(self) < int(other)

            def __le__(self, other):
                self._tick()
                return int(self) <= int(other)

            def __gt__(self, other):
                self._tick()
                return int(self) > int(other)

            def __ge__(self, other):
                self._tick()
                return int(self) >= int(other)

            def __eq__(self, other):
                self._tick()
                return int(self) == int(other)

            def __ne__(self, other):
                self._tick()
                return int(self) != int(other)

            __hash__ = int.__hash__

        import random

        rng = random.Random(3)
        size, width = 400, 150
        for plain in (
            list(range(size, 0, -1)),
            list(range(size)),
            [rng.randint(0, 50) for _ in range(size)],
        ):
            Counted.ops = 0
            values = [Counted(n) for n in plain]
            result = practice.window_maxima(values, width)
            ops = Counted.ops
            expected = [max(plain[i:i + width]) for i in range(size - width + 1)]
            self.assertEqual([int(n) for n in result], expected)
            self.assertLessEqual(ops, 6 * size, "Compare each value a few times, not once per window.")
