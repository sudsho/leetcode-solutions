# 3568. Minimum Moves to Clean the Classroom

Difficulty: Medium
Topics  : BFS on (cell, litter mask, energy), the dominance mark that holds the most energy per (cell, mask), and one mark per (cell, mask) against it

## Problem

A grid with a start `S`, litter `L`, reset cells `R`, walls `X` and empty
cells `.`. The student starts with `energy`, every move costs one, a move
onto a reset cell refills to the start value, and a move needs energy left
to make it. Return the fewest moves that pick up every litter, or -1.

## Approach

The state is `(cell, litter mask, energy)` and a plain BFS by moves on it is
the real search. The standard solution is the same BFS with one entry per
`(cell, mask)` holding the most energy seen there, reopened when a later
arrival brings more: the dominance mark. It is checked against the full
state search on every board below.

1824 left the drift guess and a column: the first arrival is harmless when
the walk round is free, costs when it is priced, and says -1 when it is cut.
1263 cut the walk with a box, 1824 with a missing lane. Here the fine
coordinate is a budget, so the walk round is cut by running out, and one mark
per `(cell, mask)`, the first arrival claims it and every later arrival is
refused, is 1263's mark with the energy ignored. A third mark claims the cell
alone and ignores the mask too, which is 864's mistake.

Each refusal in the one-mark run is recorded with its move count, and
checked against the true distance of the refused state from the real search,
so drift, one mark's own count above the true one, is counted directly.

## Exhaustive and random

Every board with `S` in the corner, the other cells from `. X L R`, at most
three litter. The solution matches the full search on all of them, and the
random boards below.

| board | energy | solvable | one mark per (cell, mask) wrong | says -1 | too long | drifted refusals |
|---|---|---|---|---|---|---|
| 2 x 3 | 2 | 783 | 8 | 7 | 1 | 0 of 147 |
| 2 x 4 | 2 | 9241 | 249 | 187 | 62 | 1 of 4349 |
| 2 x 4 | 3 | 11562 | 231 | 146 | 85 | 35 of 8936 |
| 3 x 3 | 2 | 36171 | 1504 | 1211 | 293 | 5 of 21333 |
| 3 x 3 | 3 | 45398 | 1687 | 1383 | 304 | 376 of 44259 |
| 3 x 3 | 4 | 49149 | 651 | 525 | 126 | 322 of 53035 |
| 3 x 3 | 6 | 50204 | 17 | 17 | 0 | 27 of 55504 |
| 3 x 3 | 20 | 50261 | 0 | 0 | 0 | 23 of 55987 |

2000 random boards at each size with three litter, a fifth walls and a tenth
resets: at energy 4 one mark is wrong on 241 of 960 solvable 4 x 4 boards,
277 of 720 at 5 x 5 and 261 of 566 at 6 x 6; at energy 8 on 27, 198 and 423;
at energy 16 on 0, 0 and 13. The -1 share runs 64% to 82% across every row.

## What the columns say

- **The budget cuts, and a cut refusal needs no tie.** The witness is
  `SLR / L.R` at energy 2, answer 5. The arrival at the middle cell with the
  top litter taken comes at move 2 with no energy left and claims it. The
  arrival at move 4, with one energy after the two resets, is refused, and
  the board is lost. The refused state is two moves later than the claimer,
  not tied with it. 551 of the 1504 failures at 3 x 3 and energy 2 have no
  tie anywhere on the board in either search.
- **The tie count measured the board, not the claim.** I counted a board as
  tied if any `(cell, mask)` is first reached at one move count by two
  energies, which nearly every 6 x 6 board is, 407 of 423 failures. It says
  nothing about the failing refusal, so the prediction about ties at the
  claim is not decided by this run. The one thing it does show: a refusal at
  equal count in one mark's run never happened on a board the real search
  does not tie on, zero on every row.
- **The counts barely drift.** One mark's move count for a refused state is
  above that state's true distance on 0 of 147 refusals at 2 x 3, 376 of
  44259 at 3 x 3 and energy 3, and 2850 of 70460 on random 6 x 6 at energy
  8: under 4% everywhere. So if 1824's non-tie failures are drift, it is
  drift of a kind this budget does not produce.
- **The mask is most of the mark.** One mark per cell with the mask ignored
  is wrong on 11139 of the 29050 solvable 3 x 3 boards with two or more
  litter at energy 20, where the budget never binds, 38%, and on 72% to 85%
  of the random 4 x 4 to 6 x 6 boards at energy 16. A small board leaves
  little room for the second litter to be on the wrong side of the first.
- **Energy ends it.** At energy 6 on a 3 x 3 board one mark fails 17 times,
  all -1, and at 20 never: with enough energy no later arrival has anything
  the first did not, and the mark per `(cell, mask)` is exact, as it was for
  864's keys.

## At the statement's size

20 x 20 boards with ten litter and energy 50, five of them: the dominance
mark 1205 ms, the full state search 13055 ms.

## What I had wrong

Six predictions written before the run. One right, three half, two wrong.

- **Right:** the dominance mark matches the full state search everywhere.
- **Half:** the first-arrival mark fails on over 20% of solvable 3 x 3
  boards at the tightest energy and the share falls with energy. 4.2%, and
  it falls.
- **Half:** over 70% of its failures say -1. 73% to 82% on most rows, 64% on
  random 6 x 6 at energy 8.
- **Wrong:** under a quarter of failures have a real-search tie at the
  claim. The measure was board-wide and came out 63% to 96%.
- **Half:** one mark per cell is wrong on over half of solvable boards with
  two or more litter. 38% on the exhaustive 3 x 3, 72% to 85% on the random
  boards from 4 x 4 up.
- **Wrong:** drift on at least 10% of refusals. Under 4%.

## Bounds

`O(R C 2^L E)` states for the full search and `O(R C 2^L)` entries for the
dominance mark, four moves each. The exhaustive check is `4^(R C - 1)`
boards, so it stops at 3 x 3.

## Files

- `python/solution.py`: the dominance mark, the full state search, the two
  coarser marks with the refusal record, the drift check and the runs above,
  about two minutes.
