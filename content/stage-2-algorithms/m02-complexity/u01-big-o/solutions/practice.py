def shelf_checks(codes, chosen):
    """Each shelf code in a list needs one check. Returns from the chosen shelf need one extra check.
    Return the total. Use one loop over the codes. Do not use list.count.
    Inputs: 0 to 200 codes, each a short string. Do not change the list.
    Sample: shelf_checks(["A", "B", "A"], "A") -> 5
    """
    checks = 0
    for code in codes:
        checks += 1
        if code == chosen:
            checks += 1
    return checks


def pair_checks(n):
    """Return the number of pairs of different items among n items.
    Count each pair once using nested for loops and one counter.
    Input: an integer from 0 to 100.
    Sample: pair_checks(5) -> 10
    """
    pairs = 0
    for left in range(n):
        for right in range(left + 1, n):
            pairs += 1
    return pairs


def shared_shelf_pairs(returns, records):
    """Return how many pairs have the same code, with one entry from each list.
    Count each matching pair, even when a code appears more than once.
    Inputs: two lists of 0 to 40 short strings. Leave both lists unchanged.
    Sample: shared_shelf_pairs(["A", "A"], ["A", "B", "A"]) -> 4
    """
    pairs = 0
    for returned in returns:
        for record in records:
            if returned == record:
                pairs += 1
    return pairs
