# Hands-on: Divide and conquer: split, solve, combine

Print the calls made while computing a small power. Use Python 3.9 or newer. Work in your own practice folder.

Save this code as `check.py`.

```python
def fast_power(base, exponent):
    print(exponent)
    if exponent == 0:
        return 1
    half = fast_power(base, exponent // 2)
    result = half * half
    if exponent % 2 == 1:
        result *= base
    return result

print(fast_power(2, 5))
```

Run it with `python3 check.py`. Expect this output.

```text
5
2
1
0
32
```

Remove the odd-exponent branch. The call trace is the same, but the last line is 1. Restore the branch.

If you keep your practice folder in Git, run `git add check.py` and
`git commit -m "Save algorithm experiment"` there to save the restored script.

- [ ] The original script prints the expected output.
- [ ] You can explain why the changed run differs.
- [ ] The restored script is saved in your practice folder.
