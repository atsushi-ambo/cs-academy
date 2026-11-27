import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "exercises"))
import practice


class Audit(unittest.TestCase):
    def test_contract(self):
        clean = {"password_mode": "salted-kdf", "key_in_repo": False, "checks_owner": True,
                 "patched": True, "broad_access": False, "logs_secrets": False}
        self.assertEqual(practice.audit(clean), [])
        checks = [("password_mode", "fast-hash", "password"), ("key_in_repo", True, "repo-key"),
                  ("checks_owner", False, "authorization"), ("patched", False, "dependency"),
                  ("broad_access", True, "permissions"), ("logs_secrets", True, "logging")]
        mixed = clean.copy()
        for key, value, issue in checks:
            config = dict(clean, **{key: value})
            before = config.copy()
            self.assertEqual(practice.audit(config), [issue])
            self.assertEqual(config, before)
            mixed[key] = value
        self.assertEqual(practice.audit(mixed), [issue for _, _, issue in checks])
        self.assertEqual(practice.audit(dict(clean, password_mode="plaintext")), ["password"])


class DenialAlert(unittest.TestCase):
    def test_contract(self):
        events = [{"decision": "denied"}, {"decision": "allowed"}, {"decision": "denied"}]
        before = [event.copy() for event in events]
        self.assertIs(practice.denial_alert([], 1), False)
        self.assertIs(practice.denial_alert(events, 1), True)
        self.assertIs(practice.denial_alert(events, 2), True)
        self.assertIs(practice.denial_alert(events, 3), False)
        self.assertIs(practice.denial_alert(events[1:2], 1), False)
        self.assertEqual(events, before)


class ExportTitle(unittest.TestCase):
    def test_contract(self):
        log = []
        reports = {"r1": {"owner": "lee", "title": "", "internal": "private-toy"}}
        grants = {("read", "reports")}
        self.assertEqual(practice.export_title("lee", reports, "r1", grants, "a", log), "")
        for actor, report, roles in (("kai", "r1", grants), (None, "r1", grants),
                                    ("lee", "missing", grants), ("lee", "r1", set()),
                                    ("lee", "r1", {("read", "accounts")})):
            self.assertIsNone(practice.export_title(actor, reports, report, roles, "b", log))
        self.assertEqual(log, [{"request_id": "a", "decision": "allowed"}]
                         + [{"request_id": "b", "decision": "denied"}] * 5)
        self.assertEqual(reports, {"r1": {"owner": "lee", "title": "", "internal": "private-toy"}})
        self.assertEqual(grants, {("read", "reports")})

    def test_returns_title_and_logs_request(self):
        log = []
        reports = {"r1": {"owner": "lee", "title": "", "internal": "x"},
                   "r2": {"owner": "lee", "title": "Quarterly uptime", "internal": "y"},
                   "r3": {"owner": "kai", "title": "Other", "internal": "z"}}
        grants = {("read", "reports"), ("read", "accounts")}
        self.assertEqual(practice.export_title("lee", reports, "r2", grants, "req-9", log), "Quarterly uptime")
        self.assertEqual(log, [{"request_id": "req-9", "decision": "allowed"}])
        self.assertEqual(practice.export_title("lee", reports, "r1", grants, "req-10", log), "")
        self.assertIsNone(practice.export_title("lee", reports, "r3", grants, "req-11", log))
        self.assertEqual(practice.export_title("kai", reports, "r3", grants, "req-12", log), "Other")
        self.assertEqual(log, [{"request_id": "req-9", "decision": "allowed"},
                               {"request_id": "req-10", "decision": "allowed"},
                               {"request_id": "req-11", "decision": "denied"},
                               {"request_id": "req-12", "decision": "allowed"}])
        self.assertEqual(reports["r2"], {"owner": "lee", "title": "Quarterly uptime", "internal": "y"})

if __name__ == "__main__":
    unittest.main()
