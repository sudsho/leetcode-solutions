# 201. Bitwise and of Numbers Range

Difficulty: Medium
Topics  : bit manipulation

## Problem

Bitwise AND of all numbers in [left, right].

## Approach

Strip differing low bits by right-shifting both endpoints until they match.

## Complexity

Time O(log right), space O(1).

## Files

- `python/solution.py`
- `python/solution_alt.py`
