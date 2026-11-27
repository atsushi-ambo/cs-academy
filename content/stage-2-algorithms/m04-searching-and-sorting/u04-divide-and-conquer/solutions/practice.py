def peak_delay(delays):
    def peak(lo, hi):
        if hi - lo == 1:
            return delays[lo]
        mid = (lo + hi) // 2
        left = peak(lo, mid)
        right = peak(mid, hi)
        if left > right:
            return left
        return right

    if not delays:
        return None
    return peak(0, len(delays))


def fast_power(base, exponent):
    if exponent == 0:
        return 1
    half = fast_power(base, exponent // 2)
    result = half * half
    if exponent % 2 == 1:
        result *= base
    return result


def count_inversions(values):
    def solve(lo, hi):
        if hi - lo <= 1:
            return values[lo:hi], 0
        mid = (lo + hi) // 2
        left, left_count = solve(lo, mid)
        right, right_count = solve(mid, hi)
        count = left_count + right_count
        merged = []
        i, j = 0, 0
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                count += len(left) - i
                j += 1
        return merged + left[i:] + right[j:], count

    _, count = solve(0, len(values))
    return count
