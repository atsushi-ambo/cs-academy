def error_count(codes):
    count = 0
    for code in codes:
        if 500 <= code <= 599:
            count += 1
    return count


def first_recovery(codes):
    for i in range(len(codes)):
        if codes[i] == 200:
            return i
    return -1


def large_files(folders, limit):
    count = 0
    for sizes in folders:
        for size in sizes:
            if size >= limit:
                count += 1
    return count
