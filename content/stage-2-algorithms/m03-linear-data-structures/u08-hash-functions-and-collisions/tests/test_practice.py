import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "exercises"))
import practice



def reject_shortcuts(test, function, names):
    import ast
    import inspect

    for node in ast.walk(ast.parse(inspect.getsource(function))):
        if isinstance(node, ast.Call):
            name = node.func
            if isinstance(name, ast.Name):
                test.assertNotIn(name.id, names)
            elif isinstance(name, ast.Attribute):
                test.assertNotIn(name.attr, names)
        elif isinstance(node, (ast.Import, ast.ImportFrom)):
            for imported in node.names:
                test.assertNotIn(imported.name, names)


def pairs(slots):
    return [None if pair is None else tuple(pair) for pair in slots]


class StringSlot(unittest.TestCase):
    def test_hash(self):
        for key, capacity, expected in (
            ("", 7, 0), ("a", 7, 6), ("ab", 7, 4), ("ba", 7, 6),
            ("cc", 5, 3), ("é", 8, 1), ("ab", 1, 0),
        ):
            self.assertEqual(practice.string_slot(key, capacity), expected)
        reject_shortcuts(self, practice.string_slot, {"hash"})


class MakeChainedMap(unittest.TestCase):
    def test_collision_resize_and_updates(self):
        table = practice.make_chained_map(2)
        self.assertEqual((table.size, table.buckets), (0, [[], []]))
        self.assertIsNone(table.get("c"))
        table.put("a", 4)
        table.put("c", 7)
        self.assertEqual(dict(table.buckets[1]), {"a": 4, "c": 7})
        self.assertEqual(table.get("c"), 7)
        table.put("c", 0)
        self.assertEqual((len(table.buckets), table.size), (2, 2))
        table.put("e", 9)
        self.assertEqual((len(table.buckets), table.size), (4, 3))
        self.assertEqual(dict(table.buckets[1]), {"a": 4, "e": 9})
        self.assertEqual(dict(table.buckets[3]), {"c": 0})
        expected = {"a": 4, "c": 0, "e": 9, "": 5, "api": 12, "db": 8}
        for key, value in expected.items():
            table.put(key, value)
        self.assertEqual((len(table.buckets), table.size), (8, 6))
        self.assertEqual({key: table.get(key) for key in expected}, expected)

    def test_one_bucket_and_technique(self):
        import ast
        import inspect

        table = practice.make_chained_map(1)
        other = practice.make_chained_map(1)
        table.put("", 0)
        self.assertEqual(table.get(""), 0)
        self.assertIsNone(other.get(""))
        source = ast.parse(inspect.getsource(practice.make_chained_map))
        self.assertFalse(any(isinstance(node, (ast.Dict, ast.DictComp)) for node in ast.walk(source)))
        reject_shortcuts(self, practice.make_chained_map, {"dict", "defaultdict", "hash"})


class MakeProbingMap(unittest.TestCase):
    def test_probe_wrap_and_full(self):
        table = practice.make_probing_map(4)
        slots = table.slots
        self.assertIsNone(table.get("c"))
        for key, value in (("c", 6), ("g", 3), ("k", 0), ("o", 3)):
            self.assertIs(table.put(key, value), True)
        self.assertEqual(pairs(slots), [("g", 3), ("k", 0), ("o", 3), ("c", 6)])
        self.assertEqual(table.get("k"), 0)
        self.assertEqual(table.get("c"), 6)
        self.assertIsNone(table.get("s"))
        self.assertIs(table.put("s", 9), False)
        self.assertIs(table.put("k", 9), True)
        self.assertEqual(table.get("k"), 9)
        self.assertIs(table.slots, slots)

    def test_multi_character_keys(self):
        table = practice.make_probing_map(4)
        for key, value in (("ba", 1), ("cc", 2), ("db", 3), ("api", 4)):
            self.assertIs(table.put(key, value), True)
        self.assertEqual(pairs(table.slots), [("cc", 2), ("api", 4), ("db", 3), ("ba", 1)])
        for key, value in (("ba", 1), ("cc", 2), ("db", 3), ("api", 4)):
            self.assertEqual(table.get(key), value)
        self.assertIsNone(table.get("ab"))
        self.assertIs(table.put("db", 8), True)
        self.assertEqual(table.get("db"), 8)
        self.assertIs(table.put("ab", 5), False)

    def test_one_slot_and_technique(self):
        import ast
        import inspect

        table = practice.make_probing_map(1)
        self.assertIs(table.put("", 0), True)
        self.assertIs(table.put("a", 3), False)
        self.assertEqual(table.get(""), 0)
        self.assertIsNone(table.get("a"))
        source = ast.parse(inspect.getsource(practice.make_probing_map))
        self.assertFalse(any(isinstance(node, (ast.Dict, ast.DictComp)) for node in ast.walk(source)))
        reject_shortcuts(self, practice.make_probing_map, {"dict", "defaultdict", "hash"})
