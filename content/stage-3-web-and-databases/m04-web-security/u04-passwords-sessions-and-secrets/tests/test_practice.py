import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "exercises"))
import practice


class Register(unittest.TestCase):
    def test_contract(self):
        from hashlib import scrypt
        from unittest.mock import patch

        with patch("secrets.token_bytes", side_effect=[b"a" * 16, b"b" * 16]) as source:
            a = practice.register("雪", 1024)
            b = practice.register("雪", 1024)
            self.assertEqual(source.call_count, 2)
        for record, salt in ((a, b"a" * 16), (b, b"b" * 16)):
            self.assertEqual(record, {"algorithm": "scrypt", "n": 1024, "r": 8, "p": 1, "salt": salt,
                                      "digest": scrypt("雪".encode("utf-8"), salt=salt, n=1024,
                                                       r=8, p=1, dklen=32)})
        self.assertNotEqual(a["digest"], b["digest"])
        self.assertEqual(practice.register("m", 2048)["n"], 2048)


class Verify(unittest.TestCase):
    def test_contract(self):
        from hashlib import scrypt
        from hmac import compare_digest
        from unittest.mock import patch

        salt = b"x" * 16
        for n in (1024, 2048):
            digest = scrypt(b"demo", salt=salt, n=n, r=8, p=1, dklen=32)
            record = {"algorithm": "scrypt", "n": n, "r": 8, "p": 1, "salt": salt, "digest": digest}
            before = record.copy()
            with patch("hmac.compare_digest", wraps=compare_digest) as compare:
                self.assertIs(practice.verify("demo", record), True)
                compare.assert_called_once_with(digest, digest)
            self.assertIs(practice.verify("wrong", record), False)
            self.assertIs(practice.verify("", record), False)
            self.assertEqual(record, before)
        with patch("hashlib.scrypt") as derive:
            for changes in ({"n": 2**30}, {"n": 2048.0}, {"r": 2}, {"p": True},
                            {"digest": b""}, {"salt": "invalid"}, {"algorithm": "unknown"}):
                self.assertIs(practice.verify("demo", dict(record, **changes)), False)
            self.assertIs(practice.verify("demo", {}), False)
            derive.assert_not_called()


class Login(unittest.TestCase):
    def test_contract(self):
        from unittest.mock import Mock

        old = {"n": 1024, "salt": b"old"}
        new = {"n": 2048, "salt": b"new"}
        records = {"lee": old, "kai": old.copy()}
        verify = Mock(return_value=False)
        register = Mock(return_value=new)
        self.assertIs(practice.login(records, "missing", "demo", 2048, verify, register), False)
        verify.assert_not_called()
        self.assertIs(practice.login(records, "lee", "wrong", 2048, verify, register), False)
        verify.assert_called_once_with("wrong", old)
        register.assert_not_called()
        self.assertIs(records["lee"], old)
        verify.return_value = True
        self.assertIs(practice.login(records, "lee", "demo", 2048, verify, register), True)
        register.assert_called_once_with("demo", 2048)
        self.assertIs(records["lee"], new)
        self.assertEqual(records["kai"], {"n": 1024, "salt": b"old"})
        self.assertEqual(old, {"n": 1024, "salt": b"old"})
        self.assertIs(practice.login(records, "lee", "demo", 2048, verify, register), True)
        register.assert_called_once()

if __name__ == "__main__":
    unittest.main()
