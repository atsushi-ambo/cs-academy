# Authentication vs authorization

## `authorize`

Checking the organization first limits the admin rule. With bounded fields, time and extra space are O(1).

## `visible_ids`

Each report gets its own policy check. For n reports and k allowed results, time is O(n) with a constant-time policy, and result space is O(k).

## `report_body`

Finding the report only locates data. The policy protects it. With bounded IDs and constant-time policy, average time and extra space are O(1).

## Next practice

Apply the same policy to a report export. LeetCode Explore: Hash Table.
