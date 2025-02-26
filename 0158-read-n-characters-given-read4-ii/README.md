# 158. Read N Characters Given Read4 II

Difficulty: Hard
Topics  : design

## Problem

Wrap read4 to support multiple read calls. Buffer leftover chars between calls.

## Approach

Maintain a small internal buffer of size 4 plus pointers for head and tail.

## Complexity

Time O(N), space O(1).

## Files

- `python/solution.py`
- `python/solution_alt.py`
