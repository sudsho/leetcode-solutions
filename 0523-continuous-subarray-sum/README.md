# 523. Continuous Subarray Sum

Difficulty: Medium
Topics  : array, hash table, prefix sum, math

## Problem

Given an integer array `nums` and an integer `k`, return `true` if `nums` has a *good* subarray: a contiguous slice of length at least two whose sum is a multiple of `k`. Zero counts as a multiple of `k`.

## Approach

Checking every subarray is O(n^2) even with prefix sums, so the sum has to become a key instead of a value. The observation is that a slice `(j, i]` sums to a multiple of `k` exactly when `prefix[i]` and `prefix[j]` leave the same remainder mod `k` — the multiples cancel in the subtraction. So carry the running prefix sum mod `k` and look for a repeat.

That makes this 525 with a different relabeling. Both walk the array with a hash map of value to earliest index; 525 relabels `0` to `-1` so a balanced stretch sums to zero, and this one reduces mod `k` so a divisible stretch repeats a remainder. Seed the map with `{0: -1}` for the same reason in both: a prefix that already qualifies on its own has no earlier partner to pair with.

The length-at-least-two rule is the part that bites. A repeated remainder alone is not enough, since a single element equal to a multiple of `k` matches the previous index and would pass a naive check. Guarding with `i - first_seen[r] >= 2` fixes it, and that guard is also why the map has to keep the *first* index for each remainder — the earliest match gives the widest window, so overwriting would reject inputs that do have a valid slice further back.

Storing first indices rather than frequencies is inherited from 525: this is an existence question about a window, not a counting question like 560.

## Complexity

Time O(n) for the single pass, space O(min(n, k)) since the map holds at most one entry per distinct remainder.

## Files

- `python/solution.py`
