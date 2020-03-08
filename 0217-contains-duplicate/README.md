# 217. Contains Duplicate

Difficulty: Easy
Topics: array, hash table

## Problem

Return True if any value appears at least twice in the array, else False.

## Approach

Throw the values in a set. If at any point the value was already there, we have a dup. Or compare len of set to len of list.

## Complexity

Time O(n), space O(n).

## Files

- `python/solution.py`
- `python/solution_alt.py`
