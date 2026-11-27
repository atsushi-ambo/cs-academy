# Hands-on: Backtracking

Watch what happens when two saved answers point at the same list. Use Python 3.9 or newer. Work in your own practice folder.

Save this code as `check.py`.

```python
def service_groups(services):
    result = []
    path = []

    def visit(index):
        if index == len(services):
            result.append(path[:])
            return
        visit(index + 1)
        path.append(services[index])
        visit(index + 1)
        path.pop()

    visit(0)
    return result

print(service_groups(["api", "db"]))
```

Run it with `python3 check.py`. Expect this output.

```text
[[], ['db'], ['api'], ['api', 'db']]
```

Replace result.append(path[:]) with result.append(path). The output is now [[], [], [], []]. Restore the copy.

If you keep your practice folder in Git, run `git add check.py` and
`git commit -m "Save algorithm experiment"` there to save the restored script.

- [ ] The original script prints the expected output.
- [ ] You can explain why the changed run differs.
- [ ] The restored script is saved in your practice folder.
