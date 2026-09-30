# 864. Shortest Path to Get All Keys

Difficulty: Hard
Topics  : BFS with a second coordinate that is only partly ordered, an antichain of masks per cell as 2093's bar when no single number will do, the flattened bar that is wrong, and a bug the one-key case cannot show

## Problem

A grid with a start `@`, walls `#`, keys `a`..`f` and locks `A`..`F`. A lock
can be walked through only with its key in hand. Return the fewest moves that
collect every key, or -1.

## Approach

The state is `(cell, mask of keys held)`. As in 2093 and 1654 the second
coordinate has a direction, more keys is never worse, but it is a partial
order: `{a}` and `{b}` are incomparable, and neither can stand in for the
other. So the bar at a cell cannot be one number. It is the set of masks
already queued there with no one a subset of another, and a push is dropped
when some queued mask contains it. Every move costs 1, so the bar goes on at
the push, as in 1654. The bound on the set is Sperner's, `C(k, k/2)`, 20 masks
for six keys.

## Exhaustive, against a layer oracle

The oracle keeps each layer as a set of states with nothing marked visited and
runs for as many layers as there are states. It agrees with the layered search
on every 1-key grid, on every seventh 2-key grid, and on 3000 random 4x4 grids
with 3 keys.

Every 3x3 grid with `@`, the keys and their locks on distinct cells and every
other cell `.` or `#`.

| keys | grids | answer exists | layered | antichain bar | count bar | one mark |
|---|---|---|---|---|---|---|
| 1 | 32256 | 21688 | 0 | 0 | 0 | 0 |
| 2 | 241920 | 160008 | 0 | 0 | 8978 (5.61%) | 48360 (30.22%) |

Random grids with walls at 25%, wrong counts over the answerable, and the
widest antichain any cell held:

| grid | keys | answerable | count bar | one mark | pops the bar saves | widest | Sperner bound |
|---|---|---|---|---|---|---|---|
| 4x4 | 2 | 4926 | 18.3% | 43.6% | 2.0% | 2 | 2 |
| 5x5 | 3 | 3226 | 39.2% | 81.7% | 7.1% | 3 | 3 |
| 6x6 | 4 | 2396 | 59.1% | 95.2% | 14.3% | 6 | 6 |
| 7x7 | 5 | 1175 | 72.9% | 99.0% | 23.3% | 10 | 10 |
| 8x8 | 6 | 797 | 81.4% | 99.7% | 32.7% | 15 | 20 |

The antichain bar is wrong on none of them.

## What the columns say

- **With one key nothing can go wrong, and not because the searches are
  good.** The only lock is the one key's own, which cannot be open before the
  search is over, so it is a wall and the state is the cell. One mark per cell
  and one number per cell are both exact on all 21688 grids. A test set built
  from one-key grids passes every bug in this file.
- **The count bar**, one number per cell, is the bar of 2093 applied to a
  coordinate it does not fit. The smallest failure is `@.a / bAB / ...`: `b` is
  next to the start, and the arrival at the middle-top cell holding `{a}` is
  queued a layer before the one holding `{b}`, which is then dropped for having
  no more keys. The `{a}` branch has to go through `A` to fetch `b` and the
  search says 5 where the answer is 4.
- **One mark per cell** is wrong on 30% of the answerable 2-key grids and 99.7%
  at 8x8 with six keys. `@.A / a.b / B..` is 3 moves and it says -1: the middle
  cell is reached without a key one pop before it is reached from `a` with one.
- **The order the four moves are queued changes nothing for one mark.** All 24
  orders are wrong on exactly the same 48360 grids, and six sampled orders
  agree on every random table row. The count bar does move with it, 8978 to
  9204. In 1654 an order made the one-mark search right on everything and I
  did not have the argument; here no order helps, and I do not have that
  argument either. A push from one state lands on four different cells, so the
  order can only reach a cell through what it did to earlier pops.
- **The antichain gets as wide as it is allowed to.** 6 of 6 at four keys, 10
  of 10 at five, 15 of the bound's 20 at six on 8x8 grids and 17 on a 30x30.
  I had it under 4.
- **The bar saves more pops the more keys there are**, 0.4% at two on 3x3 up to
  33% at six, and is slower anyway.

## At the statement's size

30x30 with six keys and walls at 20%, six seeds. The layered search pops
21000 to 39000 of 57600 states in 0.05 to 0.08s. The antichain bar pops 6% to
47% fewer and takes 0.05 to 0.16s, up to 2.1x longer, because each push
scans the cell's antichain in Python and the layered search's bit test costs
nothing. The bar is the right idea and the wrong speed-up.

## What I had wrong

Six predictions written before the run. Two right, three half, one wrong.

- **Right:** the layered search and the antichain bar match the oracle
  everywhere.
- **Right:** the count bar wrong on about 5% of the 2-key grids and on none of
  the 1-key. 5.61% and 0.
- **Half:** one mark wrong on about 15% with one key and 30% with two. 30.22%
  with two, and 0 with one, since the lock is a wall there.
- **Half:** no move order makes one mark right, and the best order still wrong
  on over 5% of the 1-key grids. 0 of 24 orders are right at two keys; at one
  key every order is right.
- **Wrong:** the bar saves under 10% of the pops at six keys and the antichain
  never exceeds 4. 32.7% and 15.
- **Half:** the bar is no faster than the layered search at 30x30, within 20%.
  No faster is right, 2.1x slower is not within 20%.

## Bounds

`O(cells 2^k)` states and time for the layered search. The antichain bar holds
at most `C(k, k/2)` masks per cell and scans them on each push, so its worst
case is `O(cells 2^k C(k, k/2))`, and the oracle is `O((cells 2^k)^2)`.

## Files

- `python/solution.py`
