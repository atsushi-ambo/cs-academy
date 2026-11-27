# Solutions

## `chunks_that_fit`

A chunk fits even when it uses all the free space. For k chunks that fit, time is O(k + 1), with O(1) extra space.

## `checks_used`

The counter is the next index before a check. Time is O(k + 1) for k checks. Extra space is O(1).

## `rounds_to_drain`

Only the number of rounds is returned. Time is O(r + 1) for r rounds. The counters take O(1) space.
