# 343. Integer Break

Difficulty: Medium
Topics: math, dynamic programming, greedy

## Problem

Given an integer `n`, break it into the sum of at least two positive integers
and maximize the product of those integers. Return the maximum product.

## Approach

Two ways in. The DP is the safe one: `dp[i]` is the best product for `i`, filled
by trying every first part `j` and pairing it with either the whole remainder or
its own best break, `max(i - j, dp[i - j])`.

The closed form is faster once you notice an optimal split never uses a part
bigger than 4 and favors 3s: `3 * (k - 3) > k` for any `k >= 5`, and 4 ties with
2+2. So use as many 3s as fit, then fix the remainder - a leftover 1 is folded
into a 3 to make two 2s, a leftover 2 stays a 2. `n = 2` and `n = 3` are capped
at 1 and 2 because the two-parts rule forces a 1 into the split.

## Complexity

Math: O(log n) for the exponentiation, O(1) extra space.
DP: O(n^2) time, O(n) space.

## Files

- `python/solution.py` - the O(log n) 3s-based closed form.
- `python/solution_alt.py` - the O(n^2) bottom-up DP.
