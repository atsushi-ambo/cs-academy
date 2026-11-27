def find_time(times, target):
    """Return any index with the target time, or -1 if absent.
    times is a list of 0 to 4096 integers in nondecreasing order.
    It can contain repeats. Keep the input unchanged.
    Use an iterative binary search. Do not use bisect or a linear search.
    For example, find_time([2, 6, 9], 9) -> 2
              find_time([2, 2], 3) -> -1
    """
    raise NotImplementedError


def first_at_least(times, limit):
    """Return the first index i such that times[i] >= limit.
    If there is no such value, return len(times).
    times is a list of 0 to 4096 integers in nondecreasing order.
    Use an iterative binary search without bisect. Keep times unchanged.
    For example, first_at_least([1, 5, 5, 8], 5) -> 1
              first_at_least([1, 5], 9) -> 2
    """
    raise NotImplementedError


def smallest_capacity(sizes, days):
    """Return the smallest integer capacity that sends all files in at most days days.
    Send the files in order. A file cannot be split.
    sizes contains 0 to 100 positive integers, each at most 10**9.
    days is an integer from 1 to 100. Return 0 for an empty list.
    Keep sizes unchanged. Use binary search on capacities. Do not use bisect.
    For example, smallest_capacity([4, 3, 2], 2) -> 5
              smallest_capacity([4, 3, 2], 1) -> 9
    """
    raise NotImplementedError
