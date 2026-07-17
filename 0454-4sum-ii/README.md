# 454. 4Sum II

Difficulty: Medium
Topics: hash table

## Problem

Given four integer arrays `nums1`, `nums2`, `nums3`, `nums4` all of length `n`,
return the number of tuples `(i, j, k, l)` such that
`nums1[i] + nums2[j] + nums3[k] + nums4[l] == 0`.

## Approach

Meet in the middle. Build a Counter of every pairwise sum `a + b` drawn from the
first two arrays. Then walk every pairwise sum `c + d` from the last two arrays
and add the number of first-half sums equal to `-(c + d)`, since those are the
ones that cancel it to zero.

## Complexity

Time O(n^2) for the two independent double loops, space O(n^2) for the Counter.

## Files

- `python/solution.py`
