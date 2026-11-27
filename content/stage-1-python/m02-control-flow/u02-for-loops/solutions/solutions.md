# Solutions

## `rack_labels`

The inclusive end needs a stop one higher. For n labels, time and output space are O(n). Extra space outside the returned list is O(1).

## `batch_offsets`

The exclusive stop keeps every offset inside the batch. For k offsets, time and output space are O(k). The range itself needs O(1) space.

## `failed_minutes`

Each position pairs a duration with its flag. Time is O(n) for n jobs. The index and total use O(1) extra space.
