def audit(config):
    findings = []
    if config["password_mode"] != "salted-kdf":
        findings.append("password")
    if config["key_in_repo"]:
        findings.append("repo-key")
    if not config["checks_owner"]:
        findings.append("authorization")
    if not config["patched"]:
        findings.append("dependency")
    if config["broad_access"]:
        findings.append("permissions")
    if config["logs_secrets"]:
        findings.append("logging")
    return findings


def denial_alert(events, limit):
    count = 0
    for event in events:
        if event["decision"] == "denied":
            count += 1
            if count >= limit:
                return True
    return False


def export_title(actor, reports, report_id, grants, request_id, log):
    report = reports.get(report_id)
    allowed = (("read", "reports") in grants and actor is not None
               and report is not None and report["owner"] == actor)
    decision = "allowed" if allowed else "denied"
    log.append({"request_id": request_id, "decision": decision})
    if allowed:
        return report["title"]
    return None
