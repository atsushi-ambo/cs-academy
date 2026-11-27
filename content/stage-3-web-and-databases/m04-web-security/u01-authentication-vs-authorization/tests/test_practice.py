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

    def test_input_order_and_duplicates_with_distinct_ids(self):
        reports = [{"id": "z"}, {"id": "c"}, {"id": "x"}, {"id": "c"}, {"id": "m"}]
        result = practice.visible_ids("kai", reports, lambda actor, action, report: report["id"] != "x")
        self.assertEqual(result, ["z", "c", "c", "m"])

    def test_policy_is_called_with_actor_action_and_report(self):
        reports = [{"id": "r1", "owner": "kai"}, {"id": "r2", "owner": "lee"}]
        calls = []

        def allowed(actor, action, report):
            calls.append((actor, action, report["id"]))
            return report["owner"] == "lee"

        self.assertEqual(practice.visible_ids("kai", reports, allowed), ["r2"])
        self.assertEqual(calls, [("kai", "read", "r1"), ("kai", "read", "r2")])

    def test_policy_decides_not_ownership(self):
        reports = [{"id": "r1", "owner": "lee"}, {"id": "r2", "owner": "kai"}]
        deny_owner = lambda actor, action, report: report["owner"] != actor
        self.assertEqual(practice.visible_ids("lee", reports, deny_owner), ["r2"])


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

    def test_policy_permits_non_owner_and_denies_owner(self):
        sessions = {"s1": {"id": "lee"}, "s2": {"id": "kai"}}
        reports = {"r1": {"owner": "lee", "body": "secret"}, "r2": {"owner": "kai", "body": "other"}}
        seen = []

        def allowed(user, action, report):
            seen.append((user["id"], action, report["body"]))
            return report["body"] == "other"

        self.assertEqual(practice.report_body(sessions, reports, "s2", "r2", allowed), "other")
        self.assertEqual(seen, [("kai", "read", "other")])
        self.assertEqual(practice.report_body(sessions, reports, "s1", "r2", allowed), "other")
        self.assertIsNone(practice.report_body(sessions, reports, "s1", "r1", allowed))
        self.assertIsNone(practice.report_body(sessions, reports, "s1", "missing", allowed))
        self.assertEqual(seen[-2:], [("lee", "read", "other"), ("lee", "read", "secret")])

    def test_body_is_returned_only_after_policy(self):
        sessions = {"s1": {"id": "lee"}}
        reports = {"r1": {"owner": "lee", "body": "x"}}
        self.assertIsNone(practice.report_body(sessions, reports, "s1", "r1", lambda *a: False))
        self.assertEqual(practice.report_body(sessions, reports, "s1", "r1", lambda *a: True), "x")


if __name__ == "__main__":
    unittest.main()
