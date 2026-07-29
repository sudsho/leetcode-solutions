# 974. Subarray Sums Divisible by K

Difficulty: Medium
Topics  : array, hash table, prefix sum

## Problem

Given an integer array `nums` and an integer `k`, return the number of non-empty contiguous subarrays whose sum is divisible by `k`. Values may be negative.

## Approach

This is 523 with the question changed from *does one exist* to *how many are there*. The reduction is identical: a slice `(j, i]` is divisible by `k` exactly when `prefix[i]` and `prefix[j]` leave the same remainder mod `k`, since the multiples of `k` cancel in the subtraction. So carry the running prefix sum mod `k` and look for matches.

What changes is the value stored in the map. 523 keeps the *first* index for each remainder, because it needs the widest window to clear a length constraint. Here there is no width constraint and every match is a separate answer, so the map keeps a *frequency*: when the running remainder is seen, every earlier prefix with that remainder closes one divisible subarray ending at the current index, so add the count and then increment it. Seed with `{0: 1}` for the empty prefix, which is what lets a prefix that is already divisible count on its own.

Because there are only `k` distinct remainders the map can be a plain list of length `k`, which is the alt worth keeping — it makes the O(k) space bound explicit rather than incidental.

The negative-value case is the one trap. Python's `%` returns a non-negative result for a positive modulus, so `-3 % 5 == 2` and nothing needs fixing. In a language with truncated division the same line silently splits one remainder class into two and undercounts; the fix there is `((x % k) + k) % k`.

There is also a non-incremental way to see the answer. Any two prefixes sharing a remainder define a divisible slice, so the total is the sum of `C(c, 2)` over the buckets. Counting as we go and counting at the end agree, which is a useful check that the answer depends only on the bucket sizes and not on the order of the array.

## Complexity

Time O(n) for the single pass, space O(k) for the remainder buckets.

## Files

- `python/solution.py`
