def sign(key, body):
    from hmac import digest

    return body, digest(key, body, "sha256")


def verify_tag(key, body, tag):
    from hmac import compare_digest, digest

    if tag is None or len(tag) != 32:
        return False
    return compare_digest(digest(key, body, "sha256"), tag)


def accept_event(keys, kid, now, body, tag, check):
    record = keys.get(kid)
    if record is None or now >= record[1]:
        return False
    return check(record[0], body, tag)
