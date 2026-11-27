def sign(key, body):
    raise NotImplementedError


def verify_tag(key, body, tag):
    raise NotImplementedError


def accept_event(keys, kid, now, body, tag, check):
    raise NotImplementedError
