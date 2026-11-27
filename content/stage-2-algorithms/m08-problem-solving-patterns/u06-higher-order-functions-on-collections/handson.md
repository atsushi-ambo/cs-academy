# Hands-on

Save this example as `experiment.py` in a scratch directory.
Run `python3 experiment.py` from that directory.

```python
values = list(filter(lambda n: n > 0, [3, -1, 2]))
print(list(values), list(values))
```

Expected output

```text
[3, 2] [3, 2]
```

Change the predicate to n >= 2. Predict the kept values in both copies before running again.
