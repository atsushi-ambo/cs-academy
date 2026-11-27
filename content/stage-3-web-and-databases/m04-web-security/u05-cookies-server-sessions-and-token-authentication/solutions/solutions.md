# Cookies, server sessions, and token authentication

## `session_cookie`

Cookie formatting takes O(n) time and result space for an ID of n characters.

## `new_id`

For d draws with bounded IDs, expected time is O(d) and extra space is O(1). For production-size IDs, collisions are rare.

## `rotate`

Rotation retires the earlier ID. Besides ID generation, average time and extra space are O(1) with bounded IDs.

## Next practice

Simulate guest, login, expired request, and logout with a fake clock.
