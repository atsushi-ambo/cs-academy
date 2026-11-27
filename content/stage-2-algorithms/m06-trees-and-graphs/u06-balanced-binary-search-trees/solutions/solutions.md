# Practice solutions

## `balance_factor`

Each child height is already stored. The function reads at most two heights, so time and extra space are O(1).

## `rotate_left`

The middle branch stays between the same two keys. Two stored heights are updated after the links change. Time and extra space are O(1).

## `rotate_right`

The middle branch stays between the same two keys. Two stored heights are updated after the links change. Time and extra space are O(1).

## `avl_insert`

The first turn in an inside case lines up the heavy branch. The outer turn repairs the imbalance. Each visit and rotation is O(1). AVL height is O(log n), so insertion costs O(log n) time and stack space.

## Next practice

LeetCode Explore — Binary Search Tree. Balanced Binary Tree. Balance a Binary Search Tree.
