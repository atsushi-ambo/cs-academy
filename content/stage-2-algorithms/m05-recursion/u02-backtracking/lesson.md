# Backtracking

## Why

Some tasks ask you to try many choices. A single partial answer can lead to several full answers.

## Picture

```text
choose "api" -> ["api"]
   choose "db" -> ["api", "db"] -> save a copy
   undo "db"   -> ["api"]
   choose "cache" -> ["api", "cache"] -> save a copy
```

The two deeper paths start from the same list after you undo the first deeper choice.

## Example

A queen at (0, 1) gives diagonal labels -1 and 1. At (1, 2), the first label is also -1.
Skip that square before visiting a later row.

## Common mistakes

Copy the path before saving it. Undo every change to state after a call, including flags and sets.

## At work

Try maintenance orders for a few servers. Skip a choice that breaks an uptime rule before testing later choices.

## Summary

Choose, explore, and undo. Prune a choice when no answer can follow it.

**Model answer**

Squares on the same diagonal have the same row minus column or the same row plus column. I keep three sets, one for columns, one for differences, and one for sums, and I never mix them. I skip a square if its column, difference, or sum is already in the matching set. When I return, I remove those three values so the next choice starts from the same board.
