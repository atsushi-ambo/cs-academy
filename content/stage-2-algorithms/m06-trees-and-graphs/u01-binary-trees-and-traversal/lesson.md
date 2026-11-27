# Binary trees and traversal

## Why

A tree can group service checks. Use preorder to show a heading before its checks.
Use postorder to finish the checks before you report the group result.

## Diagram

```text
        api
       /   \
     db    cdn
      \
      log
```

The root is api. Its left child is db, and its right child is cdn.
The right child of db is log.

## Example

| Order | Result |
|---|---|
| Preorder | api, db, log, cdn |
| Inorder | db, log, api, cdn |
| Postorder | log, db, cdn, api |
| Level order | api, db, cdn, log |

The height is 3 because api → db → log is the longest path.
There are two leaves, log and cdn.

## Common mistakes

A node with one child still has a branch to visit. Count it as a leaf only if both links are empty.
Return to the caller at None before reading any attributes.

## Real-world use

A report can visit groups before their checks when it prints headings.
A status collector can use postorder to gather check results before reporting each group.

## Summary

Depth-first visits differ in when they visit the parent. A queue gives level order.
Visits take O(n) time, with O(h) stack or O(w) queue space before the result list.

## Model explanation

Preorder visits the parent first, then finishes the left subtree before starting the right. Level order visits the parent first too. A queue keeps nodes already on a level ahead of their children.
