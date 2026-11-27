import sys
import unittest
from html.parser import HTMLParser
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "exercises"))
import practice


class SpanParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.events = []
        self.text = ""

    def handle_starttag(self, tag, attrs):
        self.events.append(("start", tag, attrs))

    def handle_endtag(self, tag):
        self.events.append(("end", tag))

    def handle_data(self, data):
        self.text += data


class LabelSpan(unittest.TestCase):
    def assert_span(self, label, hint):
        output = practice.label_span(label, hint)
        self.assertTrue(output.startswith('<span title="'), output)
        self.assertTrue(output.endswith("</span>"), output)
        self.assertEqual(output.count("<"), 2, output)
        self.assertEqual(output.count(">"), 2, output)
        self.assertEqual(output.count('"'), 2, output)
        parser = SpanParser()
        parser.feed(output)
        parser.close()
        self.assertEqual(parser.events, [("start", "span", [("title", hint)]), ("end", "span")], output)
        self.assertEqual(parser.text, label, output)

    def test_contract(self):
        self.assertEqual(practice.label_span("up", ""), '<span title="">up</span>')
        self.assert_span("", '"')
        self.assert_span("a < b", "x & y")
        self.assert_span("&", "&")

    def test_markup_stays_text(self):
        self.assert_span("<b>ready</b>", '"><script>alert(1)</script>')
        self.assert_span("&lt;b&gt;", "&quot;")
        self.assert_span("say \"hi\" & 'bye'", "it's \"quoted\"")
        self.assert_span("<", "<")


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

    def test_both_themes_and_overwrite(self):
        sessions = {"s1": "a", "s2": "b"}
        settings = {}
        allow = lambda sessions, sid, token: True
        for sid, theme in (("s1", "light"), ("s2", "dark"), ("s1", "dark"), ("s1", "light")):
            request = {"method": "POST", "sid": sid, "token": "x", "theme": theme}
            self.assertIs(practice.save_theme(settings, sessions, request, allow), True)
        self.assertEqual(settings, {"s1": "light", "s2": "dark"})
        for theme in ("Dark", "blue", "light ", None):
            request = {"method": "POST", "sid": "s1", "token": "x", "theme": theme}
            self.assertIs(practice.save_theme(settings, sessions, request, allow), False)
        for method in ("get", "PUT", "", None):
            request = {"method": method, "sid": "s1", "token": "x", "theme": "dark"}
            self.assertIs(practice.save_theme(settings, sessions, request, allow), False)
        self.assertEqual(settings, {"s1": "light", "s2": "dark"})

    def test_supplied_check_decides(self):
        sessions = {"s1": "a"}
        settings = {"s1": "dark"}
        seen = []

        def deny(sessions, sid, token):
            seen.append((sessions, sid, token))
            return False

        request = {"method": "POST", "sid": "s1", "token": "a", "theme": "light"}
        self.assertIs(practice.save_theme(settings, sessions, request, deny), False)
        self.assertEqual(seen, [(sessions, "s1", "a")])
        self.assertEqual(settings, {"s1": "dark"})

        def allow(sessions, sid, token):
            seen.append((sessions, sid, token))
            return True

        request = {"method": "POST", "sid": "s1", "token": "other", "theme": "light"}
        self.assertIs(practice.save_theme(settings, sessions, request, allow), True)
        self.assertEqual(seen[-1], (sessions, "s1", "other"))
        self.assertEqual(settings, {"s1": "light"})

if __name__ == "__main__":
    unittest.main()
