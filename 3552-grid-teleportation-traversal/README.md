# 3552. Grid Teleportation Traversal

Difficulty: Medium
Topics  : 0-1 BFS over portal buckets, 1345's clear at zero cost, and 1345's counting replacement

## Problem

A grid of `'.'` (empty), `'#'` (wall) and uppercase letters (portals). Start at
`(0, 0)` and reach `(m - 1, n - 1)`, moving up, down, left or right onto cells
that are not walls. Standing on a portal whose letter you have not used, you may
teleport to any other cell with the same letter. A teleport is not a move, and
each letter can be used at most once. Return the minimum number of moves, or
`-1`.

## Approach

0-1 BFS. A move has weight 1 and goes to the back of the deque, a teleport has
weight 0 and goes to the front. Portals are held in buckets by letter, and the
first time any member of a letter is popped the whole bucket is expanded and
deleted.

## The line

```python
if ch in buckets:
    for rr, cc in buckets.pop(ch):
        ...
```

**It is also the rule.** Popping the bucket is "each letter at most once", so
deleting the line deletes a sentence of the statement, and
`min_moves(clear=False)` is the problem without it.

**Harmless for the minimum.** A shortest route never teleports on one letter
twice with a move in between, since the later teleport could have been taken
from the first portal, and two teleports in a row are never better than one.
Checked on every grid over `.#AB` of shape 2x3, 2x4 and 3x3 with a free start,
248832 grids, against an oracle whose state is `(cell, letters used)`, so the
rule cannot be deleted from it. Both programs equal it everywhere.

**Necessary.** One letter in every cell, `N` cells:

```
  N=    9  clear=     9  no clear=      81
  N=  100  clear=   100  no clear=   10000
  N=  900  clear=   900  no clear=  810000
  N= 3600  clear=  3600  no clear=12960000
```

Both asserted as identities. On random 60x60 grids with 10% walls and half the
cells portals:

```
  letters=26  ratio=   62.49x
  letters= 8  ratio=  203.13x
  letters= 3  ratio=  536.13x
  letters= 1  ratio= 1595.40x
```

About the mean class size, the way 1345's clear charged.

## Under counting

Count the shortest journeys, a journey being its sequence of moves and
teleports under the rule. 882's table, and the 12th's run of it on 1871 and
1345, says the rescan the clear skips reaches a `+=`, so keeping the clear is
the bug and deleting it is the fix. `count_moves` has two switches, the clear
and what a portal pop hands the other members of its letter.

| program                                  | 2x3 (2108 reachable) | 2x4 (33272)          | 3x3 (137097)         |
|------------------------------------------|----------------------|----------------------|----------------------|
| keep the clear, copy the pop's count     | 210, all under       | 5088, all under      | 26912, all under     |
| delete it, copy                          | 908, 826 over        | 20242, 19156 over    | 89306, 83840 over    |
| keep it, read the level's walking sum    | 0                    | 0                    | 0                    |
| delete it, same read as an overwrite     | 0                    | 0                    | 0                    |

The first row agrees with the table and the second does not. The last two say
the clear was never what went wrong.

## One level

A teleport costs nothing, so every portal of a letter is one teleport from the
first one popped and all of them sit at the same distance, asserted for every
letter with two reachable portals. A move into distance `d` is pushed by a pop
at `d - 1`, and the deque finishes every pop at `d - 1` before it starts one at
`d`. So at the first pop of a letter, the walking arrivals of all its members
are final. A journey into a member either walked in or teleported from another
member that walked in, because teleporting on from a teleport reuses the letter.
Every member's count is therefore one number, the sum over the letter's members
of their walked-in journeys, and they come out equal on all 209356 letters of
the 3x3 set.

`count_moves(read="walk_sum")` reads that sum once, at the first pop, which is
`O(k)` per letter with the clear kept. With the clear deleted every later pop
writes the same value again, an overwrite of an identical value, which 882's
table already lists as absorbing a repeat, so the line is complexity-only again.

The copy goes wrong both ways. At the first pop a member's own count is only its
own walked-in journeys, so with the clear kept the other members' walking
arrivals never get handed on, which is why that row only ever undercounts.
Without the clear, a later pop's count already includes teleports into it, so
copying it on is a second teleport on the same letter.

## 1345, from the same idea

The 12th said 1345 has no index order for 1871's prefix sums and left its
replacement unwritten. It does not need one. A 1345 bucket is one jump wide, so
its members span at most two levels, asserted on every array below, and when
its first member shows up in a frontier, the frontier's members of that value
are everything the bucket will ever hand on. `count_min_jumps_1345_by_levels`
sums them once and gives the sum to the members one level down, one pass per
bucket with the clear kept.

| program                          | 2 values to length 10 | 3 values to length 7 |
|----------------------------------|-----------------------|----------------------|
| one pass per bucket              | 0 of 1024             | 0 of 2187            |
| without the neighbour correction | 96                    | 312                  |

The correction: a member next to a frontier member of its own value is reached
by both the step and the jump, and those are one index sequence, so its own
neighbours come back out of the sum. On random arrays of length 60 with 60, 20,
8, 3 and 1 distinct values it is wrong on none, at most 2.97 scans per index.

So 1871's order was not the point. What the three counting programs needed was
to know when a class had finished contributing. 1871 got that from the index,
and 1345 and 3552 get it from the class being one jump wide.

## What I had wrong

**Keeping the clear and copying, wrong on more than half of the random 6x6 grids
a teleport shortens.**

```
  letters= 1 portals=0.2  reachable 300/400  teleport shortens 288  tie  36  keep+copy wrong  34 ( 33 shortened)
  letters= 2 portals=0.2  reachable 303/400  teleport shortens 283  tie  87  keep+copy wrong  47 ( 44 shortened)
  letters= 3 portals=0.3  reachable 321/400  teleport shortens 316  tie 162  keep+copy wrong  70 ( 69 shortened)
  letters= 6 portals=0.5  reachable 297/400  teleport shortens 297  tie 238  keep+copy wrong 102 (102 shortened)
  letters=26 portals=0.5  reachable 278/400  teleport shortens 254  tie  96  keep+copy wrong  21 ( 18 shortened)
```

11%, 16%, 22%, 34% and 7%. A teleport is not what the copy needs to go wrong.
It needs a tie, two portals of one letter both walked into at that letter's
level, since without one the pop's own walked-in count is the whole sum. With no
tie the copy is right at every reachable cell of every exhaustive grid, asserted,
and the random grids it gets wrong are inside the tied ones every time. A tie on
a letter that no shortest route to the target uses costs nothing, which is the
gap between the tie column and the wrong one.

## Bounds

`-1` when the target is a wall or cut off. `0` when the target is the start or
shares the start's letter. Otherwise at least 1 and at most `mn - 1`: a shortest
journey visits no cell twice, because the stretch between two visits either
holds a move, and cutting it is shorter, or holds only teleports, and two in a
row reuse a letter. With the clear a cell is pushed at most twice, once by a
move and once improved by a teleport, and each bucket is scanned once, so
`O(mn)`. Without it the bucket scans are the sum over popped portals of their
class sizes, `(mn)^2` with one letter everywhere. The count has no modulus
because nothing asks for one, and with no walls and no portals it is already
`C(m + n - 2, m - 1)`.

## Files

- `python/solution.py`
