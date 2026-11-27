# SQL injection: break it, then fix it

## `find_ports`

Both filters run before sorting. With no index, time is O(n + k log(k + 1)) and space is O(k) for k matching rows.

## `sort_column`

Only code-owned names can reach the SQL statement. Time and extra space are O(1) with bounded input.

## `team_services`

Only a fixed clause extends the query. With no index and bounded fields, time is O(n + k log(k + 1)) and space is O(k) for k results.

## Next practice

LeetCode Explore: SQL. Practice filtering and sorting with separate value parameters in this toy database.
