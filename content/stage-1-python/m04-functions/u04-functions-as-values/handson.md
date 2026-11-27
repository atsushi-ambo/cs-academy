# Hands-on

Save this example as `experiment.py` in a scratch directory.
Run `python3 experiment.py` from that directory.

```python
def run(rule, value):
    return rule(value)

def double(value):
    return value + 10

print(run(double, 4))
```

Expected output

```text
14
```

Change the sample inputs. Predict the new result before you run the file again.
