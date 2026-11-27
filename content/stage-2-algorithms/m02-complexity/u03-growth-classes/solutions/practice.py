def half_path(size):
    """Return the number of times you can halve size with // 2 before it is 1.
    Use one recursive call per step, with no loops.
    Input: an integer from 1 to 1,000,000.
    Sample: half_path(18) -> 4
    """
    if size == 1:
        return 0
    return 1 + half_path(size // 2)


def order_count(n):
    """Return n! with one loop over the factors. Do not use a factorial helper.
    Input: an integer from 0 to 12.
    Sample: order_count(4) -> 24
    """
    total = 1
    for choices in range(1, n + 1):
        total *= choices
    return total


def triple_checks(n):
    """Return the number of ways to pick one slot for each of three roles. Each role can use any slot.
    Input: n, an integer from 0 to 500. Return the count by multiplication, without enumerating the triples.
    Sample: triple_checks(4) -> 64
    """
    return n * n * n
