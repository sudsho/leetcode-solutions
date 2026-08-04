# 699. Falling Squares

Difficulty: Hard
Topics  : array, segment tree, ordered set, coordinate compression

## Problem

Squares are dropped one at a time onto a number line. `positions[i] = [left_i, sideLength_i]` gives a square occupying `[left_i, left_i + sideLength_i)`. Each square falls until it rests on the top of whatever is already beneath it, or on the line. Return `ans[i]` = the height of the tallest stack after the i-th square lands.

## Approach

This is where last week stops working, which is the reason to do it.

Every difference-array problem from 1109 through 2406 had range updates that were two writes and an accumulate, and that worked because the updates **composed**: additively, commutatively, and without reference to the current state. `+1` over `[a,b]` followed by `+1` over `[c,d]` is the same pile in either order, so the pile collapses into one running number and the individual updates never have to be stored.

Neither half of that survives here. The value a square writes is `(max height already under it) + side`, so the update *reads* the state it is about to modify — and what it writes is an **assignment**, which erases what was underneath rather than adding to it. Two squares dropped in the opposite order produce a different skyline. An order-dependent update cannot be summarized by an accumulator, so the structure has to hold the real heights and answer `query` before every `assign`. That is a segment tree with lazy propagation, over coordinates compressed down to the `2n` endpoints that actually appear.

The lazy tag is an assignment rather than an addition, which is a small but load-bearing difference. An add-tag composes with whatever tag is already sitting on the node; an assign-tag *replaces* it, and that is correct precisely because a landing square flattens everything it covers. It also means the tag has to be stored as `None`-or-value and not tested for truthiness, since a height of `0` is legitimate and would be silently skipped on the push.

Note that the interval is half-open: a square at `[left, left + side)` and one starting at exactly `left + side` touch at a point and do **not** stack. That is the same inclusive-vs-half-open decision as every sweep problem this week, appearing in its fifth distinct syntax — as an index offset in the array version, as a `bisect_left`/`bisect_right` choice in 2251, as `<` vs `<=` in 2406, and here as the `hi - 1` that decides which compressed gap the assignment stops at. Still not something reproducible from memory; still has to be re-derived from the range semantics.

The `O(n²)` brute force is the version worth writing first and is accepted on the real constraints (`n ≤ 1000`). It states the recurrence with nothing in the way: a square's top is its side plus the tallest overlapping square placed before it.

The third version keeps an explicit skyline of disjoint flat runs, splicing each drop in and trimming the segments it partially covers. It is not faster, but it is the only one holding the profile itself rather than a queryable summary of it — if the follow-up asked for the skyline after all the drops, or the area under it, this version already has the answer and the tree would have to be walked to rebuild one. Same counts-collapse-but-sets-do-not distinction that made the heap worth keeping in 2251 and 2406.

## Complexity

Segment tree `O(n log n)` time and `O(n)` space after compressing to the `2n` endpoints. Brute force and the skyline version are `O(n²)` time, `O(n)` space; both are comfortable at `n ≤ 1000` and the skyline one is usually the fastest of the three in practice at that size.

## Files

- `python/solution.py`
