def exit_log(n):
    if n == 0:
        return [0]
    log = exit_log(n - 1)
    log.append(n)
    return log


def loop_total(n):
    total = 0
    while n > 0:
        total += n
        n -= 1
    return total


def fast_power(base, n):
    if n == 0:
        return 1
    half = fast_power(base, n // 2)
    square = half * half
    if n % 2 == 1:
        return square * base
    return square
