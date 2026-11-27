# Practice solutions

## `make_node`

The node holds references to the existing children. Creating one node takes O(1) time and O(1) space.

## `preorder`

The helper visits children in the order required for preorder. Appending once per node takes O(n) time. The call stack uses O(h) extra space, plus O(n) for the returned list.

## `inorder`

The helper visits children in the order required for inorder. Appending once per node takes O(n) time. The call stack uses O(h) extra space, plus O(n) for the returned list.

## `postorder`

The helper visits children in the order required for postorder. Appending once per node takes O(n) time. The call stack uses O(h) extra space, plus O(n) for the returned list.

## `level_order`

Each node enters and leaves the queue once. Time is O(n). The queue holds parts of two neighboring levels, so it uses O(w) extra space for maximum width w. The result uses O(n) space.

## `tree_stats`

A leaf returns (1, 1), and each real node is processed once. Time is O(n) and extra stack space is O(h).

## Next practice

LeetCode Explore — Binary Tree. Binary Tree Level Order Traversal. Maximum Depth of Binary Tree.
