import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "exercises"))
import practice


class LabelSpan(unittest.TestCase):
    def test_contract(self):
        self.assertEqual(practice.label_span("up", ""), '<span title="">up</span>')
        self.assertEqual(practice.label_span("", '"'), '<span title="&quot;"></span>')
        self.assertEqual(practice.label_span("a < b", "x & y"),
                         '<span title="x &amp; y">a &lt; b</span>')
        self.assertEqual(practice.label_span("&", "&"), '<span title="&amp;">&amp;</span>')


class FormCookie(unittest.TestCase):
    def test_contract(self):
        from http.cookies import SimpleCookie

        self.assertEqual(practice.form_cookie("lab"), "sid=lab; SameSite=Strict")
        for sid in ("a", "a-B_7", "a" * 64):
            parsed = SimpleCookie(practice.form_cookie(sid))
            self.assertEqual(list(parsed), ["sid"])
            self.assertEqual(parsed["sid"].value, sid)
            self.assertEqual(parsed["sid"]["samesite"], "Strict")


class SaveTheme(unittest.TestCase):
    def test_contract(self):
        def check(sessions, sid, token):
            return sid in sessions and sessions[sid] == token

        sessions = {"s1": "a", "s2": "b"}
        settings = {}
        request = {"method": "POST", "sid": "s1", "token": "a", "theme": "dark"}
        self.assertIs(practice.save_theme(settings, sessions, request, check), True)
        for edits in ({"method": "GET"}, {"sid": "s2"}, {"sid": "none"},
                      {"token": None}, {"theme": ""}):
            rejected = dict(request, theme="light")
            rejected.update(edits)
            original = rejected.copy()
            self.assertIs(practice.save_theme(settings, sessions, rejected, check), False)
            self.assertEqual(rejected, original)
            self.assertEqual(settings, {"s1": "dark"})
        self.assertEqual(sessions, {"s1": "a", "s2": "b"})
        self.assertEqual(request, {"method": "POST", "sid": "s1", "token": "a", "theme": "dark"})

if __name__ == "__main__":
    unittest.main()
