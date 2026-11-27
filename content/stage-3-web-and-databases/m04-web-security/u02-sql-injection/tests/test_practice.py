import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "exercises"))
import practice


class FindPorts(unittest.TestCase):
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


class SortColumn(unittest.TestCase):
    def test_contract(self):
        self.assertEqual(practice.sort_column("name"), "label")
        self.assertEqual(practice.sort_column("number"), "port")
        for bad in ("", "port", "Name", "name ", "unknown"):
            self.assertIsNone(practice.sort_column(bad))


class TeamServices(unittest.TestCase):
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

if __name__ == "__main__":
    unittest.main()
