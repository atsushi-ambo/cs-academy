def rack_labels(first, last):
    labels = []
    for number in range(first, last + 1):
        labels.append(f"rack-{number}")
    return labels


def batch_offsets(size, stride):
    return list(range(0, size, stride))


def failed_minutes(durations, failed):
    total = 0
    for i in range(len(durations)):
        if failed[i]:
            total += durations[i]
    return total
