import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "exercises"))
import practice


class Sign(unittest.TestCase):
    def test_contract(self):
        from hmac import digest

        for key, body in ((b"k", b""), (b"k", b"up"), (b"k2", b"up"), (b"k", b"up\x00")):
            self.assertEqual(practice.sign(key, body), (body, digest(key, body, "sha256")))
        self.assertEqual(practice.sign(b"k", b"up"), practice.sign(b"k", b"up"))


class VerifyTag(unittest.TestCase):
    def test_contract(self):
        import hmac
        from unittest.mock import patch

        key, body = b"toy", b"up"
        tag = hmac.digest(key, body, "sha256")
        with patch("hmac.compare_digest", wraps=hmac.compare_digest) as compare:
            self.assertIs(practice.verify_tag(key, body, tag), True)
            compare.assert_called_once_with(tag, tag)
        self.assertIs(practice.verify_tag(key, b"up ", tag), False)
        self.assertIs(practice.verify_tag(b"other", body, tag), False)
        self.assertIs(practice.verify_tag(key, b"", hmac.digest(key, b"", "sha256")), True)
        for bad in (None, b"", tag[:1], tag + b"x"):
            self.assertIs(practice.verify_tag(key, body, bad), False)


class AcceptEvent(unittest.TestCase):
    def test_contract(self):
        from hmac import compare_digest, digest
        from unittest.mock import Mock

        def verify(secret, body, tag):
            return compare_digest(digest(secret, body, "sha256"), tag)

        keys = {"v1": (b"a", 10), "v2": (b"b", 20)}
        tag = digest(b"a", b"up", "sha256")
        check = Mock(side_effect=verify)
        self.assertIs(practice.accept_event(keys, "v1", 9, b"up", tag, check), True)
        self.assertIs(practice.accept_event(keys, "v2", 9, b"up", tag, check), False)
        check.reset_mock()
        self.assertIs(practice.accept_event(keys, "v1", 10, b"up", tag, check), False)
        self.assertIs(practice.accept_event({}, "v1", 9, b"up", tag, check), False)
        self.assertIs(practice.accept_event(keys, "", 9, b"up", tag, check), False)
        check.assert_not_called()
        self.assertEqual(keys, {"v1": (b"a", 10), "v2": (b"b", 20)})

if __name__ == "__main__":
    unittest.main()
