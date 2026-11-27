def selection_report(sizes):
    result = sizes[:]
    checks = 0
    for start in range(len(result)):
        best = start
        for i in range(start + 1, len(result)):
            checks += 1
            if result[i] < result[best]:
                best = i
        result[start], result[best] = result[best], result[start]
    return result, checks


def insertion_jobs(jobs):
    result = jobs[:]
    for i in range(1, len(result)):
        current = result[i]
        j = i - 1
        while j >= 0 and result[j][0] > current[0]:
            result[j + 1] = result[j]
            j -= 1
        result[j + 1] = current
    return result


def bubble_report(values):
    result = values[:]
    checks = 0
    for end in range(len(result) - 1, 0, -1):
        swapped = False
        for j in range(end):
            checks += 1
            if result[j] > result[j + 1]:
                result[j], result[j + 1] = result[j + 1], result[j]
                swapped = True
        if not swapped:
            break
    return result, checks
