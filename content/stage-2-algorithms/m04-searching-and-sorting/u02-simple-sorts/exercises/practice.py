def selection_report(sizes):
    """Return a pair (ordered, comparisons) for 0 to 200 integer job sizes.
    Use selection sort and leave sizes unchanged. Return a new list.
    For each index, find the minimum by comparing every later item once.
    Count value comparisons. Do not use min(), sorted(), or list.sort().
    For example, selection_report([6, 3, 4]) -> ([3, 4, 6], 3)
             selection_report([]) -> ([], 0)
    """
    raise NotImplementedError


def insertion_jobs(jobs):
    """Return a new list of (priority, name) pairs in ascending priority.
    There are 0 to 200 pairs, with integer priorities and string names.
    Use insertion sort and keep ties in the input order. Leave jobs unchanged.
    Do not use sorted() or list.sort().
    For example, insertion_jobs([(5, "x"), (2, "b"), (2, "a")])
             -> [(2, "b"), (2, "a"), (5, "x")]
    """
    raise NotImplementedError


def bubble_report(values):
    """Return (ordered, comparisons) for 0 to 200 integers. Leave values unchanged.
    Use a new list. Scan adjacent pairs left to right and swap if out of order.
    After each full pass, omit its final item from the next pass.
    Stop after a pass without any swaps. Count every value comparison.
    Do not use sorted() or list.sort().
    For example, bubble_report([3, 2, 1]) -> ([1, 2, 3], 3)
             bubble_report([1, 1, 2]) -> ([1, 1, 2], 2)
    """
    raise NotImplementedError
