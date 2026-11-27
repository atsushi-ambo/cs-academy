# Solutions

## `my_map`

The list builds in input order. The helper only needs to iterate once.

For n items, time is O(n) plus callback work. The result uses O(n) space.

## `my_filter`

The predicate controls membership. The result keeps the original values and order.

For n inputs, time is O(n) plus predicate work. Output space is O(k) for k retained items.

## `my_reduce`

A left-to-right fold preserves order even for rules such as subtraction. The initial value handles the empty case.

For n items, time is O(n) plus combine work. The loop itself uses O(1) extra space beyond the accumulator.

## `incident_report`

Filtering early puts the same errors into both the total and the view. A stable sort keeps the order of equal keys.

For n inputs and k retained records with bounded host length, time is O(n + k log(k+1)). Extra space is O(k+1).

## Next practice

LeetCode Explore Array and String. Find the Highest Altitude.
