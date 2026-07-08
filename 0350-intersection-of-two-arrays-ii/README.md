# 350. Intersection of Two Arrays II

Difficulty: Easy
Topics  : array, hash table, two pointers, sorting

## Problem

Given two integer arrays, return their intersection *with multiplicity*: each
value appears in the result as many times as it shows in both arrays. Order does
not matter.

## Approach

Count the values of one array with a `Counter`, then walk the other array and
emit a value while its remaining count is positive, decrementing as we go. That
spends each shared occurrence exactly once. The alternate file sorts both arrays
and two-pointers them, taking one copy each time the two sides match - which
preserves the minimum multiplicity for free and is the version the follow-up
about sorted / very large inputs is hinting at.

## Complexity

Counter version: time O(n + m), space O(min(n, m)). Two-pointer version: time
O(n log n + m log m), space O(1) beyond the output.

## Files

- `python/solution.py`
- `python/solution_alt.py`
