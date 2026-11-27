# Hands-on: Merge sort and quicksort

Compare good and bad splits by inspecting the pivot index. Use Python 3.9 or newer. Work in your own practice folder.

Save this code as `check.py`.

```python
def lomuto_partition(values, lo, hi):
    pivot = values[hi]
    store = lo
    for i in range(lo, hi):
        if values[i] <= pivot:
            values[store], values[i] = values[i], values[store]
            store += 1
    values[store], values[hi] = values[hi], values[store]
    return store

values = [6, 2, 5, 3]
print(lomuto_partition(values, 0, 3), values)
```

Run it with `python3 check.py`. Expect this output.

```text
1 [2, 3, 5, 6]
```

Change the input to [2, 3, 5, 6]. Expect 3 [2, 3, 5, 6]. The pivot is already the largest, so the right group is empty. Restore the input.

If you keep your practice folder in Git, run `git add check.py` and
`git commit -m "Save algorithm experiment"` there to save the restored script.

- [ ] The original script prints the expected output.
- [ ] You can explain why the changed run differs.
- [ ] The restored script is saved in your practice folder.
