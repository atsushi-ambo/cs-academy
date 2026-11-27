# Practice solutions

## `search`

Each comparison discards one subtree. Time is O(h) for height h. This loop uses O(1) extra space.

## `insert`

A new key becomes a leaf on its search path. A duplicate leaves the tree intact. Time and recursion space are O(h), plus O(1) for a newly allocated leaf.

## `delete`

The successor is greater than every left key. After its old copy is removed, every remaining right key is greater than it. Search and successor work take O(h) time in total. The stack uses O(h) extra space.

## `is_bst`

Each call checks the range inherited from all ancestors. Worst-case time is O(n) and extra stack space is O(h).

## Next practice

LeetCode Explore — Binary Search Tree. Validate Binary Search Tree. Delete Node in a BST.
