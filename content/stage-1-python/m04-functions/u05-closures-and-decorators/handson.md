# Hands-on

Save this example as `experiment.py` in a scratch directory.
Run `python3 experiment.py` from that directory.

```python
from functools import wraps

notes = []
def logged(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        notes.append(fn.__name__)
        return fn(*args, **kwargs)
    return wrapper

@logged
def health(host):
    return host + " ok"

health(host="api")
print(notes)
```

Expected output

```text
['health']
```

Now call health twice. Predict the log list before running the file again.
