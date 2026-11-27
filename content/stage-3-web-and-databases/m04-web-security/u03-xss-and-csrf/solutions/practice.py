def label_span(label, hint):
    from html import escape

    return '<span title="' + escape(hint, quote=True) + '">' + escape(label) + "</span>"


def form_cookie(sid):
    from http.cookies import SimpleCookie

    cookie = SimpleCookie()
    cookie["sid"] = sid
    cookie["sid"]["samesite"] = "Strict"
    return cookie["sid"].OutputString()


def save_theme(settings, sessions, request, check):
    if request["method"] != "POST" or request["theme"] not in ("light", "dark"):
        return False
    sid = request["sid"]
    if not check(sessions, sid, request["token"]):
        return False
    settings[sid] = request["theme"]
    return True
