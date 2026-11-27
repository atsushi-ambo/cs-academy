def peak_delay(delays):
    """Return the largest value in a list of 0 to 1024 integers.
    Return None when delays is empty. Leave delays unchanged.
    Split the list into two nonempty halves until each has one value.
    Use recursion. Compare the two answers after each split.
    For example, peak_delay([-8, -3, -6]) -> -3
              peak_delay([]) -> None
    """
    raise NotImplementedError


def fast_power(base, exponent):
    """Return base raised to exponent, including 1 for exponent 0.
    base is an integer from -9 to 9. exponent is an integer from 0 to 10000.
    Use recursion and multiplication. Compute each smaller power once.
    Do not use ** or pow().
    For example, fast_power(-2, 3) -> -8
              fast_power(5, 0) -> 1
    """
    raise NotImplementedError


def count_inversions(values):
    """Return the inversion count for a list of 0 to 2048 integers.
    An inversion is i < j and values[i] > values[j]. Keep values unchanged.
    Use recursion on halves. Count cross pairs while merging their sorted values.
    Do not use sorted() or list.sort().
    For example, count_inversions([7, 3, 3, 5]) -> 3
              count_inversions([3, 2, 1]) -> 3
    """
    raise NotImplementedError
