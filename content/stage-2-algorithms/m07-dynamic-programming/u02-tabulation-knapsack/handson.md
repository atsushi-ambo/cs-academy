# Hands-on

Save this example as `experiment.py` in a scratch directory.
Run `python3 experiment.py` from that directory.

```python
best = [0, 0, 0, 0, 0]
for capacity in range(4, 1, -1):
    best[capacity] = max(best[capacity], 3 + best[capacity - 2])
print(best)
```

Expected output

```text
[0, 0, 3, 3, 3]
```

Change the range to range(2, 5). Predict which cell counts the tool twice, then run the file again.
