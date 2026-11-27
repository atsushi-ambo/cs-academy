# XSS and CSRF: break it, then fix it

## Why

An alert label should display as text. A settings form should save only an intended change.

## Two paths

```text
raw label -> HTML escape -> page text
cookie + form token -> match in session -> save
```

The page protects how data is read. The handler protects the server write.

## Example

The label `<b>ready</b>` should show the brackets as text.
A theme POST with a token from a second session should leave settings alone.

## Common mistakes

- HTML escaping does not validate a URL.
- A session cookie can arrive without an intended form submission.
- SameSite alone misses some unwanted requests. Keep the token check.

## At work

Use templates with context-aware escaping and a short CSP allowlist.
Test both the allowed POST and the rejected POST without a token.

## Summary

Keep untrusted output in its data context. Check the session token before changing state.

## Model answer

I escape an alert label before putting it into HTML text. The theme handler checks a token for the exact session before it writes. SameSite helps the browser limit when it sends the session cookie.
