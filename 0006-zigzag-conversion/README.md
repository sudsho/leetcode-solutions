# 6. Zigzag Conversion

Difficulty: Medium
Topics  : string, simulation

## Problem

Write the string out in a zigzag pattern on a given number of rows, then read it off row by row to get the result.

## Approach

Keep one list per row. Walk the input once with a row index and a direction (`+1` or `-1`). Flip the direction when you hit the top or the bottom row. The character at each step goes into the current row's list. At the end, join all rows together.

The early return for `numRows == 1` or `numRows >= len(s)` covers the two cases where the zigzag is a no-op.

## Complexity

Time O(n), space O(n).

## Files

- `python/solution.py`
