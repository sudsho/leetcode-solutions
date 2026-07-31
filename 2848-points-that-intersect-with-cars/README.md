# 2848. Points That Intersect With Cars

Difficulty: Easy
Topics  : array, prefix sum, hash table

## Problem

Given `nums` where `nums[i] = [start_i, end_i]` marks a car parked on the inclusive range `start_i..end_i` of a number line, return how many integer points are covered by at least one car.

## Approach

The difference array from 1109 with the output question changed. There a range update carried a quantity and the accumulated value *was* the answer; here it carries a count of overlapping cars and the accumulated value is only ever consulted as a predicate — `running > 0` means the point is covered. Overlaps need no special handling because two cars over the same point push the running count to 2, which still reports as covered exactly once.

`+1` at `start` and `-1` at `end + 1`, same inclusive-range logic as before: the closing write has to land on the first point *outside* the range. The opening write needs no `- 1` this time, since points and indices are both 1-based here, which is a small reminder that the `first - 1` in 1109 was about that problem's 1-indexed flights and not part of the technique.

What makes this the easy one is `end <= 100`. The coordinate space is small and fixed, so an array can just span it — no coordinate compression, no sorting. Lift that constraint to `10^9` and the array approach dies, which is why the merge-intervals alt is worth keeping: sort by start, extend the current run while the next interval overlaps *or is adjacent* (`[1,3]` and `[4,5]` leave no integer gap, so they merge), and sum the run lengths. That one scales with the number of cars instead of the width of the line.

The `max(current_end, end)` in the merge is the easy thing to get wrong. Sorting by start says nothing about the ends, so `[1, 10]` followed by `[2, 3]` would otherwise shrink the run it was supposed to extend.

## Complexity

Difference array: time O(n + M) and space O(M) for coordinate bound M = 100. Merge: time O(n log n) for the sort, space O(1) beyond it. With M fixed and small the first is effectively linear, and it is the better choice only because the constraint is generous.

## Files

- `python/solution.py`
