def sift_up(heap, i):
    """
    Change a list of integers in place and return None. Index i is valid. Only that value
    may be too small for its parent. Use index comparisons and swaps, with no heap
    library or sort. Sift up at index 3 in [2, 7, 5, 1] to get [1, 2, 5, 7].
    """
    raise NotImplementedError


def push(heap, value, sift_up):
    """
    Append an integer to the given heap list in place and use the given sift_up(heap, i)
    to repair it. Return None. Do not use heapq or sort. Push 3 into [5, 7, 8] to get [3,
    5, 8, 7].
    """
    raise NotImplementedError


def sift_down(heap, i):
    """
    Repair the subtree at a valid index i in place, with both child subtrees already min-
    heaps. Return None. Use no heap library or sort. [10, 6, 3, 7, 9, 4] at i = 0 becomes
    [3, 6, 4, 7, 9, 10].
    """
    raise NotImplementedError


def pop_min(heap, sift_down):
    """
    For an integer heap, update the same list and return its minimum, or None for an
    empty heap. Use the given sift_down(heap, i). Use no heapq or sort. For [2, 4, 3, 7],
    return 2 and leave [3, 4, 7].
    """
    raise NotImplementedError


def heapify(heap, sift_down):
    """
    Turn an integer list into a min-heap by sifting parents from the bottom. Use the
    given sift_down(heap, i). Do not use heapq, sorting, or a second list. Return None.
    For [9, 1, 4], the list becomes [1, 9, 4].
    """
    raise NotImplementedError


def schedule(jobs):
    """
    Use heapq to return job names from a list of (integer priority, name) pairs. Smaller
    priorities run first. Equal priorities follow arrival order. Keep the input
    unchanged, and keep repeat names. [(2, "log"), (1, "alert"), (2, "sync")] becomes
    ["alert", "log", "sync"].
    """
    raise NotImplementedError
