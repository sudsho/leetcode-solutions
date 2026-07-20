# 376. Wiggle Subsequence

Difficulty: Medium
Topics: array, greedy, dynamic programming

## Problem

A wiggle sequence is one where successive differences strictly alternate between
positive and negative. Given `nums`, return the length of the longest wiggle
subsequence (elements kept in original order, deletions allowed).

## Approach

Greedy single pass. Track `up` = length of the longest wiggle run ending with a
rise, and `down` = longest ending with a drop. On a real rise, `up = down + 1`;
on a real drop, `down = up + 1`; equal neighbours are ignored. Answer is
`max(up, down)`.

## Complexity

Time O(n), space O(1).

## Files

- `python/solution.py`
