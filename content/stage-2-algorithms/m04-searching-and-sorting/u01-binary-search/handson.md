# Hands-on: Binary search

Try two ways to place a request beside equal timestamps. Use Python 3.9 or newer. Work in your own practice folder.

Save this code as `check.py`.

```python
def insert_slot(values, target):
    lo, hi = 0, len(values)
    while lo < hi:
        mid = (lo + hi) // 2
        if values[mid] < target:
            lo = mid + 1
        else:
            hi = mid
    return lo

print(insert_slot([2, 5, 5, 8], 5))
```

Run it with `python3 check.py`. Expect this output.

```text
1
```

Change < to <= in the comparison. The script now prints 3 because it skips both ties. Restore <.

If you keep your practice folder in Git, run `git add check.py` and
`git commit -m "Save algorithm experiment"` there to save the restored script.

- [ ] The original script prints the expected output.
- [ ] You can explain why the changed run differs.
- [ ] The restored script is saved in your practice folder.
