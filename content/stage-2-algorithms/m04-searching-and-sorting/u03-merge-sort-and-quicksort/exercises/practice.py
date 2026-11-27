def merge_jobs(left, right):
    """Each input is a list of 0 to 200 (integer time, string name) pairs.
    The runs are in ascending order by time. Return a new list by time.
    For equal times, keep the order within each run and take left before right.
    Leave both inputs unchanged. Merge with a linear sweep, without a library sort.
    For example, merge_jobs([(3, "b")], [(3, "a")]) -> [(3, "b"), (3, "a")]
    """
    raise NotImplementedError


def merge_sort(events):
    """Return a new list in ascending time order. Keep events unchanged.
    events contains 0 to 512 (integer time, string name) pairs.
    Use recursive merge sort with a linear, stable merge. Do not use a library sort.
    For example, merge_sort([(3, "b"), (1, "x"), (3, "a")])
             -> [(1, "x"), (3, "b"), (3, "a")]
    """
    raise NotImplementedError


def lomuto_partition(values, lo, hi):
    """Rearrange the nonempty range from lo to hi, both included, in values.
    values is a list of 1 to 256 integers. Bounds are valid.
    Use the last value in the range as pivot. Return its final index p.
    Values before p in the range must be <= pivot. Values after p must be > pivot.
    Leave the rest of values unchanged. Use a linear sweep, without a library sort.
    For example, [8, 1, 3], lo=0, hi=2 -> p=1 and values becomes [1, 3, 8].
    """
    raise NotImplementedError


def hoare_partition(values, lo, hi):
    """Partition the included range lo..hi in a list of 2 to 256 integers.
    The bounds are valid and lo < hi. Use the original first value as pivot.
    Use Hoare partition. Return a cut j with lo <= j < hi.
    Indexes lo..j hold values <= pivot and j+1..hi hold values >= pivot.
    Leave values outside the range intact. Avoid library sorts or extra lists.
    For example, [4, 9, 2, 6], lo=0, hi=3 -> j=0 and values becomes [2, 9, 4, 6].
    """
    raise NotImplementedError


def quick_sort(values):
    """Rearrange values into ascending order and return None.
    values is a list of 0 to 256 integers, with possible ties.
    Use a recursive quicksort with either partition from this unit.
    Work inside the list. Avoid full-size or per-partition list copies.
    Do not use sorted() or list.sort().
    For example, starting with [4, 1, 4, 0] leaves [0, 1, 4, 4].
    """
    raise NotImplementedError
