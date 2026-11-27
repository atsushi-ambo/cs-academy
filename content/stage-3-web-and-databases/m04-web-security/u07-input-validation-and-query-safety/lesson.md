# Input validation and query safety, everywhere

## Why

Ports, file names, and profile fields arrive from requests. Each needs clear server rules.

## Three checks

```text
actor -> ownership policy
input -> type, length, range, field checks
file name -> resolved path -> permitted root
```

The server checks the actor and input. It confirms a file's location after links and relative paths are resolved.

## Example

A port of 443 as an integer is valid. The string "443" fails a strict integer contract.
A path under reports-old is outside reports, even though the text starts the same way.

## Common mistakes

- Browser validation cannot secure a server endpoint.
- A text prefix can confuse two neighboring folders.
- Copying all incoming fields lets the caller change policy fields.

## At work

Validate at each server entry point. Keep using parameterized queries and context-specific output escaping.
Keep served directory trees under trusted ownership.

## Summary

Validate input on the server. Contain file paths and permit only the fields the action needs.

## Model answer

The server checks that the actor owns the profile. It also accepts only the label field and checks its size. A browser form can help the user, but the server enforces the rules.
