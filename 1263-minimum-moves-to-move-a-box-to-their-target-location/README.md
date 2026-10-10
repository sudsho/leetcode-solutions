# 1263. Minimum Moves to Move a Box to Their Target Location

Difficulty: Hard
Topics  : BFS on (box, player), a second coordinate that is a quotient rather than an order, and where one mark per box cell can and cannot go wrong

## Problem

A grid up to 20 x 20 of walls `#`, floor `.`, one player `S`, one box `B` and
one target `T`. The player walks the floor freely and pushes the box by walking
into it, which needs the cell beyond the box to be floor. Return the fewest
pushes that put the box on the target, or -1.

## Approach

The state is `(box, player)`, a push costs 1 and a step costs nothing. After
the first push the player stands where the box was, so the textbook search
marks `(box, side)`, at most four per box cell, and flood-fills the player's
region at every pop to see which sides it can get behind.

847's mask was partly ordered and 1129's colour had no order at all. Here the
player's cell has something else: two cells in the same component, with the
box where it is, can walk to each other for free, so each stands in for the
other completely. The coordinate is a quotient, and the bar is one mark per
`(box, component)`. Two sides of the box in one component are one state. The
search labels the components once per box cell, the smallest index in each,
and a push becomes a table lookup instead of a flood fill.

## Exhaustive, against a layer oracle

Every wall set on the board with `S`, `B` and `T` on three distinct free
cells. The oracle keeps every layer as the set of `(box, player cell)` after
exactly k pushes, nothing marked across layers, and stops when a layer is empty
or repeats. The side search, the component search and a 0-1 BFS on
`(box, player cell)` agree with it on all of them.

| board | instances | one mark per box cell wrong |
|---|---|---|
| 2 x 4 | 10752 | 0 |
| 2 x 5 | 92160 | 28 (0.03%) |
| 3 x 3 | 32256 | 0 |

Random boards, 4000 at each size and wall density (1500 at 8 x 8), checked
against the 0-1 BFS and on 4 x 4 against the oracle too. Pops per instance.

| board | walls | one mark | side pops | component pops | cell pops | component saves |
|---|---|---|---|---|---|---|
| 4 x 4 | 0.00 | 0.00% | 3.7 | 3.1 | 61.5 | 15.4% |
| 4 x 4 | 0.20 | 0.03% | 2.3 | 2.2 | 28.7 | 7.5% |
| 4 x 4 | 0.35 | 0.00% | 1.6 | 1.6 | 13.4 | 2.8% |
| 6 x 6 | 0.00 | 0.00% | 14.2 | 8.1 | 371.0 | 42.8% |
| 6 x 6 | 0.20 | 0.20% | 7.3 | 5.2 | 170.7 | 28.5% |
| 6 x 6 | 0.35 | 0.25% | 3.1 | 2.6 | 54.0 | 15.2% |
| 8 x 8 | 0.00 | 0.00% | 38.5 | 17.1 | 1348.9 | 55.6% |
| 8 x 8 | 0.20 | 0.13% | 16.7 | 9.9 | 567.6 | 40.8% |
| 8 x 8 | 0.35 | 0.67% | 5.7 | 4.3 | 160.7 | 24.0% |

## What the columns say

- **One mark per box cell is almost always right**, and the reason is that the
  player's component rarely has two live values at one box cell. Its failure
  with the most walls on the exhaustive boards is `##...` over `STB..`, answer
  3. The player is shut in behind the box with the target, so the box has to go
  right once, the player walks round through the top row, and the box comes
  back left twice. The way back passes the box's start, which one mark has
  already spent on the arrival with the player on the wrong side. It says -1.
- **On 3 x 3 it cannot be wrong**, and there is an argument. A box on an edge
  cell can only be pushed along that edge, into a corner, and a box in a corner
  cannot be pushed at all. So the centre is only ever a start, an edge cell is
  the start or is reached from the centre with the player standing there, and a corner is
  a dead end where the player's side no longer matters. No box cell is ever
  reached with two player states that both matter.
