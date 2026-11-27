def halve_rounds(n):
    """Return how many times n can be cut down by whole-number division by two before n is 1 or less.
    Input: an integer from 0 to 1,000,000. Use a while loop and //.
    Sample: halve_rounds(12) -> 3
    """
    rounds = 0
    while n > 1:
        n //= 2
        rounds += 1
    return rounds


def planned_visits(n):
    """Return n times the number of halving levels. Input: an integer from 0 to 1,000,000.
    Use a while loop for the levels. Count n visits per level with one addition, without a loop over the items.
    Sample: planned_visits(16) -> 64
    """
    size = n
    visits = 0
    while size > 1:
        visits += n
        size //= 2
    return visits


def first_over_budget(budget):
    """Try sizes 1, 2, 4, 8, and so on until n × n is greater than budget. Return that size.
    Input: an integer budget from 0 to 10,000. Use a while loop that doubles the size.
    Sample: first_over_budget(16) -> 8
    """
    size = 1
    while size * size <= budget:
        size *= 2
    return size
