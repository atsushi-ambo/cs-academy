def merge_jobs(left, right):
    result = []
    i, j = 0, 0
    while i < len(left) and j < len(right):
        if left[i][0] <= right[j][0]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    return result + left[i:] + right[j:]


def merge_sort(events):
    def merge(left, right):
        result = []
        i, j = 0, 0
        while i < len(left) and j < len(right):
            if left[i][0] <= right[j][0]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        return result + left[i:] + right[j:]

    if len(events) <= 1:
        return events[:]
    mid = len(events) // 2
    left = merge_sort(events[:mid])
    right = merge_sort(events[mid:])
    return merge(left, right)


def lomuto_partition(values, lo, hi):
    pivot = values[hi]
    store = lo
    for i in range(lo, hi):
        if values[i] <= pivot:
            values[store], values[i] = values[i], values[store]
            store += 1
    values[store], values[hi] = values[hi], values[store]
    return store


def hoare_partition(values, lo, hi):
    pivot = values[lo]
    i = lo - 1
    j = hi + 1
    while True:
        i += 1
        while values[i] < pivot:
            i += 1
        j -= 1
        while values[j] > pivot:
            j -= 1
        if i >= j:
            return j
        values[i], values[j] = values[j], values[i]


def quick_sort(values):
    def partition(lo, hi):
        middle = (lo + hi) // 2
        values[middle], values[hi] = values[hi], values[middle]
        pivot = values[hi]
        store = lo
        for index in range(lo, hi):
            if values[index] <= pivot:
                values[store], values[index] = values[index], values[store]
                store += 1
        values[store], values[hi] = values[hi], values[store]
        return store

    def sort_range(lo, hi):
        if lo < hi:
            p = partition(lo, hi)
            sort_range(lo, p - 1)
            sort_range(p + 1, hi)

    sort_range(0, len(values) - 1)
