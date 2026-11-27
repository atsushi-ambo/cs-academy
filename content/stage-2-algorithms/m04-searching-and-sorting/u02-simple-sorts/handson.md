# Hands-on: Simple sorts and why they are slow

Compare the same bubble pass with a large item at the left and a small item at the right. Use Python 3.9 or newer. Work in your own practice folder.

Save this code as `check.py`.

```python
values = [5, 1, 4, 2]
for j in range(len(values) - 1):
    if values[j] > values[j + 1]:
        values[j], values[j + 1] = values[j + 1], values[j]
print(values)
```

Run it with `python3 check.py`. Expect this output.

```text
[1, 4, 2, 5]
```

Use range(len(values) - 2) instead. The script prints [1, 4, 5, 2]. Explain why 5 never reaches the end. Restore the range.

If you keep your practice folder in Git, run `git add check.py` and
`git commit -m "Save algorithm experiment"` there to save the restored script.

- [ ] The original script prints the expected output.
- [ ] You can explain why the changed run differs.
- [ ] The restored script is saved in your practice folder.
