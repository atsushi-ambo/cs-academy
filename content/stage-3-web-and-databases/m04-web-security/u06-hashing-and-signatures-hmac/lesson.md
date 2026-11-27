# Hashing and signatures (HMAC): integrity of data you send

## Why

A webhook can carry an operational event. Verify its bytes before acting on it.

## Message path

```text
sender:   shared key + body -> tag -> send body and tag
receiver: shared key + received body -> expected tag -> compare
```

The receiver computes an expected tag over the received bytes and checks the supplied tag.

## Example

Adding one JSON space changes the bytes. A tag for the old body should fail on the edited body.

## Common mistakes

- A plain hash gives no key-based proof.
- An HMAC gives integrity. Confidentiality requires encryption.
- A valid tag alone gives no replay protection.

## At work

Keep separate keys for separate message formats or services.
Use a fixed algorithm and exact bytes. Monitor failures without logging the keys.

## Summary

Use library HMAC and compare the complete tag. Verify freshness separately and retire old keys.

## Model answer

A matching HMAC checks that the exact bytes came with a tag made using the shared key. The tag does not hide the message. I also check a timestamp and an event ID to reject replays.
