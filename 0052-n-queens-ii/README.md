# 52. N-Queens II

Difficulty: Hard
Topics: backtracking

## Problem

The n-queens puzzle places n queens on an n x n chessboard so that no two attack each other. Return the number of distinct solutions.

## Approach

Place one queen per row and backtrack. Three sets track what is already attacked: occupied columns, "\" diagonals keyed by `row - col`, and "/" diagonals keyed by `row + col`. A column is safe only if none of the three sets contain it, which makes each check O(1). When a placement reaches row n we have a full valid board, so we count it.

## Complexity

Time O(n!) in the worst case (heavily pruned by the diagonal checks), space O(n) for the sets and recursion depth.

## Files

- `python/solution.py`
