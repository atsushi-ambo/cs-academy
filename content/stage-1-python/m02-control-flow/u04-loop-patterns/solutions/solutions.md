# Solutions

## `error_count`

One pass visits n codes in O(n) time. Only a counter and the current code are needed, so extra space is O(1).

## `first_recovery`

The loop ends on the first match. Worst-case time is O(n), with O(1) extra space.

## `large_files`

For r folders and n files, time is O(r + n). Even empty folders are visited. The counter and loop variables use O(1) extra space.
