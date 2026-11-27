# Hands-on — Count moves to the tail

Run this in the app's Try step or save it as `demo.py` in a scratch folder outside the course repository.
At a terminal, run `python3 demo.py`.

```python
links = [2, None, 1]
index = 2
moves = 0
while links[index] is not None:
    index = links[index]
    moves += 1
print(index, moves)
```

Set the starting index to 0. Print the final index and the number of moves.

Expected output after your edit:

```text
1 2
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
