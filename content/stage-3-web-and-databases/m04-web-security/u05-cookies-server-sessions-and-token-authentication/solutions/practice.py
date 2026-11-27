def session_cookie(sid):
    from http.cookies import SimpleCookie

    cookie = SimpleCookie()
    cookie["sid"] = sid
    morsel = cookie["sid"]
    morsel["httponly"] = True
    morsel["secure"] = True
    morsel["samesite"] = "Lax"
    morsel["path"] = "/"
    return morsel.OutputString()


def new_id(sessions, draw):
    candidate = draw()
    while candidate in sessions:
        candidate = draw()
    return candidate


def rotate(sessions, old_id, user, expires, fresh_id):
    taken = dict(sessions)
    taken[old_id] = None
    sid = fresh_id(taken)
    sessions.pop(old_id, None)
    sessions[sid] = (user, expires)
    return sid
