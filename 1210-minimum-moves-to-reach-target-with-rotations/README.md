# 1210. Minimum Moves to Reach Target with Rotations

Difficulty: Hard
Topics  : BFS on (tail, orientation), a DP that needs no queue, and one mark per head cell failing with no return to blame

## Problem

An `n x n` grid of 0s and 1s. A snake two cells long starts horizontal on
`(0, 0)` and `(0, 1)` and has to end horizontal on `(n - 1, n - 2)` and
`(n - 1, n - 1)`. It can move right or down by one if the cells it moves into
are 0, and it can turn clockwise from horizontal or counterclockwise from
vertical about its tail if the 2 x 2 block at the tail is all 0. Return the
fewest moves, or -1.

## Approach

The state is `(r, c, orientation)` with `(r, c)` the tail, at most `2 n^2`
states and four moves each, and a plain BFS marks each state once.

The oracle uses no queue. Right and down raise the tail's `r + c` by one and a
turn keeps the tail, so the tail cells can be taken in order of `r + c`, each
orientation's distance read off the cell above and the cell to the left, and
then the two orientations of one cell relaxed against each other through the
one block they share.

1263 left open why one mark per box cell never blocked a shorter self-avoiding
path. Here the same coarse bar is one mark per head cell, and every shortest
solution here keeps its head self-avoiding for free: `r + c` of the head never
falls, it only stays put across a turn, and turning twice in a row is wasted.
So any failure of one mark here is a first arrival from the wrong side on a
cell the snake never comes back to, which 1263 never produced.

## Exhaustive and random

| board | grids | solvable | need a turn | one mark per head cell wrong |
|---|---|---|---|---|
| 3 x 3 | 128 | 8 | 0 | 0 |
| 4 x 4 | 16384 | 368 | 64 | 64, on all 24 move orders |

Random grids at 20% walls, the boards that cannot be solved without a turn
and the share of them one mark gets wrong.

| board | need a turn | head mark wrong among them | wrong with no turn needed |
|---|---|---|---|
| 5 x 5 | 243 | 242 | 0 |
| 6 x 6 | 362 | 354 | 0 |
| 8 x 8 | 576 | 556 | 0 |

The DP oracle matches the BFS on every grid above and on 48000 more random
ones from 5 x 5 to 8 x 8 at four wall densities. Every head-mark failure says
-1, none answers too long.

## What the columns say

- **One mark per tail cell can never turn.** A turn keeps the tail, so the
  turned state finds its tail already marked. It is wrong on exactly the
  boards that need a turn, which makes it the control for the head column.
- **One mark per head cell is wrong on almost the same boards.** The witness
  is `0000 / 0010 / 1000 / 0000`, answer 7: turn at the start, go right, then
  down column 1. Going down from the start without turning puts a horizontal
  snake's head on `(1, 1)` at move 1, a dead end, and the turned snake gets
  its head there at move 2 and is refused. The turn's own 2 x 2 block is free,
  so a turn followed by a right move always loses its head cell to the snake
  that went down instead. Whether that covers every failure was not checked.
- **The move order does nothing**, 64 on all 24 orders at 4 x 4. Unlike
  1263's two-row boards this is not because a cell has one parent: the
  winning arrival is a whole move ahead, so the order inside a layer never
  gets to decide it.
- **So 1263's narrow claim is not about marking.** There one mark gave the
  shortest self-avoiding count on every board tried. Here the shortest
  solution is self-avoiding in the head on every board and one mark still
  says -1 on 96% to 100% of the boards that need a turn. Whatever kept the
  first arrival harmless in 1263 was something about that board, my guess
  the player walking for free inside a component, and not a property of
  marking first arrivals.

## At the statement's size

100 x 100, a tenth walls, 50 random grids. BFS 30.4 ms each, the DP 31.0 ms.

## What I had wrong

Six predictions written before the run. Three right, three wrong.

- **Right:** the DP oracle matches the BFS everywhere.
- **Right:** one mark per tail cell is wrong on exactly the boards that need a turn.
- **Right:** one mark per head cell fails, and none of its failures needs a
  return. The second half is forced by the moves.
- **Wrong:** head-mark failures as rare as 1263's, under 1% of solvable
  boards. 64 of 368 at 4 x 4, nearly every board that needs a turn.
- **Wrong:** some of the 24 move orders do better than others. All 64.
- **Wrong:** some failures answer too long, as 4 of 426 did on 1263. All -1.

## Bounds

`O(n^2)` states and `O(1)` work each for both the BFS and the DP. The
exhaustive check is `2^(n^2 - 2)` grids, so it stops at 4 x 4.

## Files

- `python/solution.py`: the BFS, the DP oracle, the two one-mark searches and
  the runs above, about 20 seconds.
