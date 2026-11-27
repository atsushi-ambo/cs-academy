def service_groups(services):
    """Return all subsets of services, including the empty subset.
    services holds 0 to 8 distinct strings. Keep it unchanged.
    Keep the input order within each subset. Result order can vary.
    Use recursion. Build the choices yourself without itertools or other helpers
    that generate combinations for you.
    For example, service_groups(["api"]) -> [[], ["api"]]
              service_groups([]) -> [[]]
    """
    raise NotImplementedError


def job_orders(jobs):
    """Return every order of jobs exactly once. Return one empty order for [].
    jobs contains 0 to 7 distinct strings. Keep jobs unchanged.
    The orders can appear in any sequence. Use recursion and undo your choices.
    Do not call a library function that generates permutations for you.
    For example, job_orders(["db", "api"]) -> [["db", "api"], ["api", "db"]]
    """
    raise NotImplementedError


def count_boards(n):
    """Return the number of ways to place n queens on an n by n board.
    n is an integer from 0 to 8. No two queens share a row, column, or diagonal.
    Count rotations and mirror images separately if their positions differ.
    The empty board counts once. Use recursion and skip conflicts before recursing.
    For example, count_boards(0) -> 1
              count_boards(4) -> 2
    """
    raise NotImplementedError
