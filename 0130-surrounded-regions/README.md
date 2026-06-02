# 130. Surrounded Regions

Difficulty: Medium
Topics  : graph, flood fill, dfs

## Problem

Given a board of X and O, flip every O region that is fully surrounded by X. Regions connected to the border stay as O.

## Approach

Inverse flood fill from the borders. Mark every O reachable from a border cell with a temporary sentinel `#`. After the sweep, the remaining O are the surrounded ones - flip those to X and restore `#` back to O. Iterative stack to avoid recursion blowing up on long border runs.

## Complexity

Time O(rows * cols), space O(rows * cols) worst case for the stack.

## Files

- `python/solution.py`
