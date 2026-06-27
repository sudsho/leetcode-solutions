# 827. Making A Large Island

Difficulty: Hard
Topics  : array, depth-first search, breadth-first search, union find, matrix

## Problem

You are given an n x n binary matrix. You may change at most one 0 to a 1.
Return the size of the largest island (4-directionally connected 1s) you can
make.

## Approach

Label every existing island with a unique id and remember its size. Then for
each 0 cell, sum the sizes of the distinct islands bordering it and add one for
the flipped cell. The best such candidate, or the largest island already present
when there are no zeros, is the answer.

## Complexity

Time O(n^2), space O(n^2) for the id/size bookkeeping.

## Files

- `python/solution.py`
