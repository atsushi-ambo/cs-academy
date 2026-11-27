def rack_labels(first, last):
    """Return a new list of labels from first through last, in order.
        Start each label with "rack-" and add the number. Use a for loop.
        first and last are integers from 0 to 50. Return [] if first > last.
        Sample: rack_labels(2, 4) -> ["rack-2", "rack-3", "rack-4"]
        Sample: rack_labels(5, 3) -> []
        Use f"rack-{number}" to put the number inside the text.
    """
    raise NotImplementedError


def batch_offsets(size, stride):
    """Return a list of offsets 0, stride, 2 * stride, and so on below size.
        An offset is a position counted from 0. Use range with three arguments.
        size is 0 to 100. stride is 1 to 20. Both are integers.
        Sample: batch_offsets(10, 4) -> [0, 4, 8]
        Sample: batch_offsets(0, 4) -> []
    """
    raise NotImplementedError


def failed_minutes(durations, failed):
    """Return the sum of durations at positions where failed is True.
        Both lists have the same length, 0 to 100. Durations are integers from 0 to 60.
        Leave both lists unchanged. Use a for loop with range.
        Sample: failed_minutes([3, 9, 6], [True, False, True]) -> 9
        A list index starts at 0. Use failed[i] to read the flag at index i.
    """
    raise NotImplementedError
