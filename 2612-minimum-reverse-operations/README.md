# 2612. Minimum Reverse Operations

Difficulty: Hard
Topics  : BFS with skip pointers per parity, the skip under counting, and a pull from the finished level

## Problem

An array of `n` zeros with a single 1 at `p`. One operation reverses a subarray of
length `k`, and it is allowed only if the 1 does not land on an index in
`banned`. Return, for every index, the fewest operations that bring the 1 there,
or `-1`.

## Approach

Reversing `[left, left + k - 1]` with the 1 at `i` inside sends it to
`2 * left + k - 1 - i`, and `left` runs from `max(0, i - k + 1)` to
`min(i, n - k)`, so one operation reaches a stride-2 run, `landing(i, n, k)`.
BFS over indices. The unvisited indices of each parity sit behind skip pointers
(union-find with path halving), a run is walked with `find`, and every index it
hands out is removed.

## The line

```python
if clear:
    nxt[j] = j + 2
```

**Harmless.** Every `n` up to 9 with every `p`, every `k` and every banned set not
holding `p`, 33789 instances. `min_ops(clear=True)` and `min_ops(clear=False)`
both equal an oracle that simulates each reversal on an actual array.

**Necessary.** Indices examined, nothing banned, `p = 0`:

```
  n= 1000 k=    2  reachable  1000  kept     1999  dropped      2997  ratio     1.50
  n= 1000 k=    3  reachable   500  kept      999  dropped      1996  ratio     2.00
  n= 1000 k=   51  reachable   500  kept      999  dropped     24724  ratio    24.75
  n= 1000 k=  500  reachable  1000  kept     1999  dropped    251499  ratio   125.81
  n= 1000 k=  999  reachable   500  kept      999  dropped      1498  ratio     1.50
  n= 4000 k= 2000  reachable  4000  kept     7999  dropped   4005999  ratio   500.81
  n= 4000 k= 3999  reachable  2000  kept     3999  dropped      5998  ratio     1.50
```

With the line it is `2r - 1` for `r` reachable indices, one per index handed out
and one failing lookup per pop. Without it it is the sum of the reachable runs.
Both are asserted. The ratio peaks near `k = n / 2` at about `n / 8`, and at
`k = n - 1` a run holds at most two indices, so the line saves almost nothing
there.

## Under counting

Count the shortest sequences of reversals. Two subarrays from the same index
never land in the same place, asserted in the oracle, so a sequence is a path in
the index graph.

- **keep the skip, `+=`**: 1 at every reachable index, asserted on all 33789. Each
  index is handed out once, to whoever finds it first, so the count is copied
  down a chain of first discoverers, which is 1871's failure exactly. Wrong on
  the 2112 instances that have an index with two shortest sequences.
- **delete the skip, `+=` only from the level below**: right on all 33789 and on
  2400 random instances with `n = 60`. It pays for every run in full.
- **keep the skip, pull from the finished level**: right on all of the same.

## The pull

`count_by_levels` discovers each level with the skip kept and only then fills in
its counts. Two facts make that one range sum per index.

The relation is symmetric. A second reversal of the same subarray puts the 1 back, so
the indices that reach `j` are exactly `landing(j, n, k)`.

A level is one parity. A reversal of length `k` moves the 1 from `i` to an index
congruent to `k - 1 - i` mod 2, so from `p` every index at one distance has the
same parity, asserted on every level of every instance. So every index of the
finished level that falls inside `j`'s run numerically is a predecessor, with no
filter.

Sort the level, prefix-sum its counts, two bisections per new index:

```
  n=5000 k=    8  reachable  4750  levels  364  pull  0.010s  delete+add  0.012s  largest count has 30 digits
  n=5000 k=  101  reachable  2374  levels   26  pull  0.006s  delete+add  0.044s  largest count has 20 digits
  n=5000 k= 1000  reachable  4750  levels    4  pull  0.011s  delete+add  0.732s  largest count has 9 digits
  n=5000 k= 2500  reachable  4750  levels    2  pull  0.011s  delete+add  1.155s  largest count has 4 digits
```

With `p = n / 2` and 5% banned. Nothing in 2612 is a class. The level is
finished whenever the BFS finishes a frontier, and what the fix needed was that
the part of the finished level reaching `j` is one sum. Here that sum is a run,
because the relation is symmetric.

## What I had wrong

**Keeping the skip, wrong on more than half of the reachable non-start indices
once `k >= 3` and `n >= 8`.**

```
  n=8  k=2:0.000  k=3:0.000  k=4:0.152  k=5:0.000  k=6:0.100  k=7:0.000  k=8:0.000
  n=9  k=2:0.000  k=3:0.000  k=4:0.180  k=5:0.019  k=6:0.180  k=7:0.039  k=8:0.000  k=9:0.000

  n=60, 300 random instances each
  k= 3 banned~0.0  reachable non-start  8700  >1 sequence     0 (0.000)
  k= 5 banned~0.1  reachable non-start  7061  >1 sequence  3430 (0.486)
  k= 8 banned~0.1  reachable non-start 15710  >1 sequence 12169 (0.775)
  k= 9 banned~0.1  reachable non-start  7780  >1 sequence  4569 (0.587)
  k=20 banned~0.2  reachable non-start 13944  >1 sequence 10119 (0.726)
  k=21 banned~0.2  reachable non-start  6874  >1 sequence  3129 (0.455)
  k=45 banned~0.4  reachable non-start  4918  >1 sequence  2370 (0.482)
```

On the exhaustive set it never passes 18%, and it is 3336 of 45874 overall. At
`k = 3` it is zero at every size, because a reversal of length 3 moves the 1 by
two, each parity is a path, and a path has one shortest route. At `n = 60` it
holds at `k = 8, 9, 20` and fails at `3, 5, 21, 45`. The two even `k` are the two
highest, and I do not have the reason.

**About `nk / 2` indices examined without the skip.** Right from `k = 51` to
`k = n / 2`, 24724 against 25500 and 4005999 against 4000000. Wrong at the ends:
1498 against 499500 at `k = n - 1`.

## Bounds

`0` at `p`, `-1` on banned and unreachable indices. Otherwise at most `r - 1` for
`r` reachable indices, since every level before an index is nonempty, and `n - 1`
is attained at `k = 2` from an end. With the skip, `2r - 1` indices are examined
and path halving without ranks keeps a lookup `O(log n)` amortised. Without it
the examined count is at most `r * min(k, n - k + 1)`, and about half that with
nothing banned, `n^2 / 4` at `k = n / 2`. The pull adds a sort per level and two
bisections per index, `O(n log n)`. The counts have no modulus because nothing
asks for one.

## Files

- `python/solution.py`
