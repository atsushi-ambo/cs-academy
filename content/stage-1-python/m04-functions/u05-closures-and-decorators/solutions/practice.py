def make_total(start):
    total = start

    def add(delta):
        nonlocal total
        total += delta
        return total

    return add


def timed(fn, clock, sink):
    from functools import wraps

    @wraps(fn)
    def wrapper(*args, **kwargs):
        start = clock()
        result = fn(*args, **kwargs)
        sink(clock() - start)
        return result

    return wrapper


def retry_with_log(fn, attempts, sink):
    from functools import wraps

    @wraps(fn)
    def wrapper(*args, **kwargs):
        for number in range(1, attempts + 1):
            sink(number)
            result = fn(*args, **kwargs)
            if result is not None:
                return result
        return None

    return wrapper
