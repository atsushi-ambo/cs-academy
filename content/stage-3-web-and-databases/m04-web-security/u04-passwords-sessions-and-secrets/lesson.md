# Passwords, sessions, and secrets

## Why

Plaintext in a stolen backup gives away all stored passwords. Fast hashes leave cheap offline checks.

## Storage and login

```text
register: password + random salt + profile -> KDF -> record
verify:   password + stored salt + profile -> KDF -> compare
```

The record stores the digest, salt, algorithm, and cost. Verification repeats the same calculation.

## Example

A record with lab n=1024 can still verify under a lab policy of n=2048.
After a valid login, write a fresh salt and digest using the new profile, but only when it is stronger than the stored one.

## Common mistakes

- A shared salt lets one guess be tested against many accounts at once.
- An online rate limit has no effect on offline guesses.
- Weak or legacy hashes need a migration plan. Reset exposed credentials.

## At work

Prefer maintained password libraries with a measured Argon2id profile. For scrypt, plan its memory use (about 128 MiB for the OWASP baseline) and set Python's maxmem on purpose.
Keep peppers and service keys in managed secrets. Redact passwords and tokens from logs.
Use random, hashed, one-use reset tokens and revoke sessions after a reset.

## Summary

Use a fresh salt and a slow KDF. Verify with the saved profile and upgrade only after success.

## Model answer

A unique salt means one computed digest cannot be reused for many accounts. The attacker must run the same guess again for each salt. scrypt makes every one of those checks cost time and memory. An online rate limit protects the login service from repeated requests.
