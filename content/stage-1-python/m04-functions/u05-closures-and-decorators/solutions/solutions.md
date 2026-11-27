# Solutions

## `make_total`

Each outer call creates one binding. Its nested function updates that same binding when called.

Each call performs O(1) work and holds O(1) state, treating integers as fixed-size.

## `timed`

The clock and sink are passed in, so the same wrapper works with real or fake readings.

The wrapper adds two clock calls, one sink call, and O(1) other work and storage beyond argument forwarding.

## `retry_with_log`

A bound makes failure finite. Checking the specific sentinel lets valid falsey values such as 0 succeed.

For k attempts, overhead is O(k) time and O(1) extra space beyond argument forwarding and the callbacks.

## Next practice

LeetCode Explore Hash Table offers practice separating stored state from the code that uses it.
