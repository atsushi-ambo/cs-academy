def valid_target(port, label, mode):
    return (type(port) is int and 1 <= port <= 65535
            and isinstance(label, str) and 1 <= len(label) <= 30
            and isinstance(mode, str) and mode in ("brief", "full"))


def report_path(root, name):
    from pathlib import Path

    if not name or Path(name).is_absolute():
        return None
    try:
        base = root.resolve(strict=True)
        candidate = (base / name).resolve(strict=True)
    except (OSError, RuntimeError, ValueError):
        return None
    if base not in candidate.parents:
        return None
    return candidate


def edit_label(user_id, profile, body):
    if user_id is None or user_id != profile["id"]:
        return None
    if len(body) != 1 or "label" not in body:
        return None
    label = body["label"]
    if not isinstance(label, str) or not 1 <= len(label) <= 30:
        return None
    result = profile.copy()
    result["label"] = label
    return result
