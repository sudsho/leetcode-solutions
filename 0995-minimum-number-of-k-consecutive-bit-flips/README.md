# 995. Minimum Number of K Consecutive Bit Flips

Difficulty: Hard
Topics: array, bit-manipulation, queue, sliding-window, prefix-sum, greedy

## Problem

Given a binary array `nums` and an integer `k`, one operation picks any
contiguous subarray of length exactly `k` and flips every bit in it (0 to 1,
1 to 0). Return the minimum number of operations to make every element 1, or
`-1` if it is impossible.

## Approach

Greedy, left to right. Index 0 can only be corrected by a window starting at 0,
since no window can start earlier. More generally, by the time the sweep reaches
index `i`, every window that could affect an earlier index has already been
decided, so if `nums[i]` still reads 0 the only legal fix is to begin a fresh
window at `i`. That makes the choice at each position forced - hence optimal -
and the answer is just the count of windows we are forced to open.

The remaining problem is reading off the *current* value of `nums[i]` without
re-flipping ranges. Keep a queue of the start indices of windows that still
cover the current position; a window started at `j` stops covering `i` once
`i >= j + k`, so expire those from the front. The parity of the queue length is
the net flip applied to `nums[i]`, because an even number of overlapping flips
cancels. The effective bit is `nums[i] XOR (parity)`; when it is 0 we must open
a window at `i`, but only if `i + k <= n` - otherwise the window would run off
the end and the configuration is impossible, so return `-1`.

(The same idea can be written with a difference array instead of a queue: a
`+1` at the flip start and a `-1` at `start + k`, with a running prefix sum
giving the live parity. The queue version makes the "which windows are still
active" bookkeeping explicit.)

## Complexity

Time O(n): each index is visited once and each window is pushed and popped from
the queue at most once. Space O(k) for the queue of active window starts.

## Files

- `python/solution.py`
