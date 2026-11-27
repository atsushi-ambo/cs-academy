# Hashing and signatures (HMAC): integrity of data you send

## `sign`

Signing is deterministic for the same key and body. Time is O(n + k) for body and key lengths. The tuple references the body and adds O(1) result space.

## `verify_tag`

Recomputing and comparing takes O(n + k) time for the body and key. SHA-256 uses bounded working memory here and a fixed-size tag.

## `accept_event`

The receiver can retire keys without changing the body format. Lookup takes average O(1) time and extra space for bounded IDs, plus the verification cost.

## Next practice

Add an event ID and a deadline to the signed bytes. Test a duplicate event and an expired event.
