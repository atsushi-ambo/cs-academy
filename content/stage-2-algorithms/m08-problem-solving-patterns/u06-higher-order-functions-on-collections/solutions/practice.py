def my_map(rule, items):
    result = []
    for item in items:
        result.append(rule(item))
    return result


def my_filter(keep, items):
    result = []
    for item in items:
        if keep(item):
            result.append(item)
    return result


def my_reduce(combine, items, initial):
    result = initial
    for item in items:
        result = combine(result, item)
    return result


def incident_report(logs):
    from functools import reduce

    errors = [row for row in logs if 500 <= row[1] <= 599]
    delays = map(lambda row: row[2], errors)
    total = reduce(lambda value, delay: value + delay, delays, 0)
    ordered = sorted(errors, key=lambda row: (-row[2], row[0]))
    return (total, ordered)
