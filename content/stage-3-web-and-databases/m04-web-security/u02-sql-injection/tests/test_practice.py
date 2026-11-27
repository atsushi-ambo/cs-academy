import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "exercises"))
import practice


class SpyDb:
    """Wraps a real SQLite connection and records every statement and its parameters."""

    def __init__(self, db):
        self.db = db
        self.calls = []

    def execute(self, sql, params=()):
        self.calls.append((sql, params))
        return self.db.execute(sql, params)

    def cursor(self):
        return SpyCursor(self, self.db.cursor())

    def __getattr__(self, name):
        return getattr(self.db, name)


class SpyCursor:
    def __init__(self, spy, cursor):
        self.spy = spy
        self.cursor = cursor

    def execute(self, sql, params=()):
        self.spy.calls.append((sql, params))
        self.cursor.execute(sql, params)
        return self

    def __getattr__(self, name):
        return getattr(self.cursor, name)


def bound_values(params):
    return list(params.values()) if isinstance(params, dict) else list(params)


class BindingCase(unittest.TestCase):
    def assert_bound(self, spy, values):
        self.assertTrue(spy.calls, "run the query with db.execute")
        for sql, params in spy.calls:
            for value in values:
                self.assertNotIn(value, sql, "the value must not be placed in the SQL text")
                self.assertIn(value, bound_values(params), "pass the value as a bound parameter")


class FindPorts(BindingCase):
    def test_contract(self):
        import sqlite3

        db = sqlite3.connect(":memory:")
        db.execute("CREATE TABLE endpoints (team TEXT, host TEXT, port INTEGER)")
        self.assertEqual(practice.find_ports(db, "ops", "edge"), [])
        rows = [("ops", "edge", 443), ("ops", "edge", 80), ("other", "edge", 19),
                ("ops", "other", 21), ("ops", "edge", 80), ("", "O'Neil", 443)]
        db.executemany("INSERT INTO endpoints VALUES (?, ?, ?)", rows)
        self.assertEqual(practice.find_ports(db, "ops", "edge"), [(80,), (80,), (443,)])
        self.assertEqual(practice.find_ports(db, "", "O'Neil"), [(443,)])
        self.assertEqual(practice.find_ports(db, "edge", "ops"), [])
        self.assertEqual(db.execute("SELECT count(*) FROM endpoints").fetchone(), (6,))

    def test_values_are_bound_not_joined(self):
        import sqlite3

        db = sqlite3.connect(":memory:")
        db.execute("CREATE TABLE endpoints (team TEXT, host TEXT, port INTEGER)")
        db.executemany("INSERT INTO endpoints VALUES (?, ?, ?)",
                       [("t'1", "h'1", 22), ("t'2", "h'2", 25), ("t'1", "h'2", 53)])
        texts = set()
        for team, host, expected in (("t'1", "h'1", [(22,)]), ("t'2", "h'2", [(25,)]),
                                     ("t'1", "h'2", [(53,)])):
            spy = SpyDb(db)
            self.assertEqual(practice.find_ports(spy, team, host), expected)
            self.assert_bound(spy, [team, host])
            texts.update(sql for sql, _ in spy.calls)
        self.assertEqual(len(texts), 1, "the SQL text must not change with the data")


class SortColumn(unittest.TestCase):
    def test_contract(self):
        self.assertEqual(practice.sort_column("name"), "label")
        self.assertEqual(practice.sort_column("number"), "port")
        for bad in ("", "port", "Name", "name ", "unknown"):
            self.assertIsNone(practice.sort_column(bad))


class TeamServices(BindingCase):
    def test_contract(self):
        import sqlite3

        db = sqlite3.connect(":memory:")
        db.execute("CREATE TABLE services (team TEXT, label TEXT, port INTEGER)")
        self.assertEqual(practice.team_services(db, "ops", "name"), [])
        rows = [("ops", "z", 80), ("other", "b", 21), ("ops", "a", 443),
                ("ops", "a", 80), ("ops", "z", 80), ("O'Neil", "v", 20)]
        db.executemany("INSERT INTO services VALUES (?, ?, ?)", rows)
        self.assertEqual(practice.team_services(db, "ops", "name"),
                         [("a", 80), ("a", 443), ("z", 80), ("z", 80)])
        self.assertEqual(practice.team_services(db, "ops", "number"),
                         [("a", 80), ("z", 80), ("z", 80), ("a", 443)])
        self.assertEqual(practice.team_services(db, "O'Neil", "name"), [("v", 20)])
        self.assertIsNone(practice.team_services(db, "ops", "port"))
        self.assertIsNone(practice.team_services(db, "ops", ""))
        self.assertEqual(db.execute("SELECT count(*) FROM services").fetchone()[0], 6)

    def test_team_is_bound_and_order_is_fixed_text(self):
        import sqlite3

        db = sqlite3.connect(":memory:")
        db.execute("CREATE TABLE services (team TEXT, label TEXT, port INTEGER)")
        db.executemany("INSERT INTO services VALUES (?, ?, ?)",
                       [("t'1", "b", 2), ("t'2", "a", 1), ("t'1", "a", 3)])
        for order in ("name", "number"):
            texts = set()
            for team in ("t'1", "t'2", "t'3"):
                spy = SpyDb(db)
                practice.team_services(spy, team, order)
                self.assert_bound(spy, [team])
                texts.update(sql for sql, _ in spy.calls)
            self.assertEqual(len(texts), 1, "the SQL text must not change with the team")
        spy = SpyDb(db)
        self.assertIsNone(practice.team_services(spy, "t'1", "name; DROP TABLE services"))
        self.assertEqual(spy.calls, [], "an unknown order must not reach the database")
        self.assertEqual(db.execute("SELECT count(*) FROM services").fetchone()[0], 3)

if __name__ == "__main__":
    unittest.main()
