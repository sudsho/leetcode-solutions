# 259. 3Sum Smaller

Difficulty: Medium
Topics  : array, two pointers, sorting

## Problem

Given an array `nums` and a target, count the number of index triplets `i < j < k` with `nums[i] + nums[j] + nums[k] < target`.

## Approach

Sort the array, then fix the first index `i` and run two pointers `lo`/`hi` over the rest. When `nums[i] + nums[lo] + nums[hi] < target`, every element between `lo` and `hi` also satisfies the bound because the array is sorted, so we add `hi - lo` triplets in one step and move `lo` right. Otherwise the sum is too large and we drop `hi`. The batch-count trick is what turns this from O(n^3) into O(n^2).

## Complexity

Time O(n^2), space O(1) beyond the sort.

## Files

- `python/solution.py`
