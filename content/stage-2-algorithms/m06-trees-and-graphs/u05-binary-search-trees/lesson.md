# Binary search trees: insert, search, delete

## Why

A BST can answer “is this ID active?” while also supporting changes.
If the tree stays short, a search can skip most IDs.

## Diagram

```text
      20
     /  \
   11    60
         /
        35
          \
           42
```

20 has left child 11 and right child 60. 60 has left child 35, whose right child is 42.

## Example

Remove 20. Its successor is 35, the smallest key in the right subtree.
Copy 35 to the root. Then replace the old 35 with its right child, 42.
An inorder visit now reads 11, 35, 42, 60.

## Common mistakes

Checking only the parent misses a key in the wrong subtree.
Replacing a node with None also drops any children it still has.

## Real-world use

An ordered in-memory index can insert or remove an ID and find the next larger ID.
A system that expects many sorted inserts can use a balanced tree for that index.

## Summary

Search and update follow comparisons. Path costs grow with height.
An ordinary BST can reach height n. Checking all bounds visits up to n nodes.

## Model explanation

Go right once, then go left until the path ends. Copy that key to the node being deleted. Remove the old copy from the right subtree and keep its right child if it has one.
