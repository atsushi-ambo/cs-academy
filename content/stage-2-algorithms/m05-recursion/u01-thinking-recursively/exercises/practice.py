def batch_pages(n):
    """Return n + (n - 1) + ... + 1. Use recursion with no loop or sum().
        n is an integer from 0 to 100. At zero, return 0.
        Sample: batch_pages(4) -> 10
        Sample: batch_pages(0) -> 0
    """
    raise NotImplementedError


def job_orders(n):
    """Return the number of orders for n different jobs. The first job
        has n choices. Each choice leaves n - 1 jobs. Use recursion.
        n is an integer from 0 to 12. The empty order counts as one.
        Sample: job_orders(3) -> 6
        Sample: job_orders(0) -> 1
    """
    raise NotImplementedError


def stair_routes(n):
    """Return the number of routes up n stairs using moves of 1 or 2.
        Order matters. Use two recursive calls. Do not save old results yet.
        n is an integer from 0 to 15. Zero stairs has one empty route.
        Sample: stair_routes(3) -> 3
        Sample: stair_routes(5) -> 8
    """
    raise NotImplementedError
