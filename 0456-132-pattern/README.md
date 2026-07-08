# 456. 132 Pattern

Difficulty: Medium
Topics  : array, binary search, stack, monotonic stack, ordered set

## Problem

Given a list of integers, decide whether there exist indices `i < j < k` such
that `nums[i] < nums[k] < nums[j]` - a "132" pattern (a low, then a high, then a
middle).

## Approach

Scan from the right with a monotonic-decreasing stack of candidate peak values
(the "3"). Track `third`, the largest value we have popped off the stack so far -
that is the best "2" (the middle), guaranteed to have a bigger element to its
right. For each new number from the right we first pop every stack entry smaller
than it, lifting `third` each time (the current number is a larger element to
their left, so they qualify as a "2"). The moment we see a number strictly below
`third`, it is a valid "1" sitting to the left of a complete 3-2 pair, so the
pattern exists.

## Complexity

Each element is pushed and popped at most once, so time O(n), space O(n).

## Files

- `python/solution.py`
