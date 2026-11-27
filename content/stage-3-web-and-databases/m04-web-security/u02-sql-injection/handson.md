# Hands-on in the Python sandbox

Use the unit’s Python editor with the sample below. Use only the supplied toy data.

## Give the name its own value slot

Set name to O'Neil. Keep the same query and its value tuple.

Completed sample

```python
import sqlite3

db = sqlite3.connect(":memory:")
name = "O'Neil"
print(db.execute("SELECT ?", (name,)).fetchone()[0])
```

Expected output line

```text
O'Neil
```

Run the final Code tests. Check the allowed case and the rejected case.
