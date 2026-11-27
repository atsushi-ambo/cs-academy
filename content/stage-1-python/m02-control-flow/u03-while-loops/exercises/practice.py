def chunks_that_fit(free, chunk):
    """Return how many whole chunks fit in free space. Use a while loop.
        free is an integer from 0 to 500. chunk is an integer from 1 to 500.
        Sample: chunks_that_fit(14, 4) -> 3
        Sample: chunks_that_fit(4, 4) -> 1
    """
    raise NotImplementedError


def checks_used(codes, limit):
    """Return how many checks were used, including the first 200 if found.
        Stop at 200, the end of codes, or limit checks. Use while.
        codes holds up to 100 integers. limit is an integer from 0 to 100.
        Leave codes unchanged. Sample: checks_used([503, 200, 503], 3) -> 2
        Sample: checks_used([503, 200], 1) -> 1
    """
    raise NotImplementedError


def rounds_to_drain(pending, per_round):
    """Return how many rounds empty the queue. Each round processes
        per_round jobs, or all jobs left if fewer remain. Use while.
        pending is an integer from 0 to 500. per_round is from 1 to 500.
        Sample: rounds_to_drain(7, 3) -> 3
        Sample: rounds_to_drain(0, 3) -> 0
    """
    raise NotImplementedError
