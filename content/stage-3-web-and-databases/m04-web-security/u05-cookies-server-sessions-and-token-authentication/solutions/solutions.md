# Cookies, server sessions, and token authentication

## `session_cookie`

Cookie formatting takes O(n) time and result space for an ID of n characters.

## `new_id`

For d draws with bounded IDs, expected time is O(d) and extra space is O(1). For production-size IDs, collisions are rare.

## `rotate`

Rotation retires the earlier ID and keeps it out of the choices, even when it is already absent from the table. Copying the table costs O(s) time and space for s stored sessions. Besides ID generation, the other table operations are O(1) on average with bounded IDs.

## Next practice

Simulate guest, login, expired request, and logout with a fake clock.
