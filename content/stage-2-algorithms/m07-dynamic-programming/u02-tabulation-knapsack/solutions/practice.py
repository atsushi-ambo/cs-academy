def bag_value(items, capacity):
    best = [0] * (capacity + 1)
    for weight, value in items:
        for remaining in range(capacity, weight - 1, -1):
            best[remaining] = max(best[remaining], value + best[remaining - weight])
    return best[capacity]


def min_coins(coins, amount):
    unreachable = amount + 1
    best = [0] + [unreachable] * amount
    for total in range(1, amount + 1):
        for coin in coins:
            if coin <= total:
                best[total] = min(best[total], 1 + best[total - coin])
    if best[amount] == unreachable:
        return -1
    return best[amount]


def lcs_length(left, right):
    best = [[0] * (len(right) + 1) for row in range(len(left) + 1)]
    for i in range(1, len(left) + 1):
        for j in range(1, len(right) + 1):
            if left[i - 1] == right[j - 1]:
                best[i][j] = 1 + best[i - 1][j - 1]
            else:
                best[i][j] = max(best[i - 1][j], best[i][j - 1])
    return best[len(left)][len(right)]


def bag_choices(items, capacity):
    best = [[0] * (capacity + 1) for row in range(len(items) + 1)]
    for i in range(1, len(items) + 1):
        weight, value = items[i - 1]
        for c in range(capacity + 1):
            best[i][c] = best[i - 1][c]
            if weight <= c:
                best[i][c] = max(best[i][c], value + best[i - 1][c - weight])

    chosen = []
    c = capacity
    for i in range(len(items), 0, -1):
        if best[i][c] != best[i - 1][c]:
            chosen.append(i - 1)
            c -= items[i - 1][0]
    return chosen[::-1]
