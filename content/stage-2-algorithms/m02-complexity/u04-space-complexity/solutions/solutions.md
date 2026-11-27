# Solutions

## Reset the original slots

```python
codes = [6, 9]
for index in range(len(codes)):
    codes[index] = 0
print(codes)
```

The loop visits n slots in O(n) time and uses one index, O(1) extra space.

## `count_large`

One pass takes O(n) time. The counter and current value take O(1) extra space.

## `above_zero`

Time is O(n). There are O(n) output slots and O(1) other extra space.

## `peak_open`

The loop takes O(n) time. Two counts track the peak in O(1) extra space.
