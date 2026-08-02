# 2251. Number of Flowers in Full Bloom

Difficulty: Medium
Topics  : array, binary search, prefix sum, sorting

## Problem

Given `flowers[i] = [start, end]`, the inclusive interval during which flower `i` is in bloom, and an array `people` of arrival times, return for each person how many flowers are blooming when they arrive.

## Approach

Reads exactly like the difference-array problems from Friday — range updates of `+1` over `[start, end]`, then read the value at a point — right up until the constraints, where the times run to `10^9`. There is no array to allocate, which is the case the notes flagged and never actually hit.

The fix is to go back to what the accumulate was computing. The value at position `t` is the prefix sum of the diff array up to `t`, and every entry of that diff array is `+1` at some `start` or `-1` past some `end`. So the prefix sum at `t` is just *(how many starts are ≤ t)* minus *(how many ends are behind t)* — two counts in two sorted lists, and a count in a sorted list is a binary search. The technique survives unbounded coordinates by never materializing the array and querying the prefix directly.

The two bisects are deliberately different. `bisect_right(starts, t)` counts `start <= t`; `bisect_left(ends, t)` counts `end < t`, the ones already finished. That asymmetry is the inclusive-vs-half-open decision that the array version encodes in *where the closing write goes* — same choice, relocated. Use `bisect_right` on both and every flower wilting exactly at `t` silently disappears.

The alternate is the offline sweep: sort the people, walk the flowers, keep the open ones in a min-heap keyed by end time. Worth keeping not because it is faster (it isn't) but because it degrades better — if the question were *which* flowers rather than *how many*, the counting version gives nothing and the heap hands over the open set. The heap is again holding the range updates that have not closed yet, which is what the array's unaccumulated tail does implicitly.

## Complexity

Time O(n log n + m log n) for n flowers and m people — the sorts, then one binary search per person. Space O(n) for the two sorted lists. The sweep variant is the same bound with an extra O(m log m) to sort the queries. Brute force is O(n · m), which at n, m ≤ 5 · 10⁴ is 2.5 billion comparisons.

## Files

- `python/solution.py`
