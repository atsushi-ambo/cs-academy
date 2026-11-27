import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "exercises"))
import practice


class ValidTarget(unittest.TestCase):
    def test_contract(self):
        for port in (1, 443, 65535):
            self.assertIs(practice.valid_target(port, "a" * 30, "full"), True)
        for port in ("443", True, None, 443.0, 0, 65536):
            self.assertIs(practice.valid_target(port, "api", "brief"), False)
        for label in ("", "a" * 31, [], None):
            self.assertIs(practice.valid_target(443, label, "brief"), False)
        for mode in ("Full", "", ["brief"], None):
            self.assertIs(practice.valid_target(443, "api", mode), False)
        self.assertIs(practice.valid_target(443, "空", "brief"), True)


class ReportPath(unittest.TestCase):
    def test_contract(self):
        from pathlib import Path
        from tempfile import TemporaryDirectory

        with TemporaryDirectory() as folder:
            base = Path(folder).resolve()
            root = base / "reports"
            root.mkdir()
            other = base / "reports-old"
            other.mkdir()
            (other / "a.txt").touch()
            (root / "a.txt").touch()
            (root / "daily").mkdir()
            (root / "daily" / "a.txt").touch()
            (root / "outside-link").symlink_to(other, target_is_directory=True)
            (root / "loop").symlink_to(root / "loop")
            self.assertEqual(practice.report_path(root, "a.txt"), root / "a.txt")
            self.assertEqual(practice.report_path(root, "daily/a.txt"), root / "daily/a.txt")
            for bad in ("", ".", "missing.txt", str(root / "a.txt"), "../reports-old/a.txt",
                        "outside-link/a.txt", "loop/a.txt", "bad" + chr(0)):
                self.assertIsNone(practice.report_path(root, bad))
            self.assertEqual(sorted(path.name for path in root.iterdir()), ["a.txt", "daily", "loop", "outside-link"])


class EditLabel(unittest.TestCase):
    def test_contract(self):
        profile = {"id": "lee", "label": "api", "role": "viewer"}
        body = {"label": "a" * 30}
        result = practice.edit_label("lee", profile, body)
        self.assertEqual(result, {"id": "lee", "label": "a" * 30, "role": "viewer"})
        self.assertIsNot(result, profile)
        for user in (None, "kai"):
            self.assertIsNone(practice.edit_label(user, profile, body))
        for bad in ({}, {"label": ""}, {"label": False}, {"label": "x" * 31},
                    {"role": "admin"}, {"label": "web", "role": "admin"}):
            self.assertIsNone(practice.edit_label("lee", profile, bad))
        self.assertEqual(profile, {"id": "lee", "label": "api", "role": "viewer"})
        self.assertEqual(body, {"label": "a" * 30})

if __name__ == "__main__":
    unittest.main()
