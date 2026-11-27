# Solutions

## `apply_each`

The caller chooses the operation. The loop handles order and collection.

For n readings, time is O(n) plus callback work. The output uses O(n) space.

## `slowest`

The key supplies the delay. max keeps the first item when several items share the largest key.

For n records, time is O(n) and extra space is O(1).

## `incident_order`

Tuple order sets the priority of each rule. A new list leaves the report source as it was.

For n records and bounded host length, worst-case time is O(n log n). Extra space is O(n).

## Next practice

Top K Frequent Elements. First group equal values and then decide how to compare their counts.
