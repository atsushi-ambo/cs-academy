import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "exercises"))
import practice


class SessionCookie(unittest.TestCase):
    def test_contract(self):
        from http.cookies import SimpleCookie

        for sid in ("a", "x_y-9", "b" * 64):
            cookie = SimpleCookie(practice.session_cookie(sid))
            self.assertEqual(list(cookie), ["sid"])
            item = cookie["sid"]
            self.assertEqual(item.value, sid)
            self.assertTrue(item["secure"])
            self.assertTrue(item["httponly"])
            self.assertEqual(item["samesite"], "Lax")
            self.assertEqual(item["path"], "/")
            self.assertEqual(item["domain"], "")


class NewId(unittest.TestCase):
    def test_contract(self):
        from unittest.mock import Mock

        draw = Mock(side_effect=["a", "a", "b"])
        sessions = {"a": None}
        self.assertEqual(practice.new_id(sessions, draw), "b")
        self.assertEqual(draw.call_count, 3)
        self.assertEqual(sessions, {"a": None})
        draw = Mock(return_value="first")
        self.assertEqual(practice.new_id({}, draw), "first")
        draw.assert_called_once_with()


class Rotate(unittest.TestCase):
    def test_contract(self):
        def fresh_id(sessions):
            self.assertIn("guest", sessions)
            return "new"

        sessions = {"guest": None, "other": ("kai", 90)}
        self.assertEqual(practice.rotate(sessions, "guest", "lee", 30, fresh_id), "new")
        self.assertEqual(sessions, {"new": ("lee", 30), "other": ("kai", 90)})
        blank = {}
        self.assertEqual(practice.rotate(blank, "absent", "lee", 30, lambda table: "a"), "a")
        self.assertEqual(blank, {"a": ("lee", 30)})

if __name__ == "__main__":
    unittest.main()
