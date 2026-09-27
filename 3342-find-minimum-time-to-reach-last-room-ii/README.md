# 3342. Find Minimum Time to Reach Last Room II

Difficulty: Medium
Topics  : Dijkstra where the next edge's cost depends on how many edges came before, why the cell alone is still a big enough state on a grid, and what goes wrong once the grid stops being bipartite

## Problem

An `n x m` grid of rooms. `moveTime[i][j]` is the earliest time a move into room
`(i, j)` may start. From `(0, 0)` at time 0, moves go to an edge-adjacent room
and cost 1 and 2 seconds alternately, starting with 1. Return the earliest time
`(n - 1, m - 1)` can be reached.

## Approach

A move into `(a, b)` as move number k, from a room reached at time t, arrives at

```python
max(t, moveTime[a][b]) + (1 if k % 2 == 0 else 2)
```

Waiting is allowed, and this is non-decreasing in t, so arriving earlier is
never worse for the same next cost. That is the settle argument's condition
from the last week of this log. What is new is that the next cost is not a
property of the edge. It depends on the parity of the move count, so two
arrivals at the same cell are only comparable if they pay the same next step,
and the honest state is `(cell, parity)`.

On a 4-neighbour grid the parity of every walk into `(i, j)` is the parity of
`i + j`, because the grid is bipartite. So the cell alone determines the parity
and Dijkstra on the cell is the `(cell, parity)` search with half its states
never reached. The solution runs on the cell.

## Exhaustive, against the walk-length oracle

The oracle settles nothing. `at[L][cell]` is the earliest arrival over walks of
exactly L moves, built from `at[L - 1]` by one step, which is exact because
arrival is non-decreasing in t. The answer is the minimum over L up to
`2 * cells + 2`, past which a walk repeats a `(cell, parity)` pair and the loop
can be cut out. King is the same problem with the four diagonal moves added,
where a triangle of moves exists and parity is no longer a function of the cell.

| shape | moveTime in | grids | cell | (cell, parity) | king, cell | king, (cell, parity) | gate as arrival | first move 2 | right/down only | answer needs a wait |
|---|---|---|---|---|---|---|---|---|---|---|
| 1x2 | 0..6 | 7 | 0 | 0 | 0 | 0 | 6 | 7 | 0 | 6 |
| 2x2 | 0..6 | 343 | 0 | 0 | 0 | 0 | 317 | 155 | 0 | 317 |
| 2x3 | 0..5 | 7776 | 0 | 0 | 800 | 0 | 7056 | 5868 | 0 | 7056 |
| 3x3 | 0..3 | 65536 | 0 | 0 | 1280 | 0 | 43520 | 7360 | 0 | 43520 |

Random grids, `moveTime[0][0] = 0`:

| shape | moveTime in | grids | cell wrong | king, cell wrong | king, (cell, parity) wrong | right/down only wrong |
|---|---|---|---|---|---|---|
| 4x4 | 0..20 | 2000 | 0 | 205 | 0 | 0 |
| 6x6 | 0..40 | 500 | 0 | 60 | 0 | 10 |
| 10x10 | 0..100 | 100 | 0 | 12 | 0 | 12 |

## What the columns say

- **The cell is enough on the grid and not off it.** Zero wrong everywhere on
  4 neighbours. With diagonals the cell-only search is wrong on 10% of 2x3
  grids, 2% at 3x3 with small gates and 10-12% on the random ones, and keeping
  the parity fixes every one of them. What goes wrong is an early arrival
  that owes the 2-second step shadowing a later one that owes the 1.
- **The gate as an arrival bound.** Reading `moveTime` as the earliest arrival,
  `max(t + cost, gate)`, is never later than the right answer and is wrong on
  exactly as many grids as need a wait, 43520 of 65536 at 3x3. That is the
  two formulas agreeing when `gate <= t` and differing by the step cost when
  the walker has to wait, so the equal counts are the expected thing and not a
  coincidence of the enumeration.
- **Starting with the 2-second move** changes the answer on 11% of 3x3 grids
  and 75% of 2x3 grids, and the swing is parity: an odd number of moves pays
  one more second, which a wait at the right room can absorb.
- **Right and down only.** Every such walk has `r + c - 2` moves, so the costs
  are fixed and only the waits vary. It is never wrong up to 4x4, and none in
  200000 random grids from 2x3 to 4x4 with gates up to 50 either. A detour
  costs two more moves, 3 seconds, and has to get round a gate, which needs
  room. It is wrong on 2% at 6x6 and 12% at 10x10.

## At the statement's size

750 x 750, all zeros: answer 2247 in 1.97s, which is 1498 moves, 749 pairs
at 3 seconds each. Random gates up to 10^9: 619325164 in 1.41s, faster because the
heap stops as soon as the corner pops and large gates make the frontier thin.

## What I had wrong

Five predictions written before the run. One right, two half, two wrong.

- **Right:** Dijkstra on the cell matches the oracle on the grid.
- **Half:** the cell alone wrong on about 5% with diagonals. 2% at 3x3 and 10%
  or more elsewhere, so the size of the gates matters more than I allowed.
- **Wrong:** the gate-as-arrival reading wrong on about 30%. It is 66% at 3x3,
  because it is wrong whenever a wait is needed and most small grids need one.
- **Half:** the first-move-2 reading changing about half the answers. 11% to
  75% depending on the shape's parity.
- **Wrong:** right and down only wrong on about 10% at 3x3, the same share as
  1631. It is never wrong at 3x3. In 1631 a detour only has to find a flatter
  edge. Here it pays 3 seconds before it saves anything.

## Bounds

`O(nm log nm)` time and `O(nm)` space. On a non-bipartite move set the
`(cell, parity)` search doubles both.

## Files

- `python/solution.py`
