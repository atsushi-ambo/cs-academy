# Hands-on in the Python sandbox

Use the unit’s Python editor with the sample below. Use only the supplied toy data.

## Change only the message

Change the second body to b'down' while keeping the key the same.

Completed sample

```python
import hmac

key = b"toy-only"
first = hmac.digest(key, b"up", "sha256")
second = hmac.digest(key, b"down", "sha256")
print(hmac.compare_digest(first, second))
```

Expected output line

```text
False
```

Run the final Code tests. Check the allowed case and the rejected case.
