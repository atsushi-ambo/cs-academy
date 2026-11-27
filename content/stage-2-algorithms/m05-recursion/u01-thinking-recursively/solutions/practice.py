def batch_pages(n):
    if n == 0:
        return 0
    return n + batch_pages(n - 1)


def job_orders(n):
    if n == 0:
        return 1
    return n * job_orders(n - 1)


def stair_routes(n):
    if n == 0:
        return 1
    if n < 0:
        return 0
    return stair_routes(n - 1) + stair_routes(n - 2)
