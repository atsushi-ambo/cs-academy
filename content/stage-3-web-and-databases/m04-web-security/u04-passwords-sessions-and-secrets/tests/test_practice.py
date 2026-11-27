import hashlib
import hmac
import secrets
import sys
import unittest
from contextlib import ExitStack, contextmanager
from pathlib import Path
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "exercises"))
import practice


@contextmanager
def replaced(owner, name, replacement):
    original = getattr(owner, name)
    with ExitStack() as stack:
        stack.enter_context(patch.object(owner, name, replacement))
        for key, value in list(vars(practice).items()):
            if value is original:
                stack.enter_context(patch.object(practice, key, replacement))
        yield replacement


class Register(unittest.TestCase):
    def test_contract(self):
        from hashlib import scrypt

        source = Mock(side_effect=[b"a" * 16, b"b" * 16])
        with replaced(secrets, "token_bytes", source):
            a = practice.register("雪", 1024)
            b = practice.register("雪", 1024)
        self.assertEqual(source.call_count, 2)
        self.assertTrue(all(call.args == (16,) or call.kwargs == {"nbytes": 16}
                            for call in source.call_args_list))
        for record, salt in ((a, b"a" * 16), (b, b"b" * 16)):
            self.assertEqual(record, {"algorithm": "scrypt", "n": 1024, "r": 8, "p": 1, "salt": salt,
                                      "digest": scrypt("雪".encode("utf-8"), salt=salt, n=1024,
                                                       r=8, p=1, dklen=32)})
        self.assertNotEqual(a["digest"], b["digest"])
        self.assertEqual(practice.register("m", 2048)["n"], 2048)

    def test_real_salts_differ(self):
        first = practice.register("same", 1024)
        second = practice.register("same", 1024)
        self.assertEqual(len(first["salt"]), 16)
        self.assertNotEqual(first["salt"], second["salt"])
        self.assertNotEqual(first["digest"], second["digest"])


class Verify(unittest.TestCase):
    def test_contract(self):
        from hashlib import scrypt

        salt = b"x" * 16
        for n in (1024, 2048):
            digest = scrypt(b"demo", salt=salt, n=n, r=8, p=1, dklen=32)
            record = {"algorithm": "scrypt", "n": n, "r": 8, "p": 1, "salt": salt, "digest": digest}
            before = record.copy()
            compare = Mock(wraps=hmac.compare_digest)
            with replaced(hmac, "compare_digest", compare):
                self.assertIs(practice.verify("demo", record), True)
            compare.assert_called_once_with(digest, digest)
            wrong = scrypt(b"wrong", salt=salt, n=n, r=8, p=1, dklen=32)
            compare = Mock(wraps=hmac.compare_digest)
            with replaced(hmac, "compare_digest", compare):
                self.assertIs(practice.verify("wrong", record), False)
            compare.assert_called_once_with(wrong, digest)
            self.assertIs(practice.verify("", record), False)
            self.assertEqual(record, before)
        derive = Mock()
        with replaced(hashlib, "scrypt", derive):
            for changes in ({"n": 2**30}, {"n": 2048.0}, {"r": 2}, {"p": True},
                            {"digest": b""}, {"salt": "invalid"}, {"algorithm": "unknown"}):
                self.assertIs(practice.verify("demo", dict(record, **changes)), False)
            self.assertIs(practice.verify("demo", {}), False)
        derive.assert_not_called()


class Login(unittest.TestCase):
    def test_contract(self):
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

    def test_never_replaces_with_a_weaker_profile(self):
        strong = {"n": 2048, "salt": b"strong"}
        records = {"lee": strong}
        verify = Mock(return_value=True)
        register = Mock(return_value={"n": 1024, "salt": b"weak"})
        self.assertIs(practice.login(records, "lee", "demo", 1024, verify, register), True)
        register.assert_not_called()
        self.assertIs(records["lee"], strong)
        self.assertEqual(strong, {"n": 2048, "salt": b"strong"})

    def test_equal_profile_is_kept(self):
        same = {"n": 1024, "salt": b"same"}
        records = {"lee": same}
        register = Mock(return_value={"n": 1024, "salt": b"fresh"})
        self.assertIs(practice.login(records, "lee", "demo", 1024, Mock(return_value=True), register), True)
        register.assert_not_called()
        self.assertIs(records["lee"], same)

if __name__ == "__main__":
    unittest.main()
