# 1552. Magnetic Force Between Two Balls

Difficulty: Medium
Topics  : array, binary search, greedy, sorting

## Problem

`position[i]` is the location of the `i`th basket on a line, and `m` balls have to be distributed into distinct baskets. The magnetic force between two balls is the distance between their baskets. Return the largest possible value of the minimum force over all pairs.

## Approach

2528 was a maximin the sweep could not answer directly, so binary search converted it into a feasibility question and the sweep became the oracle inside one. The same conversion works here - bisect on the gap, and "can `m` balls sit at these positions with every pair at least `gap` apart" is one left-to-right pass.

What differs is the direction the greedy pushes, and that turns out to be the entire content.

2528 pushed right. A station serving city `i` could sit anywhere in `[i-r, i+r]`, and the rightmost choice covered the longest suffix of what was still ahead. Here the greedy pulls left: a ball goes at the earliest position clearing the last one. The two are the same exchange argument rather than opposite ones - leave the most freedom for what has not been decided - and the direction flips only because the quantity extending forward changes sign. In 2528 it was coverage, a benefit, so extending it further was free. Here it is the occupied prefix, a cost, and every unit of line spent behind is a unit the remaining balls cannot use.

There is one genuine asymmetry. In 2528 rightmost was forced: pulling left loses solutions, because a station left of `i` covers less of what is ahead with no compensating gain. Here the mirror is legal. Reflecting the coordinates through zero reverses the order and preserves every pairwise distance, so the rightmost-anchored greedy is equally correct. `maxDistanceMirrored` is that claim as executable code, since the direction was the one thing that would not transfer from yesterday.

The feasibility pass folds two exchange claims that are easy to run together by accident. The **anchor** - some optimal arrangement uses `position[0]` - holds because sliding the leftmost ball of any valid arrangement down to `position[0]` changes one gap and only grows it. The **step** - take the earliest legal position - holds because a later choice leaves a shorter suffix for the remaining balls, so any arrangement built on it maps onto one built on the earlier choice.

Sorting is not bookkeeping here. 2528 handed over the geometry already in index order, so "further right" was a fact about the array; this input is an unordered set of coordinates and "as early as possible" means nothing until the order exists. Only consecutive gaps get checked, which is why the pass is linear rather than pairwise: once sorted, any non-adjacent pair is separated by at least the sum of the gaps between them.

The upper bound `(max - min) // (m - 1)` is pigeonhole - `m` balls in a span of `W` leave `m-1` gaps summing to at most `W`. It also removes a guard rather than adding one: the positions are distinct integers, so the span is at least `n-1 >= m-1` and the bound is never below the starting `low` of 1. The search range cannot come out empty.

The placement alternate returns a witness rather than *the* witness, same verdict as 2528 and now with a name for the ambiguity - the mirror returns a different placement on most inputs and is equally correct. So placements cannot be compared across callers, but the two directions must still agree on the answer, and that is a stronger check than replaying one greedy against itself. The adjacent-gap alternate covers `m == n`, the one input where the greedy makes no decision at all and the answer is just the minimum adjacent gap.

## Complexity

Primary: `O(n log n + n log W)` time where `W` is the coordinate span, `O(n)` space for the sort. Mirrored: identical. Placement: same plus `O(m)` for the witness. Adjacent: `O(n log n)` time.

## Files

- `python/solution.py`
