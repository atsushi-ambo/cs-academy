def count_large(values, limit):
    """Return how many values are greater than limit. Use one pass and a running count.
    Inputs: 0 to 200 integers and an integer limit. Leave the list unchanged.
    Use a loop with comparison and counting. Do not build another collection or use a helper.
    Sample: count_large([3, 8, 5, 8], 5) -> 2
    """
    count = 0
    for value in values:
        if value > limit:
            count += 1
    return count


def above_zero(values):
    """Return a new list with True for each value above zero and False for each other value.
    Inputs: 0 to 200 integers. Keep the input unchanged. Append each result to the output list.
    Sample: above_zero([2, 0, -3]) -> [True, False, False]
    """
    flags = []
    for value in values:
        flags.append(value > 0)
    return flags


def peak_open(changes):
    """Read changes to the number of open requests. A 1 opens one and a -1 closes one.
    Return the largest number open at once. The count starts at zero and never goes below zero.
    Inputs: 0 to 200 changes. Track the current and biggest counts in one pass. Do not save past counts.
    Sample: peak_open([1, 1, -1, 1, -1, -1]) -> 2
    """
    current = 0
    peak = 0
    for change in changes:
        current += change
        if current > peak:
            peak = current
    return peak
