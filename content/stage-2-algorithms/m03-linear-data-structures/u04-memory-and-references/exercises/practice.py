def same_list(a, b):
    """Return True only if the inputs are the same list object. Use is.
    Inputs: two lists of up to 100 integers. Do not change either list.
    Sample: with a = [4], same_list(a, a) -> True and same_list(a, [4]) -> False
    """
    raise NotImplementedError


def blank_grid(rows, cols):
    """Return rows lists, each with cols zeros. A change in one row must leave the others alone.
    Inputs: both sizes are integers from 0 to 20.
    Sample: blank_grid(2, 3) -> [[0, 0, 0], [0, 0, 0]]
    """
    raise NotImplementedError


def head_view(data, count):
    """Return a memoryview of the first count bytes of data. Writes through it must reach data.
    Inputs: a bytearray of length 0 to 100 and an integer count from 0 to len(data).
    Sample: for data = bytearray([5, 1, 3]), head_view(data, 2) shows [5, 1].
    """
    raise NotImplementedError
