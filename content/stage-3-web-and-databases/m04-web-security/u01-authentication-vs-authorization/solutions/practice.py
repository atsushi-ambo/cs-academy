def authorize(user, action, resource):
    if user is None or resource is None:
        return False
    if user["org"] != resource["org"] or user["role"] not in ("member", "admin"):
        return False
    is_owner = user["id"] == resource["owner"]
    if action == "read":
        return is_owner or user["role"] == "admin"
    if action == "edit":
        return is_owner
    return False


def visible_ids(actor, reports, allowed):
    result = []
    for report in reports:
        if allowed(actor, "read", report):
            result.append(report["id"])
    return result


def report_body(sessions, reports, key, report_id, allowed):
    if not key:
        return None
    user = sessions.get(key)
    report = reports.get(report_id)
    if user is None or report is None or not allowed(user, "read", report):
        return None
    return report["body"]
