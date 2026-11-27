def apply_each(readings, rule):
    result = []
    for reading in readings:
        result.append(rule(reading))
    return result


def slowest(logs):
    return max(logs, key=lambda row: row[1], default=None)


def incident_order(logs):
    return sorted(logs, key=lambda row: (row[0], -row[1], row[2]))
