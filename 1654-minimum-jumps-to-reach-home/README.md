# 1654. Minimum Jumps to Reach Home

Difficulty: Medium
Topics  : BFS with a second coordinate that has two values, the can-still-jump-back bar as 2093's bar at its smallest, how far past the target the search has to be allowed to stand, and a queue order that hides the one-mark bug

## Problem

A bug starts at 0 and wants to reach `x`. It jumps `a` forward or `b` backward,
never backward twice in a row, never onto a `forbidden` position and never
below 0. It may pass `x` and come back. Return the fewest jumps, or -1.

## Approach

The state is `(position, arrived by a backward jump)`. Like 2093's discounts
left, the second coordinate has a direction: an arrival by a forward jump can
do everything an arrival by a backward jump can. So one bar per position is
enough, whether an arrival that may still jump back has been queued there, and
a backward arrival is dropped when one has. Every jump costs 1, so the queue
is in cost order from the moment of the push and the bar can be set at the
push, which 2093 could not do.

The part with no counterpart in the earlier problems is that the graph is
infinite. The search needs a furthest position it may stand on, and the answer
depends on it.

## Exhaustive, against a layer oracle

The oracle keeps each layer, every `(position, flag)` some `k` jumps can stand
on, as two bitsets, marks nothing as visited and runs for as many layers as
there are states. Its own cap is 120, and moving it to 400 changes 0 of 20000
answers.

Every `a`, `b` in 1..6, `x` in 1..10 and every forbidden subset of 1..10 without
`x`: 184320 instances, 42475 with an answer, 25534 of those with `a >= b`.

| search | wrong | share of the answerable |
|---|---|---|
| layered, two marks per position | 0 | |
| one bar per position | 0 | |
| one mark per position, forward jump queued first | 1767 | 4.16% |
| one mark per position, backward jump queued first | 0 | |

| furthest position allowed | wrong | share | wrong with `a >= b` |
|---|---|---|---|
| `x + b` | 427 | 1.01% | 0 |
| `max(x, F) + b` | 269 | 0.63% | 0 |
| `max(x, F) + a` | 688 | 1.62% | 0 |
| `max(x, F) + a + b - 1` | 0 | | 0 |
| `max(x, F) + a + b` | 0 | | 0 |

Random instances with forbidden positions past `x`, wrong counts:

| a, b up to | x up to | forbidden | answerable | one mark, forward first | one mark, back first | cap `x + b` | cap `max + a + b - 1` |
|---|---|---|---|---|---|---|---|
| 8 | 30 | 10 in 1..40 | 5520 | 1107 (20%) | 0 | 122 (2.2%) | 0 |
| 12 | 40 | 25 in 1..60 | 2595 | 335 (13%) | 0 | 59 (2.3%) | 0 |
| 20 | 100 | 60 in 1..150 | 697 | 138 (20%) | 0 | 21 (3.0%) | 0 |
| 50 | 300 | 100 in 1..400 | 342 | 185 (54%) | 0 | 17 (5.0%) | 0 |

## What the columns say

- **One mark per position** loses the forward arrival when a backward one got
  there first. The smallest failure has nothing forbidden: `a = 3`, `b = 2`,
  `x = 2`. The route is 0, 3, 1, 4, 2. The search reaches 4 from 6 by a
  backward jump before it reaches 4 from 1 by a forward one, both on the third
  jump, the mark goes to the arrival that cannot jump back, and it says -1.
- **The same search with the backward jump queued first is never wrong**, on
  the 42475 above, the 9154 in the random table and 92395 more with `a`, `b` up
  to 14, where the forward-first order is wrong on 31%. I do not have the
  argument. It is not that the two arrivals always tie, since the bar saves
  only 7.5% of the pops. A solution written in that order passes every test
  and carries the bug.
- **With `a >= b` nothing past `x + b` is ever needed**, and no cap in the
  table is wrong there. Every failure of a short cap is an instance with
  `a < b`, where the bug has to build up forward jumps before it can afford a
  backward one.
- **The cap `max(x, F) + a + b` is reached, but not in the first table.** With
  `a`, `b` up to 6 the most any instance needs is `a + b - 1` past `max(x, F)`.
  Over every `a < b <= 8`, `x` in 1..16 and at most two forbidden positions,
  5 of the 28 pairs need all of it and the cap one short is wrong on 112 of
  26692. The smallest is `a = 3`, `b = 7`, `x = 1` with 2 forbidden: 0, 3, 6,
  9, 12, 5, 8, 1, since 9 cannot jump back onto 2. The pairs are (3, 7), (3, 8),
  (4, 7), (5, 7), (5, 8). I do not know what they share.
- **Most instances need no room at all.** 82% of the answerable ones are
  solved without standing anywhere near `max(x, F)`, 9.8% need exactly that
  far, and 8.6% need to go past it.

## At the statement's size

`a`, `b`, `x <= 2000` and up to 1000 forbidden positions `<= 2000`. The cap is
at most 6000, which is where the 6000 in most solutions comes from. The worst
row is `a = 1998`, `b = 1999`, `x = 2000` with nothing forbidden: 3994 jumps,
7987 states, 0.002s. The bar saves nothing there, 7987 pops either way. With
several hundred positions forbidden most instances end within 8 pops.

## What I had wrong

Six predictions written before the run. Four right, two half.

- **Right:** the layered search with cap `max(x, F) + a + b` matches the oracle
  everywhere.
- **Half:** one mark per position wrong on about 10%. 4.2% exhaustively and
  13% to 54% on random instances, and 0% in the other queue order, which I had
  not thought to separate.
- **Half:** cap `x + b` wrong on about 5%. 1.0% exhaustively, 2.2% to 5.0% on
  random instances.
- **Right:** some instance needs the whole of `a + b`. None with `a`, `b` up to
  6, which is the range I enumerated first and would have reported from.
- **Right:** with `a >= b` nothing past `x + b` is needed.
- **Right:** the bar saves under 20% of the pops. 7.5%.

## Bounds

`O(max(x, F) + a + b)` time and space, two states per position in the layered
search and one bar per position in the other. The oracle is
`O(cap)` bitset operations of `cap` bits each.

## Files

- `python/solution.py`
