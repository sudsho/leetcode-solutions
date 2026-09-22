# 1631. Path With Minimum Effort

Difficulty: Medium
Topics  : Dijkstra where the relation is a max, a union-find that needs no settle at all, and an early exit that the max makes worse rather than better

## Problem

A grid of heights. A route from the top-left cell to the bottom-right one moves
up, down, left or right, and its effort is the largest absolute height
difference between two consecutive cells on it. Return the least effort.

## Approach

Dijkstra with the sum replaced by a max:

```python
nxt = max(e, w)
if nxt < best.get((nr, nc), inf):
    best[(nr, nc)] = nxt
    heapq.heappush(heap, (nxt, nr, nc))
```

The 20th ended on the settle argument resting on the update not improving a
value, and not on addition. `max(e, w) >= e` is non-improving, so a cell popped
at `e` is final for the same reason. What is new is that the max is idempotent:
most of the time `max(e, w) == e` and the relaxation writes the popped value
straight through, so whole regions of the grid settle at one value.

Two alternatives that do not settle anything. A minimax route between two cells
can always be taken inside a minimum spanning tree, so Kruskal with a union-find,
stopped when the corners join, returns the last edge it added. And the answer is
monotone in a limit, so a binary search over the limit with a BFS over steps
`<= limit` finds it too.

## Exhaustive, against every simple route

The oracle enumerates every simple route between the corners and keeps the best
max, the best sum and how many routes attain the best max. Both relations are
non-decreasing along a route, so a repeated cell never helps and the simple
routes hold the answers.

| shape | heights | grids | tied best routes | dijkstra wrong | union-find wrong | bisect wrong | right/down wrong (too big) | on-push wrong, max | on-push wrong, sum |
|---|---|---|---|---|---|---|---|---|---|
| 2x2 | 0..3 | 256 | 100 | 0 | 0 | 0 | 0 (0) | 26 | 10 |
| 2x3 | 0..2 | 729 | 541 | 0 | 0 | 0 | 2 (2) | 56 | 22 |
| 3x3 | 0..2 | 19683 | 17363 | 0 | 0 | 0 | 44 (44) | 1900 | 706 |
| 2x5 | 0..2 | 59049 | 55469 | 0 | 0 | 0 | 1930 (1930) | 3870 | 1598 |
| 3x4 | 0, 1 | 4096 | 3866 | 0 | 0 | 0 | 0 (0) | 0 | 0 |

The sum form is asserted against the oracle's best sum on every one of them.
On random grids the three methods agree on 2000 at 10x10, 300 at 30x30 and 20 at
100x100 with heights to 10^6.

88% of the 3x3 grids have more than one route attaining the best effort. With a
max, a tie is the normal case and not the exception, and the answer is a scalar,
so as in 1514 there is nothing for a tie-break to change.

## Right and down only

The DP that only moves right and down searches a subset of the routes, so it can
only be too big, and it is never too small anywhere. How often it is wrong
depends mostly on how much room a detour has:

| grids | right/down wrong |
|---|---|
| 3x3, heights 0..2 | 44 of 19683, 0.2% |
| 2x5, heights 0..2 | 1930 of 59049, 3.3% |
| random 10x10, 1..10 | 271 of 2000, 13.6% |
| random 30x30, 1..1000 | 148 of 300 |
| random 100x100, 1..10^6 | 12 of 20 |

The smallest kind of case, at 3x3:

```
0 0 1
0 2 2
2 1 0
```

Right and down gives 2. The answer is 1, along the top row, down to the 2 on the
right, left onto the middle 2, and down through the 1, which needs one step to
the left.

## Returning when the corner is first written

For a sum this early exit is known to be wrong: the first write to the target
comes from whichever neighbour settles first, and its last step is not
controlled. I expected the max to make it rarer, because `max(e, w)` forgives a
large `w` whenever `e` is already larger. It makes it more common, 1900 against
706 on the 3x3 grids and 3870 against 1598 at 2x5.

The plateaus are why. With a max, the corner's two neighbours often settle at
the same value and the heap picks between them by position. Of the 3x3
failures, all 706 of the sum's and 1552 of the max's 1900 have the two
neighbours settled at the same value. The idempotence that makes the settle
cheap is the same thing that leaves the order of the pops uninformative.

## At the statement's size

100x100 with heights to 10^6: Dijkstra 0.03s, union-find 0.02s, binary search
0.28s. A snake of walls whose only flat route is about 5000 cells long: 0.02s,
0.01s and 0.16s, all returning 0.

## What I had wrong

Five predictions written before the run. Three right, two half.

- **Right:** Dijkstra on the max matches the simple-route oracle on every grid
  enumerated, 83813 of them.
- **Right:** union-find and binary search agree with it everywhere, random
  100x100 included.
- **Right:** under 1s at the statement's size. 0.03s.
- **Half:** right and down only ever too big, right. Wrong on more than 10% of
  the 3x3 grids, wrong, 0.2%. It gets past 10% only at 10x10.
- **Half:** returning on the first write to the corner wrong for both relations,
  right. Less often for the max, wrong, 2.7x more often.

## Bounds

`O(rc log(rc))` time and `O(rc)` space for Dijkstra and for Kruskal, which sorts
the `2rc` edges. The binary search is `O(rc log H)` with H the height range.

## Files

- `python/solution.py`
