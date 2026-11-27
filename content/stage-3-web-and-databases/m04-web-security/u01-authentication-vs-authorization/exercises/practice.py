def authorize(user, action, resource):
    raise NotImplementedError


def visible_ids(actor, reports, allowed):
    raise NotImplementedError


def report_body(sessions, reports, key, report_id, allowed):
    raise NotImplementedError
