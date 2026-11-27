def exit_log(n):
    """Return a list of numbers in the order frames close, from 0 up to n.
        Use one recursive call per non-base frame and no for or while.
        n is an integer from 0 to 100. Do not print.
        Sample: exit_log(3) -> [0, 1, 2, 3]
        Sample: exit_log(0) -> [0]
    """
    raise NotImplementedError


def loop_total(n):
    """Return n + (n - 1) + ... + 1. Use a while loop with a running total.
        Do not use recursion, sum(), or a formula. n is an integer from 0 to 10000.
        Sample: loop_total(3) -> 6
        Sample: loop_total(0) -> 0
    """
    raise NotImplementedError


def fast_power(base, n):
    """Return base to the power n. Call your function once with n // 2.
        Do not use **, pow(), or loops. base is an integer from -3 to 3.
        n is an integer from 0 to 10000. Return 1 when n is zero, even for base 0.
        Sample: fast_power(2, 5) -> 32
        Sample: fast_power(-2, 4) -> 16
    """
    raise NotImplementedError
