# Hands-on

Save this example as `experiment.py` in a scratch directory.
Run `python3 experiment.py` from that directory.

```python
def fib(n):
    global calls
    calls += 1
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)

calls = 0
print(fib(3), calls)
```

Expected output

```text
2 5
```

Change the input to 4 again. Draw its call tree and check that it has nine calls.
