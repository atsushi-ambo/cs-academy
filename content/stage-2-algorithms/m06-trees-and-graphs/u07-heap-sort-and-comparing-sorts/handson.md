# Hands-on: watch the boundary

Save the code in a scratch folder as `boundary.py` and run `python3 boundary.py`.

```python
def sift_down_max(values, i, end):
    while 2*i + 1 < end:
        child = 2*i + 1
        right = child + 1
        if right < end and values[right] > values[child]:
            child = right
        if values[i] >= values[child]:
            break
        values[i], values[child] = values[child], values[i]
        i = child
values = [9, 6, 5, 1, 12]
end = 4
last = end - 1
values[0], values[last] = values[last], values[0]
end -= 1
sift_down_max(values, 0, end)
print(values[:end], values[end:])
```

Expected output:

```text
[6, 1, 5] [9, 12]
```

Change the sift call to use `len(values)` in place of `end`. Run again.

```text
[6, 12, 5] [9, 1]
```

Restore the end bound. Explain why the second run mixed the two parts.
