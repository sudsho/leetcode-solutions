# 318. Maximum Product of Word Lengths

Difficulty: Medium
Topics  : bit manipulation, array, string

## Problem

Given an array of strings `words`, return the maximum value of
`len(words[i]) * len(words[j])` where the two words share no common letters.
If no such pair exists, return 0.

## Approach

Encode each word's letter set as a 26-bit mask (bit k set iff letter k appears).
Two words are letter-disjoint iff `mask_i & mask_j == 0`. Precompute all masks,
then check every pair with a single bitwise AND and track the best product.

## Complexity

Time O(n^2 + total characters), space O(n).

## Files

- `python/solution.py`
