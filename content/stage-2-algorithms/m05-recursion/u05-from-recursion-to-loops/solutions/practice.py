def reduced_price(cents, weeks):
    while weeks > 0:
        cents = cents * 9 // 10
        weeks -= 1
    return cents


def unpack_sizes(batch):
    pending = [batch]
    result = []
    while pending:
        item = pending.pop()
        if isinstance(item, list):
            for child in reversed(item):
                pending.append(child)
        else:
            result.append(item)
    return result


def route_count(n):
    older, newer = 1, 1
    for step in range(2, n + 1):
        older, newer = newer, older + newer
    return newer
