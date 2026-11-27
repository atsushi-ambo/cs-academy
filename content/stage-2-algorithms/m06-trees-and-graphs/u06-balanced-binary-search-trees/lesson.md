# Balanced binary search trees (AVL rotations, the idea of red-black)

## Why

With sorted inserts, an ordinary BST can grow one long branch.
An AVL tree repairs each lean so future searches stay short.

## Diagram

```text
       30              30               20
      /               /                /  \
    10       ->      20       ->      10   30
      \             /
       20          10
```

30 has left child 10, which has right child 20.
A left turn at 10 moves 20 up. A right turn at 30 makes 20 the new root.

## Example

Before the LR repair the factor of 30 is 2, while the factor of 10 is -1.
After both turns each child has height 1. The new root has height 2 and factor 0.
LL and RR need only one turn. RL mirrors LR.

## Common mistakes

Dropping the pivot's middle branch loses keys.
Refreshing the new parent first reads a stale height from the old parent.

## Real-world use

An ordered index can keep lookup paths short as jobs arrive in increasing ID order.
Red-black trees use marks and rotations to keep keys ordered with a different balance rule.

## Summary

Refresh heights on the way back after insertion. Rotate at a lean outside -1 through 1.
An AVL lookup or insert has O(log n) time when heights stay valid.

## Model explanation

In an LR case the node leans left but its left child leans right. Turn the left child left, then turn the node right. The rotations keep all keys in the same inorder sequence.
