"""Exercises for "Lists: Keeping Many Values in Order".

In the app: write each function in the editor and press "Run tests".

On your own Mac: copy the whole unit folder, open a terminal in it, and run

    python3 -m unittest discover -s tests

Replace each `raise NotImplementedError` with your code. Use only what this
unit taught (the "start empty, loop, decide, collect" pattern).
The ">>>" lines below are examples of input and output.
"""


def last_and_first(items):
    """Return a new list [last item, first item].

    If `items` is empty, return an empty list. (Remember: an empty list is
    "false" in an if statement.)

    >>> last_and_first(["a", "b", "c"])
    ['c', 'a']
    """
    raise NotImplementedError


def slow_servers(servers, response_ms, limit_ms):
    """Return the names of servers whose response time is greater than limit_ms.

    `servers` and `response_ms` have the same length. Keep the original order.
    If the lengths are different, raise ValueError.

    >>> slow_servers(["web01", "web02"], [120, 950], 500)
    ['web02']
    """
    raise NotImplementedError


def without_duplicates(items):
    """Return a new list with duplicates removed, keeping the first occurrence.

    Do not change `items`.

    >>> without_duplicates(["web01", "db01", "web01", "cache01", "db01"])
    ['web01', 'db01', 'cache01']
    """
    raise NotImplementedError


def moving_window_max(values, size):
    """Return the maximum of every window of `size` consecutive values.

    If size is less than 1 or greater than len(values), return an empty list.
    Hint: use slices.

    >>> moving_window_max([3, 1, 4, 1, 5, 9, 2], 3)
    [4, 4, 5, 9, 9]
    """
    raise NotImplementedError
