# 303. Range Sum Query - Immutable

Difficulty: Easy
Topics  : array, prefix sum, design

## Problem

Given an integer array `nums`, answer many `sumRange(left, right)` queries returning the inclusive sum `nums[left] + ... + nums[right]`. The array never changes.

## Approach

Because the array is immutable, every query can be answered from a single precomputed prefix-sum array built once in the constructor. Store `prefix[i]` as the sum of the first `i` elements, with `prefix[0] = 0`, and any range sum becomes `prefix[right + 1] - prefix[left]`.

The padding zero at the front is the detail worth keeping: without it, a query starting at index 0 needs its own branch. With it, both endpoints are handled by the same subtraction.

The immutability is the whole reason this works. Once updates enter the picture the prefix array has to be rebuilt on every write, which is what pushes 307 and 308 toward a Fenwick tree instead.

## Complexity

Time O(n) to build, O(1) per query. Space O(n).

## Files

- `python/solution.py`
