# Hands-on — Repeat a status in a log

Run this in the app's Try step or save it as `demo.py` in a scratch folder outside the course repository.
At a terminal, run `python3 demo.py`.

```python
codes = [200, 500, 200]
seen = set()
for code in codes:
    seen.add(code)
print(len(seen))
```

Add 503 at the end of codes. Count distinct status codes.

Expected output after your edit:

```text
3
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
