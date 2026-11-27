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
    sid = fresh_id(sessions)
    sessions.pop(old_id, None)
    sessions[sid] = (user, expires)
    return sid
