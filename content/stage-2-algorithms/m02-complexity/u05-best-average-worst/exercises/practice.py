def checks_until_match(codes, target):
    """Return how many items you compare before you find target or run out of items.
    Inputs: 0 to 200 integers and an integer target. Stop at the first match. Leave the list unchanged.
    Sample: checks_until_match([3, 8, 3], 8) -> 2
    """
    raise NotImplementedError


def uniform_hit_cost(n):
    """Return the average number of comparisons if exactly one item matches and all n positions are equally likely.
    Input: an integer from 1 to 1,000,000. Use arithmetic without loops or a collection.
    Sample: uniform_hit_cost(4) -> 2.5
    """
    raise NotImplementedError


def batch_checks(codes, targets):
    """Scan codes from the start for each target. Stop each scan at its first match.
    Return the total comparisons. Inputs: two lists of 0 to 100 integers. Leave both unchanged.
    Sample: batch_checks([3, 8, 4], [3, 9, 8]) -> 6
    """
    raise NotImplementedError
