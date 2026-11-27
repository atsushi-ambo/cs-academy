# Anatomy of a data breach

## Why

A breach can start with one defect and grow when other controls are missing.

## Investigation and response

```text
signal -> confirm and scope -> contain -> repair and verify -> monitor
               |---------------------------------> notify as needed
```

Start from a clue, find the affected systems, and contain ongoing exposure. Notify through the incident plan.

## Example

A toy report service logs an active key. Stop logging the key, revoke it, and install a replacement.
Check past logs as evidence and test that the old key fails.

## Common mistakes

- Deleting the key from source leaves old copies and an active key.
- A database grant does not prove a particular user owns a report.
- An alert alone does not prove that data left the system.

## Response checklist

1. Contain the risky route or credential. Preserve evidence with restricted access and scope the impact.
2. Rotate exposed secrets and revoke old ones. Patch the cause and verify the new configuration.
3. Force affected password resets and revoke sessions if passwords may be exposed.
4. Notify the incident team, affected users, and other parties as required by your plan.
5. Test allowed and denied operations. Watch for continued activity.

## Summary

Map every failure to a control and test that control. Close the exposure before declaring recovery.

## Model answer

I pause the risky export and revoke the leaked key. I keep restricted evidence and notify the incident lead. After rotating the key, I check that the old one fails and that new logs contain only approved fields.
