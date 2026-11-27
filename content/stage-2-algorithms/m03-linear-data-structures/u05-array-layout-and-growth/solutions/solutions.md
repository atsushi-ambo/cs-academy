# Solutions

## Write a grid cell by flat index

```python
cells = [0] * 6
cols = 3
index = 1 * cols + 0
cells[index] = 6
print(cells)
```

The index calculation and write take O(1) time and O(1) extra space. Making or printing all cells takes O(rows × cols) time for positive sizes.

## `read_cell`

A few arithmetic steps and one slot read take O(1) time and O(1) extra space.

## `copies_for_appends`

The count visits O(log(count + 2)) resize sizes. It uses O(1) extra space and builds no storage block.

## `make_array`

Without a resize, append takes O(1) time. A full array of n values takes O(n) time to grow. Across n appends the total work is O(n), or amortized O(1) per append. The blocks take O(n) space even while both are live during growth.
