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

Change calls from 4 to 8. Compare the printed average times. The test counts examples, so timer noise cannot fail it. The scrypt n=1024 and the 10000 PBKDF2 steps are lab-only values. Real settings are in the next step.

Completed sample

```python
import hashlib
from time import perf_counter

if not hasattr(hashlib, "scrypt"):
    raise SystemExit("This Python has no scrypt. Run the lab in the app's Python 3.13 sandbox.")

known = b"public-demo"
calls = 8
start = perf_counter()
for _ in range(calls):
    hashlib.sha256(known).digest()
print("fast ms/call", 1000 * (perf_counter() - start) / calls)
start = perf_counter()
for _ in range(calls):
    hashlib.scrypt(known, salt=b"timer-fixture", n=1024, r=8, p=1, dklen=32)
print("scrypt ms/call", 1000 * (perf_counter() - start) / calls)
start = perf_counter()
for _ in range(calls):
    hashlib.pbkdf2_hmac("sha256", known, b"timer-fixture", 10000)
print("PBKDF2 ms/call", 1000 * (perf_counter() - start) / calls)
print("calls per method", calls)
```

Expected output line

```text
calls per method 8
```

Run the final Code tests. Check the allowed case and the rejected case.
