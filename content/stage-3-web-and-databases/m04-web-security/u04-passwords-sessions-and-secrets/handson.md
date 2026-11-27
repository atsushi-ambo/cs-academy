# Hands-on in the Python sandbox

Use the unit’s Python editor with the sample below. Use only the supplied toy data.

## Count how little a fast hash needs

Change OUTPUT to 'sha256'. Both use one hash call here. Compare these with the later KDF timing.

Completed sample

```python
import hashlib

OUTPUT = "sha256"
known_input = b"public-demo"
digest = hashlib.new(OUTPUT, known_input).digest()
print("digest bytes", len(digest))
```

Expected output line

```text
digest bytes 32
```

## Measure the cost per known input

Change calls from 4 to 8. Compare the printed average times. The test counts examples, so timer noise cannot fail it.

Completed sample

```python
from hashlib import pbkdf2_hmac, scrypt, sha256
from time import perf_counter

known = b"public-demo"
calls = 8
start = perf_counter()
for _ in range(calls):
    sha256(known).digest()
print("fast ms/call", 1000 * (perf_counter() - start) / calls)
start = perf_counter()
for _ in range(calls):
    scrypt(known, salt=b"timer-fixture", n=1024, r=8, p=1, dklen=32)
print("scrypt ms/call", 1000 * (perf_counter() - start) / calls)
start = perf_counter()
for _ in range(calls):
    pbkdf2_hmac("sha256", known, b"timer-fixture", 10000)
print("PBKDF2 ms/call", 1000 * (perf_counter() - start) / calls)
print("calls per method", calls)
```

Expected output line

```text
calls per method 8
```

Run the final Code tests. Check the allowed case and the rejected case.
