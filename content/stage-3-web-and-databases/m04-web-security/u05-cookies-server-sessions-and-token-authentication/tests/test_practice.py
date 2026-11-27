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
        def fresh_id(taken):
            self.assertEqual(set(taken), {"guest", "other"})
            return "new"

        sessions = {"guest": None, "other": ("kai", 90)}
        self.assertEqual(practice.rotate(sessions, "guest", "lee", 30, fresh_id), "new")
        self.assertEqual(sessions, {"new": ("lee", 30), "other": ("kai", 90)})
        blank = {}
        self.assertEqual(practice.rotate(blank, "absent", "lee", 30, lambda table: "a"), "a")
        self.assertEqual(blank, {"a": ("lee", 30)})

    def test_old_id_is_never_reissued_even_when_absent(self):
        draws = iter(["gone", "gone", "next"])
        offered = []

        def fresh_id(taken):
            offered.append(set(taken))
            return practice_new_id(taken, lambda: next(draws))

        sessions = {"other": ("kai", 90)}
        self.assertEqual(practice.rotate(sessions, "gone", "lee", 30, fresh_id), "next")
        self.assertEqual(offered, [{"other", "gone"}])
        self.assertEqual(sessions, {"other": ("kai", 90), "next": ("lee", 30)})
        empty = {}
        draws = iter(["gone", "fresh"])
        self.assertEqual(practice.rotate(empty, "gone", "lee", 5, fresh_id), "fresh")
        self.assertEqual(empty, {"fresh": ("lee", 5)})

    def test_old_session_is_removed_and_others_stay(self):
        sessions = {"old": None, "a": ("kai", 1), "b": ("sam", 2)}
        snapshot = dict(sessions)
        seen = []

        def fresh_id(taken):
            seen.append(dict(taken))
            return "n"

        self.assertEqual(practice.rotate(sessions, "old", "lee", 9, fresh_id), "n")
        self.assertEqual(seen, [snapshot])
        self.assertEqual(sessions, {"a": ("kai", 1), "b": ("sam", 2), "n": ("lee", 9)})


def practice_new_id(taken, draw):
    candidate = draw()
    while candidate in taken:
        candidate = draw()
    return candidate

if __name__ == "__main__":
    unittest.main()
