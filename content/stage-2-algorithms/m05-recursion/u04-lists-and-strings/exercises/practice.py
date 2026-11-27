def size_total(sizes, i=0):
    """Return the sum of file sizes from index i to the end. Use recursion.
        Do not slice or change sizes. It has 0 to 100 integer sizes in MB.
        Each size is 0 to 1000. i is between 0 and len(sizes), inclusive.
        Sample: size_total([4, 8, 5]) -> 17
        Sample: size_total([4, 8, 5], 1) -> 13
    """
    raise NotImplementedError


def reverse_label(label):
    """Return the characters in opposite order. Use recursion and slices.
        Do not use reversed() or a negative slice step.
        label contains 0 to 80 ASCII characters. Keep spaces and punctuation.
        Sample: reverse_label("web-8") -> "8-bew"
        Sample: reverse_label("") -> ""
    """
    raise NotImplementedError


def is_mirror(label, left=0, right=None):
    """Return True if the chosen part reads the same in both directions.
        Endpoints left and right are inclusive. When right is None, use
        len(label) - 1. When left >= right, return True. Use recursion.
        label holds 0 to 80 ASCII characters. Compare case exactly. No slices.
        Sample: is_mirror("radar") -> True
        Sample: is_mirror("xabay", 1, 3) -> True
        Assume endpoints are valid unless they mark an empty span.
    """
    raise NotImplementedError


def flatten_sizes(batch, out=None):
    """Return the integer sizes from a nested list, left to right. Use recursion.
        There are up to 200 items and lists, with nesting depth at most 30.
        Sizes are non-negative integers. Leave all input lists unchanged.
        In top calls, omit out. Inside recursion, pass the same output list.
        Sample: flatten_sizes([1, [], [2, [3]], 4]) -> [1, 2, 3, 4]
        Sample: flatten_sizes([[], []]) -> []
    """
    raise NotImplementedError
