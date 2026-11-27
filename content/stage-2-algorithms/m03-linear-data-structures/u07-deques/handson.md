# Hands-on — Wrap a left push

Run this in the app's Try step or save it as `demo.py` in a scratch folder outside the course repository.
At a terminal, run `python3 demo.py`.

```python
head = 1
slots = [None] * 4
head = (head - 1) % len(slots)
slots[head] = "retry"
print(head, slots[head])
```

Set the starting head to 0. Print the new head and its value.

Expected output after your edit:

```text
3 retry
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
