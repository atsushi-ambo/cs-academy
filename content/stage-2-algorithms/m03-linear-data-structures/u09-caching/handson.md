# Hands-on — See which calls do work

Run this in the app's Try step or save it as `demo.py` in a scratch folder outside the course repository.
At a terminal, run `python3 demo.py`.

```python
memo = {}
for key in ["api", "db", "mail"]:
    if key not in memo:
        print("compute", key)
        memo[key] = len(key)
print(len(memo))
```

Replace 'mail' with 'api'. The last line should count only distinct keys. Check that compute api appears once.

Expected output after your edit:

```text
compute api
compute db
2
```

Undo your edit and run the original. Name the value or link that changed
the output. Restore your edit and run it once more.

To save your experiment, run these commands in that scratch folder:

```sh
git init
git add demo.py
git commit -m "Save data structure experiment"
```

## Done when

- [ ] The edited script prints the expected line.
- [ ] You can explain the change from the original output.
- [ ] Your final Code exercise passes in the app.
