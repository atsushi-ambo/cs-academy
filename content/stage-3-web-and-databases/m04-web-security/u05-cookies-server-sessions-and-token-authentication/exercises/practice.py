def session_cookie(sid):
    raise NotImplementedError


def new_id(sessions, draw):
    raise NotImplementedError


def rotate(sessions, old_id, user, expires, fresh_id):
    raise NotImplementedError
