# 2536. Increment Submatrices by One

Difficulty: Medium
Topics  : array, matrix, prefix sum

## Problem

Start from an `n x n` zero matrix. Each `queries[i] = [row1, col1, row2, col2]` adds `1` to every cell of the inclusive submatrix with those corners. Return the matrix after all queries.

## Approach

The last two problems were both the difference array failing. 699 failed on composition, since the update read the state it was about to write. 2158 failed on attribution, since the coverage count was perfectly computable and answered a different question than the one asked. This one is deliberately the opposite case: the question is exactly what the accumulator produces, how much landed on each cell, only asked over a grid. So it tests how far the same machinery stretches rather than where it stops.

It stretches by being run once per axis, and that is the entire content of the 2d version. Sweep each row into a prefix sum, then sweep each column, and the value at `(r, c)` is the sum of every delta weakly north-west of it. The writes then have to be placed so that exactly the query rectangle nets `+1`. In 1d that was `+1` at the open end and `-1` past the close. In 2d it is those two writes per axis multiplied out, which is the four corners of inclusion-exclusion: `+1` at `(r1, c1)`, `-1` at `(r1, c2+1)` and `(r2+1, c1)` to cancel the strips extending right and down, and `+1` back at `(r2+1, c2+1)` for the quadrant just cancelled twice.

The fourth write is the one to drop by accident, and dropping it does not corrupt the rectangle itself. It corrupts the cells to the south-east, which is the region a small hand-checked example is least likely to contain.

Closing writes at `c2 + 1` and `r2 + 1` because the bounds are inclusive. That is the seventh syntax for the inclusive-vs-half-open decision in about a week and a half, and the first time it has shown up twice inside one problem, once per axis. Two independent copies of the same call in the same function is reassuring rather than repetitive: it means the decision really does belong to the range semantics and not to the dimension count.

The single-pass alternate accumulates with `grid[r][c] = diff[r][c] + grid[r-1][c] + grid[r][c-1] - grid[r-1][c-1]` instead of two separable sweeps. It is worth having written down because the read side turns out to be four-corner inclusion-exclusion for exactly the reason the write side was, the two neighbouring quadrants double-count the one to their north-west. Same identity, same four terms, once placing the deltas and once consuming them. That is also the shape of the 2d Fenwick tree in 308 and the band collapse in 1074, both of which had been filed as prefix-sum facts. They are not. They are one statement about rectangles, and the difference array and the prefix sum are its two directions.

The separable version is still the primary, because two independent 1d sweeps is a *claim* that the second axis introduces nothing new, and that claim is the result here. The recurrence hides it behind something that reads like a fact about 2d needing to be memorized on its own terms.

The row-wise alternate is the one that isolates what the second axis actually buys. It runs a plain 1d difference array on each row a query spans, which is 1109 applied `r2 - r1 + 1` times, and it is already correct. Its only flaw is that a full-height query costs `n` writes instead of 4. The 2d version computes nothing this one cannot, it defers the vertical spreading into a column sweep that every cell pays for anyway. So the saving is not a better idea about rectangles, it is noticing that the work is already being done for free. Break-even is `q * n` against `n^2`, so this version only loses once `q` reaches `n`, which at these bounds it does.

## Complexity

Two-pass 2d: `O(q + n²)` time, `O(n²)` space. Single-pass: identical. Row-wise 1d: `O(q·n + n²)` time, `O(n²)` space. Brute force: `O(q·n²)` time.

## Files

- `python/solution.py`
