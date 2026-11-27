# Hands-on in the Python sandbox

Use the unit’s Python editor with the sample below. Use only the supplied toy data.

## See how a cookie flag changes the header

Set cookie['sid']['httponly'] to True after setting the value.

Completed sample

```python
from http.cookies import SimpleCookie

cookie = SimpleCookie()
cookie["sid"] = "sample"
cookie["sid"]["httponly"] = True
print(cookie["sid"].OutputString())
```

Expected output line

```text
sid=sample; HttpOnly
```

## Draw a random session ID

Change the input to 32 random bytes. Print the length, while keeping the ID private.

Completed sample

```python
from secrets import token_urlsafe

sid = token_urlsafe(32)
print("ID characters", len(sid))
```

Expected output line

```text
ID characters 43
```

Run the final Code tests. Check the allowed case and the rejected case.
