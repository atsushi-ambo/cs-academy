def last_and_first(items):
    if not items:
        return []
    return [items[-1], items[0]]


def slow_servers(servers, response_ms, limit_ms):
    if len(servers) != len(response_ms):
        raise ValueError("servers and response_ms must have the same length")
    slow = []
    for server, ms in zip(servers, response_ms):
        if ms > limit_ms:
            slow.append(server)
    return slow


def without_duplicates(items):
    result = []
    for item in items:
        if item not in result:
            result.append(item)
    return result


def moving_window_max(values, size):
    if size < 1 or size > len(values):
        return []
    maxima = []
    for start in range(len(values) - size + 1):
        maxima.append(max(values[start:start + size]))
    return maxima
