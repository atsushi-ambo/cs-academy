# Input validation and query safety, everywhere

## `valid_target`

These tests use fixed bounds and Python length lookups. Time and extra space are O(1).

## `report_path`

Resolution follows path components and links. With bounded path sizes and filesystem limits, this check uses bounded time and space, excluding filesystem latency.

## `edit_label`

Access and field checks run before the edit. For bounded IDs, fixed input fields, and a fixed profile, time and extra space are O(1).

## Next practice

Define rules for a file export request. Test its owner, output format, and permitted directory.
