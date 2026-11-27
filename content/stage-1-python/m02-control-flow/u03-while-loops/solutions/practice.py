def chunks_that_fit(free, chunk):
    count = 0
    while free >= chunk:
        free -= chunk
        count += 1
    return count


def checks_used(codes, limit):
    used = 0
    while used < limit and used < len(codes):
        code = codes[used]
        used += 1
        if code == 200:
            break
    return used


def rounds_to_drain(pending, per_round):
    rounds = 0
    while pending > 0:
        pending -= per_round
        rounds += 1
    return rounds
