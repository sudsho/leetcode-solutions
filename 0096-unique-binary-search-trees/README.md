# 96. Unique Binary Search Trees

Difficulty: Medium
Topics  : dynamic programming, tree, binary search tree, math

## Problem

Given an integer `n`, return the number of structurally unique BSTs that store
exactly the values `1 .. n`.

## Approach

Fix each value `i` as the root. Because the tree is a BST, the `i-1` smaller
values must all live in the left subtree and the `n-i` larger values in the
right subtree, and the two sides are shaped independently. So the number of
trees with `i` at the root is `count(i-1) * count(n-i)`, and the answer sums
that product over every choice of root. That recurrence is exactly the Catalan
numbers, filled bottom-up: `dp[k]` is the number of BSTs over `k` ordered
values, with the empty tree as the `dp[0] = 1` base case.

## Complexity

Time O(n^2) - a double loop over node counts and root choices. Space O(n) for
the dp array.

## Files

- `python/solution.py`
