def sift_down_max(values, i, end):
    """
    Repair the max-heap prefix in place. Index i is valid inside the prefix of length
    end. Its child subtrees are already max-heaps. Return None, keep values[end:]
    unchanged, and use no sort or heap library. Sifting [1, 7, 5, 2, 4, 12] at 0 with end
    = 5 yields [7, 4, 5, 2, 1, 12].
    """
    while 2*i + 1 < end:
        child = 2*i + 1
        right = child + 1
        if right < end and values[right] > values[child]:
            child = right
        if values[i] >= values[child]:
            break
        values[i], values[child] = values[child], values[i]
        i = child


def move_max(values, end, sift_down_max):
    """
    Given a max-heap prefix of an integer list with 2 <= end <= len(values), put its
    maximum at end - 1. Repair the remaining prefix with the given sift_down_max(values,
    i, end). Work in place and return the new end. For [9, 6, 4, 2, 12] and end = 4,
    return 3 and leave [6, 2, 4, 9, 12].
    """
    end -= 1
    values[0], values[end] = values[end], values[0]
    sift_down_max(values, 0, end)
    return end


def heap_sort(values):
    """
    Sort an integer list in ascending order in its original list and return None. Use the
    given local sift_down_max helper. Build the heap, then shrink it until one item
    remains. Use no extra list, sort, or heap library. [4, -1, 4, 0] becomes [-1, 0, 4,
    4].
    """
    def sift_down_max(values, i, end):
        while 2*i + 1 < end:
            child = 2*i + 1
            right = child + 1
            if right < end and values[right] > values[child]:
                child = right
            if values[i] >= values[child]:
                break
            values[i], values[child] = values[child], values[i]
            i = child

    end = len(values)
    for i in range(end // 2 - 1, -1, -1):
        sift_down_max(values, i, end)
    while end > 1:
        end -= 1
        values[0], values[end] = values[end], values[0]
        sift_down_max(values, 0, end)
