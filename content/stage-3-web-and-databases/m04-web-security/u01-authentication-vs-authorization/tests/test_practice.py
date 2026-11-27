import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "exercises"))
import practice


class Authorize(unittest.TestCase):
    def test_contract(self):
        lee = {"id": "lee", "role": "member", "org": "north"}
        admin = {"id": "kai", "role": "admin", "org": "north"}
        report = {"owner": "lee", "org": "north"}
        self.assertIs(practice.authorize(lee, "read", report), True)
        self.assertIs(practice.authorize(lee, "edit", report), True)
        self.assertIs(practice.authorize(lee, "publish", report), False)
        self.assertIs(practice.authorize(admin, "read", report), True)
        self.assertIs(practice.authorize(admin, "edit", report), False)
        self.assertIs(practice.authorize(dict(lee, id="pat"), "read", report), False)
        self.assertIs(practice.authorize(dict(admin, org="south"), "read", report), False)
        self.assertIs(practice.authorize(dict(lee, role="temp"), "edit", report), False)
        self.assertIs(practice.authorize(None, "read", report), False)
        self.assertIs(practice.authorize(lee, "read", None), False)
        self.assertEqual(report, {"owner": "lee", "org": "north"})
        self.assertEqual(lee, {"id": "lee", "role": "member", "org": "north"})


class VisibleIds(unittest.TestCase):
    def test_contract(self):
        def allowed(actor, action, report):
            return actor == "lee" and action == "read" and report["id"] == "a"

        reports = [{"id": "b"}, {"id": "a"}, {"id": "a"}]
        self.assertEqual(practice.visible_ids("lee", reports, allowed), ["a", "a"])
        self.assertEqual(practice.visible_ids("lee", reports[:1], allowed), [])
        self.assertEqual(practice.visible_ids(None, reports, allowed), [])
        self.assertEqual(practice.visible_ids("lee", [], allowed), [])
        self.assertEqual(reports, [{"id": "b"}, {"id": "a"}, {"id": "a"}])


class ReportBody(unittest.TestCase):
    def test_contract(self):
        def allowed(user, action, report):
            return user["id"] == report["owner"] and action == "read"

        sessions = {"s1": {"id": "lee"}, "s2": {"id": "kai"}, "": {"id": "lee"}}
        reports = {"r1": {"owner": "lee", "body": ""}}
        self.assertEqual(practice.report_body(sessions, reports, "s1", "r1", allowed), "")
        for key in ("", "s2", "expired"):
            self.assertIsNone(practice.report_body(sessions, reports, key, "r1", allowed))
        self.assertIsNone(practice.report_body(sessions, {}, "s1", "r1", allowed))
        self.assertEqual(sessions["s1"], {"id": "lee"})
        self.assertEqual(reports, {"r1": {"owner": "lee", "body": ""}})

if __name__ == "__main__":
    unittest.main()
