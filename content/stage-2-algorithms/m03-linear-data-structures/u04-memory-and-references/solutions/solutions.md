# Solutions

## Make a new top-level list

```python
original = [5]
other = original[:]
other.append(8)
print(original, other)
```

Copying n slots takes O(n) time and O(n) space for the new list. The original stays the same.

## `same_list`

The identity test takes O(1) time and O(1) extra space. It does not read the list slots.

## `blank_grid`

The grid needs O(rows + rows × cols) output space and time. The loop uses O(1) extra space outside the output.

## `head_view`

A view of these bytes needs a start and a length. Time and extra space are O(1), since no bytes are copied.
