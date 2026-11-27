# Solutions

## `batch_pages`

There are n + 1 calls and n additions. Time and frame space are both O(n + 1). The loop version uses O(1) extra space.

## `job_orders`

There are O(n + 1) calls and frames. The function does not build the orders. This counts arithmetic operations, without the cost of large integers.

## `stair_routes`

Time grows exponentially because branches repeat smaller calls. O(2**n) is an upper bound. Space is O(n + 1) because only one path of calls is active at a time.
