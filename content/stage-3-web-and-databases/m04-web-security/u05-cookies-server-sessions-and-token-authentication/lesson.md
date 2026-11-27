# Cookies, server sessions, and token authentication

## Why

Each dashboard request needs a current identity. A login from yesterday may already have expired.

## Session flow

```text
browser cookie -> opaque ID -> server record -> user and expiry check
```

The request carries an ID. The server finds the account and decides whether the ID is still usable.

## Example

Replace a guest ID with a random ID after login. Delete the new ID on logout.

## Common mistakes

- Clearing the browser cookie alone leaves copied IDs usable.
- HttpOnly does not stop scripts from causing requests.
- A decodable JWT may still fail signature or claim validation.

## At work

Set Secure, HttpOnly, and a suitable SameSite policy. Check expiry on every request.
Plan early revocation before deciding to use a locally checked JWT.

## Summary

Generate fresh IDs, keep their lifetime short, and invalidate them when trust changes.

## Model answer

After login I create a new session ID and retire the old one. At logout I delete the current session from the server. A copy of either retired ID can no longer find a valid session.
