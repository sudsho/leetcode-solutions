# 13. Roman to Integer

Difficulty: Easy
Topics: string, hash table

## Problem

Convert a roman numeral string to an integer. Roman numerals use subtraction when a smaller numeral appears before a larger one (IV = 4, IX = 9, etc).

## Approach

Map each roman char to its value. Walk left to right and add the value, but if the current value is smaller than the next one, subtract it instead.

<!-- revisited -->
## Complexity

Time O(n), space O(1).

## Files

- `python/solution.py`
- `python/solution_alt.py`
