# 1109. Corporate Flight Bookings

Difficulty: Medium
Topics  : array, prefix sum

## Problem

There are `n` flights labelled `1` to `n`. Each booking `[first, last, seats]` reserves `seats` seats on every flight in the inclusive range `first..last`. Return an array where entry `i` is the total number of seats reserved on flight `i + 1`.

## Approach

Applying each booking directly is O(n) per booking and O(n · m) overall, which is the version that times out. The fix is to stop storing values and start storing the differences between neighbours. In a difference array `diff[i] = a[i] - a[i-1]`, adding a constant across a whole range only changes two entries: the value jumps up where the range starts and drops back down just past where it ends. A range update becomes O(1), and one prefix sum at the end reconstructs every value.

That makes this the mirror image of the last few weeks. Those problems all went values → prefix sums so that a range *query* was a subtraction of two entries. Here the range *update* is the frequent operation, so the array is stored pre-differenced and the prefix sum is the step that undoes it. Same pair of operations, opposite direction, and which one you precompute is decided by which one happens more often.

The indexing is where this actually goes wrong. Flights are 1-indexed and the array is not, so flight `f` sits at `f - 1` and the opening `+seats` lands at `first - 1`. The closing `-seats` goes at `last`, not `last - 1`, because it has to take effect on the first flight *outside* the range — the range is inclusive of `last`, so `last` itself must still see the seats. Allocating `n + 1` slots means a booking ending on the final flight writes its cancellation into a real index instead of needing a bounds check, and that last slot is never read back.

## Complexity

Time O(n + m) for m bookings — each booking is two writes, then one pass to accumulate. Space O(n) for the difference array, or O(1) beyond the output if you accumulate in place.

## Files

- `python/solution.py`
