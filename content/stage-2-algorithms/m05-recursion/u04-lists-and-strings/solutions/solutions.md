# Solutions

## `size_total`

For k remaining items, time and stack space are O(k + 1). Each frame shares the input list.

## `reverse_label`

Slicing and joining copy characters. For length n, the work adds up to O(n²). The waiting frames hold O(n²) characters in suffixes and use O(n) frames. An index and a list of output letters can avoid these copies.

## `is_mirror`

For n letters, at most half the pairs are compared. Worst-case time and stack space are O(n + 1). No substrings are copied.

## `flatten_sizes`

For n entries and lists the time is O(n). The active call stack uses O(d) extra space for depth d. The returned list uses O(k) space for k integers.