- **Every failure is a return**, on every board tried. `self_avoiding` finds
  the fewest pushes over box paths that never stand on a cell twice, start
  included. On 2 x 5, 2 x 6 and 3 x 4, exhaustively, the boards with no such
  path at the optimum are exactly the boards one mark gets wrong, 28, 400 and
  60, and on all of them there is no self-avoiding path at any length and one
  mark says -1. On 3000 random boards at each of 5 x 5, 6 x 6 and 8 x 8 and
  three wall densities, all 30 failures need a return too. Half of this is
  forced: one mark's search tree is a self-avoiding path, so a board where
  every solution returns gets -1 from it. The other half, that a board with
  any self-avoiding solution gets the right count from it, I have only as a
  count.
- **That other half was wrong as stated.** On `#...#` / `...BS` / `..#T#` /
  `.....` / `##...` the player is shut in behind the box, so the fastest way
  is out one cell and back through the start, 3 pushes. A self-avoiding way
  round exists, 7 pushes, and one mark says 7. What held is narrower: one mark
  says the shortest self-avoiding count, whatever it is. That is equal on all
  92160 boards of 2 x 5 and all 675840 of 3 x 4, and on 13500 random boards
  from 4 x 4 to 6 x 6. Too-long answers are rare. A separate search of 192000
  random boards from 5 x 5 to 8 x 8 had 426 failures, 4 of them too long, and
  each was the shortest self-avoiding count. The old claim holds only where
  the shortest self-avoiding solution is also optimal. The forced half still
  stands: one mark's answer is at least the self-avoiding minimum. The other
  direction, that marking the first arrival never blocks a shorter
  self-avoiding path, is still only a count.
- **The order column came out flatter than the symmetry said.** The 24 push
  orders fall into orbits under the board's symmetries, three of eight on
  3 x 3 and six of four on 2 x 5, and relabelling says only that the count is
  constant on each orbit. It was constant on all of them, and on 2 x 5 all 24
  orders are wrong on the same 28 instances. In two rows the box only moves
  sideways, the cells it reaches are an interval grown outward from its start,
  and a new cell has one parent, so the order of the pushes never decides which
  arrival marks it.
- **The component bar saves more as the board opens up**, 56% of the side
  search's pops on an empty 8 x 8, where most box cells have every side in one
  component, and 3% on a 4 x 4 with a third of it walls.
- **The 0-1 BFS pops 20 to 80 times as often** and is no slower than the side
  search, because its pops are cheap and the side search's each carry a flood
  fill.

## At the statement's size

20 x 20, a fifth walls, 200 random instances. Side 43.3 ms each, component
25.4 ms, cell 41.1 ms.

## What I had wrong

Six predictions written before the run. One right, two half, three wrong.

- **Right:** the side, component and cell searches match the oracle everywhere.
- **Wrong:** one mark wrong on about 3% at 3 x 3. It cannot be wrong there.
- **Wrong:** one mark never wrong on two-row boards. 28 at 2 x 5, none at 2 x 4.
- **Half:** one count per symmetry orbit, and the three orbits at 3 x 3 differ.
  One count per orbit, and every orbit the same count.
- **Half:** the component bar saves about 20% of the pops at 6 x 6 with a fifth
  walls. 28.5%, and 3% to 56% across the table.
- **Wrong:** the component search at least twice as fast as the side search at
  20 x 20, and the cell search slowest. 1.7x, and the cell search is slightly
  faster than the side search.

## Bounds

With `N = m n` cells, the side search pops at most `4N` states and flood-fills
at each, `O(N^2)` time. The component search labels at most `N` box cells at
`O(N)` each and then does `O(1)` per push, also `O(N^2)` but with the flood
fills shared. The 0-1 BFS has `N^2` states and `O(1)` work each. The oracle can hold
`N^2` states a layer, for as many layers as come before a repeat.

## Files

- `python/solution.py`
