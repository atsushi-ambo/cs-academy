def register(password, n):
    from hashlib import scrypt
    from secrets import token_bytes

    salt = token_bytes(16)
    digest = scrypt(password.encode("utf-8"), salt=salt, n=n, r=8, p=1, dklen=32)
    return {"algorithm": "scrypt", "n": n, "r": 8, "p": 1, "salt": salt, "digest": digest}


def verify(password, record):
    from hashlib import scrypt
    from hmac import compare_digest

    n = record.get("n")
    r = record.get("r")
    p = record.get("p")
    salt = record.get("salt")
    digest = record.get("digest")
    if not password or record.get("algorithm") != "scrypt":
        return False
    if type(n) is not int or type(r) is not int or type(p) is not int:
        return False
    if (n, r, p) not in ((1024, 8, 1), (2048, 8, 1)):
        return False
    if not isinstance(salt, bytes) or len(salt) != 16:
        return False
    if not isinstance(digest, bytes) or len(digest) != 32:
        return False
    actual = scrypt(password.encode("utf-8"), salt=salt, n=n, r=r, p=p, dklen=32)
    return compare_digest(actual, digest)


def login(records, account, password, current_n, verify, register):
    record = records.get(account)
    if record is None or not verify(password, record):
        return False
    if record["n"] != current_n:
        records[account] = register(password, current_n)
    return True
