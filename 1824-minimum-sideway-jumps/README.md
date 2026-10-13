# 1824. Minimum Sideway Jumps

Difficulty: Medium
Topics  : 0-1 BFS on (point, lane), a three-lane DP, and one mark per point with the walk round made free, priced and cut

## Problem

A road of points `0..n` with three lanes. `obstacles[i]` is the lane blocked
at point `i`, or 0. The frog starts at point 0 in lane 2 and has to reach
point `n` in any lane. It can move forward one point in its lane if that lane
is clear at the next point, or jump sideways at its current point to any lane
clear there. Return the fewest sideways jumps.

## Approach

The answer is a three-number DP: carry each lane's count forward, set the
blocked lane to infinity, and let every clear lane take the smallest count
plus one. The search it is checked against is a 0-1 BFS on `(point, lane)`,
forward moves weighing 0 and jumps 1, and a second DP that relaxes the jumps
at each point as a shortest path on three lanes, so the same code can price
the jump at 0 or allow only neighbouring lanes.

1210 left a guess open, that one mark per box cell was harmless in 1263
because the player walks for free inside its component, so a first arrival
from the wrong side can walk round to the right one. Here the lanes at one
point play the component and a forward move plays the push. One mark per
point lets the first forward arrival claim the point, jump sideways inside it
from there, and refuses every later forward arrival. Three versions of the
walk round:

- **free walk**: a jump costs 0, so the component is free, as in 1263.
- **real, cost 1**: the statement, the walk round always exists and costs one.
- **adjacent only**: a jump goes to a neighbouring lane only, so an obstacle
  in lane 2 cuts lane 1 off from lane 3 at that point, the way the box cuts
  the player's region in 1263.

## Exhaustive and random

Every road with clear ends, `4^(n - 1)` of them.

| n | variant | roads | solvable | one mark wrong | too long | says -1 |
|---|---|---|---|---|---|---|
| 8 | free walk | 16384 | 16384 | 0 | 0 | 0 |
| 8 | real, cost 1 | 16384 | 16384 | 3410 | 3410 | 0 |
| 8 | adjacent only | 16384 | 13386 | 2942 | 420 | 2522 |
| 9 | free walk | 65536 | 65536 | 0 | 0 | 0 |
| 9 | real, cost 1 | 65536 | 65536 | 14998 | 14998 | 0 |
| 9 | adjacent only | 65536 | 51284 | 12329 | 1590 | 10739 |

On the real road the too-long answers at n = 9 are over by 1 on 13100, by 2
on 1806, by 3 on 91 and by 4 on one. 3000 random roads at n = 30 and 100 and
three obstacle rates give the same picture: free walk wrong on none, real
wrong on 981 to 2872, adjacent only on 14 to 1537. Both DPs match the BFS on
every road in every variant.

## What the columns say

- **A free walk makes the first arrival harmless.** 0 failures on 83,000
  exhaustive roads and 18,000 random ones. Any later arrival at a point is
  one the first could have walked to for nothing, so refusing it costs
  nothing.
- **Pricing the walk makes it cost, never -1.** At cost 1 the claimer can
  still reach every clear lane, so one mark never loses the road, and it is
  wrong on 21% to 23% of roads by answering long. The witness is
  `(0, 0, 2, 1, 0)`, answer 1. Lane 2 is blocked at point 2, so the frog
  jumps once either way, and lanes 1 and 3 both reach point 2 at one jump.
  Lane 1 is popped first and claims the point, lane 1 is blocked at point 3,
  and the claimer jumps again where the lane 3 frog would not have. Lane
  order decides that tie; the other orders were not run.
- **Cutting the walk is what makes it -1.** With neighbouring lanes only, 86%
  of the failures at n = 8 say -1, the way I expect 1263's did when the box
  split the player's region, though there I never split the failures by that.
- **The failures are not the real search's ties.** I expected a failure only
  where two forward arrivals reach a point at the same count. At n = 8 that
  covers 1501 of the 3410 failures. My guess is that one mark's own counts
  drift after its first refusal, so the tie that matters is in its run, not
  the real one. Not checked.

So the 1263 guess holds where it can be tested: the first arrival is
harmless exactly when the walk round is free, it costs when the walk is
priced, and it says -1 when the walk is cut.

## At the statement's size

`n = 5 * 10^5` at half obstacles, five roads. The DP 457 ms, the 0-1 BFS 1943 ms.

## What I had wrong

Six predictions written before the run. Two right, two half, two wrong.

- **Right:** both DPs match the BFS everywhere.
- **Right:** with a free walk one mark is never wrong.
- **Half:** at cost 1 one mark is wrong only on ties, by exactly 1, and never
  -1. Never -1 held. Over by up to 4, and 1501 of 3410 on ties.
- **Half:** adjacent only is wrong on more roads than the real one, some
  saying -1. Most say -1, but 2942 against 3410, fewer.
- **Wrong:** one mark wrong on under 5% of real roads at n = 8. 21%.
- **Wrong:** the 0-1 BFS within 3x of the DP. 4.3x.

## Bounds

`O(n)` time and `O(1)` space for the DP, `O(n)` states for the BFS. The
exhaustive check is `4^(n - 1)` roads, so it stops at n = 9.

## Files

- `python/solution.py`: the DP, the 0-1 BFS with and without one mark, the
  second DP, the three variants and the runs above, about 80 seconds.
