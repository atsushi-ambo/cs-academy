def fib_misses(n):
    memo = {}

    def fib(k):
        if k in memo:
            return memo[k]
        if k < 2:
            memo[k] = k
        else:
            memo[k] = fib(k - 1) + fib(k - 2)
        return memo[k]

    value = fib(n)
    return (value, len(memo))


def stair_ways(n):
    from functools import lru_cache

    @lru_cache(maxsize=None)
    def ways(remaining):
        if remaining <= 1:
            return 1
        return ways(remaining - 1) + ways(remaining - 2)

    return ways(n)


def coin_ways(coins, amount):
    from functools import lru_cache

    values = sorted(set(coins))

    @lru_cache(maxsize=None)
    def count(index, left):
        if left == 0:
            return 1
        if left < 0 or index == len(values):
            return 0
        return count(index, left - values[index]) + count(index + 1, left)

    return count(0, amount)
