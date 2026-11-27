# Simple sorts and why they are slow

## Why

Sorting jobs by size can help a server choose what runs next.

## Picture

```text
start       after selection      after one bubble pass
[5, 1, 4]   [1 | 5, 4]           [1, 4 | 5]
```

The bar marks the fixed part. Selection fixes the first place. Bubble fixes the last place.

## Example

Insert (2, B) into [(2, A), (5, C)]. Slide (5, C) right and place B after A.
This keeps equal keys in arrival order.

## Common mistakes

Insertion loses stability if it shifts equal keys. Bubble must reset its swap flag each pass.
Count value comparisons even when no items move.

## At work

Keep the arrival order when two log events share the same time.
Insertion sort can make sense for a short, nearly ordered batch.

## Summary

These sorts can take O(n²) time. Insertion and early-stop bubble take O(n) time on sorted input.
A selection swap can move a key past its tie.

**Model answer**

A pass without swaps shows that every neighboring pair in the active part is in order. The end is already fixed. Selection sort still checks the whole remaining part to find the next minimum.
