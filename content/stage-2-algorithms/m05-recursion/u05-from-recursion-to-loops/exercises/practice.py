def reduced_price(cents, weeks):
    """Each week, replace the price by 90 percent of its current value.
        Round down each week using cents * 9 // 10. Return the final cents.
        Rewrite the tail call reduced_price(cents * 9 // 10, weeks - 1)
        as a while loop. Base case: return cents when weeks is zero.
        cents and weeks are integers from 0 to 10000.
    Sample: reduced_price(99, 2) -> 80
        Sample: reduced_price(99, 0) -> 99
    """
    raise NotImplementedError


def unpack_sizes(batch):
    """Rewrite recursive flattening as a while loop with an explicit stack.
        Return all integer sizes in left-to-right order. No recursive calls.
        batch is a finite nested list with up to 5000 entries and lists.
        Depth can reach 1500. Do not change the input.
        Sample: unpack_sizes([[8], 2, [6, []]]) -> [8, 2, 6]
        Sample: unpack_sizes([[], []]) -> []
    """
    raise NotImplementedError


def route_count(n):
    """Count routes up n stairs with moves of 1 or 2. Order matters.
        Use a loop and keep only two previous counts. No recursion.
        n is an integer from 0 to 1200. The empty route counts as one.
        Sample: route_count(4) -> 5
        Sample: route_count(0) -> 1
    """
    raise NotImplementedError
