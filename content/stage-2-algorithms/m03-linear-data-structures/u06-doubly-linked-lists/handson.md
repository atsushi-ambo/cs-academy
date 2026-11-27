# Hands-on — Repair a backward link

Run this in the app's Try step or save it as `demo.py` in a scratch folder outside the course repository.
At a terminal, run `python3 demo.py`.

```python
values = ["scan", "mail"]
nxt = [1, None]
prev = [None, None]
print(prev[nxt[0]] == 0)
```

Set prev[1] to 0 in the list. Check that a forward step and a backward step return to 0.

Expected output after your edit:

```text
True
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
