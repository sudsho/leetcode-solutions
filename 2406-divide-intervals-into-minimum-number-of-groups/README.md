# 2406. Divide Intervals Into Minimum Number of Groups

Difficulty: Medium
Topics  : array, greedy, sorting, heap, prefix sum

## Problem

Given `intervals[i] = [left_i, right_i]` (inclusive), divide the intervals into the minimum number of groups such that no two intervals in the same group intersect.

## Approach

The grouping is a red herring — two intervals have to be separated exactly when they overlap, so the answer is the size of the largest set of intervals that are all live simultaneously. For intervals specifically, pairwise overlap implies a *common* point (Helly in one dimension), so that set is always pinned to a single coordinate. The question is therefore: what is the maximum number of intervals covering any one point.

That is the difference array for the fifth time this week, and it is the first reading of the accumulator that is genuinely new. 1109 wanted its final value, 2848 wanted whether it was positive, 1094 wanted it compared against a bound at every step, 2381 wanted it reduced mod 26. This one wants its **maximum over the sweep** — watched the whole way like 1094, but reported at the end like 1109. Worth naming as its own entry because it needs the running total *kept*, not consumed at a point.

Endpoints are inclusive, so the cancelling write lands at `right + 1` and the array is sized `limit + 2` so the widest interval has somewhere real to put it. Same rule as the rest of the week: the technique promises two writes and an accumulate, the problem decides where the second write goes.

Two alternates, both earning their place. The heap version sorts by start and keeps one end time per open group — it is the only one that could actually *construct* an assignment rather than count one, and it makes the greedy legible: reusing a group whose last interval already ended is free, so open a new group only when none is reusable. Checking the earliest-ending group alone is sufficient, since if that one does not fit, none does.

The two-pointer version drops the heap by noticing the sweep never needs to know *which* interval opened or closed, only how many — so the pairing between a start and its own end can be discarded, which is what sorting the two endpoint columns independently does. That is the same collapse as 2251 viewed from the other end: there the two sorted endpoint lists got binary searched at `m` query points, here they get walked once because every point is a query point.

The strict comparisons in both alternates (`ends[0] < left`, `ends[j] < start`) are the inclusive-endpoint decision relocated again — intervals that merely touch at a point still overlap, so `<=` would merge two groups that conflict.

## Complexity

Time O(n + C) for the array sweep, where C is the coordinate bound, versus O(n log n) for the heap and two-pointer versions. With C = 10⁶ against n ≤ 10⁵ the array spends ten slots per interval to avoid the sort, which is the usual coordinate-space trade. Space O(C) and O(n) respectively. Brute force is O(n²).

## Files

- `python/solution.py`
