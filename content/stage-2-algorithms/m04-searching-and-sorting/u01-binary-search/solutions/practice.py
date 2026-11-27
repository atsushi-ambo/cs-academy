def find_time(times, target):
    lo = 0
    hi = len(times) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        value = times[mid]
        if value == target:
            return mid
        if value < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1


def first_at_least(times, limit):
    lo = 0
    hi = len(times)
    while lo < hi:
        mid = (lo + hi) // 2
        if times[mid] < limit:
            lo = mid + 1
        else:
            hi = mid
    return lo


def smallest_capacity(sizes, days):
    if not sizes:
        return 0

    lo = 0
    hi = 0
    for size in sizes:
        if size > lo:
            lo = size
        hi += size

    while lo < hi:
        mid = (lo + hi) // 2
        needed = 1
        used = 0
        for size in sizes:
            if used + size > mid:
                needed += 1
                used = 0
            used += size
        if needed <= days:
            hi = mid
        else:
            lo = mid + 1
    return lo
