# 797. All Paths From Source to Target

Difficulty: Medium
Topics  : DFS enumeration of the paths in a DAG, path counting by predecessor sums, and the most paths a DAG on n nodes and m edges can hold

## Problem

A directed acyclic graph on nodes `0` to `n - 1`, given as adjacency lists.
Return every path from `0` to `n - 1`, in any order. `n` is at most 15.

## Approach

A dfs with one path on the stack, appended at the sink. The cap on `n` is
there because the output can be every subset of the middle nodes, `2^(n-2)`
paths on the transitive tournament, 8192 at 15.

The problem is here as an instrument. 1786 counts paths on which the
distance to `n` strictly falls, which are the paths of the DAG the distance
potential defines, and it left open how many such paths a graph of `n` nodes
can hold: the ladder gives `2^((n-3)/2)` and "layers of three would grow like
`3^(n/3)`". The other direction holds too. Any DAG whose nodes all reach the
sink is a 1786 instance with weight = fall in a potential strictly decreasing
along its edges, since every walk's weight telescopes to at least the fall,
with equality exactly when it never climbs. So 1786's maximum is the most
`0 -> n-1` paths a DAG on `n` nodes and `m` edges can hold, with `m` at most
`4 * 10^4` for `n` at most `2 * 10^4`, two edges a node.

`solution.py` checks the realisation against 1786's own program, enumerates
every DAG to `n = 9` by predecessor sets, with the last three nodes closed by
their best predecessor set per size since the sink's count is a sum of
non-negative terms, and puts chains of complete blocks, a climber and the
strips the table turned up against it.

## Realisation

Weight `= n - 1 - i` minus `n - 1 - j` on edge `i -> j`, nodes shifted to
`1..n`. 1786's program agrees with the DAG's path count on 3 of 3 DAGs at
`n = 3`, 21 of 21 at 4 and 315 of 315 at 5, every edge set whose nodes all
reach the sink, and on 2000 random DAGs at `n = 9` under random potentials.

## The most paths on at most n nodes and m edges

Exhaustive, with the best chain of complete blocks in brackets, where a block
of `k` nodes shares one node with the next and multiplies the count by
`2^(k-2)` for `k(k-1)/2` edges. A star marks the chain beaten.

| n | m: paths (chain) |
|---|---|
| 4 | 3:2 (2) 4:2 (2) 5:3 (2)* 6:4 (4) |
| 5 | 4:2 (2) 5:3 (2)* 6:4 (4) 7:5 (4)* 8:6 (4)* 9:7 (4)* 10:8 (8) |
| 6 | 5:3 (2) 6:4 (4) 7:5 (4)* 8:6 (4)* 9:8 (8) 10:10 (8)* 11:12 (8)* 12:13 (8)* 13:14 (8)* 14:15 (8)* 15:16 (16) |
| 7 | 6:4 (4) 7:5 (4)* 8:6 (4)* 9:8 (8) 10:10 (8)* 11:13 (8)* 12:16 (16) 13:20 (16)* 14:22 (16)* 15:24 (16)* 16:26 (16)* 17:28 (16)* 18:29 (16)* 19:30 (16)* 20:31 (16)* 21:32 (32) |
| 8 | 7:5 (4) 8:6 (4)* 9:8 (8) 10:10 (8)* 11:13 (8)* 12:16 (16) 13:21 (16)* 14:26 (16)* 15:32 (16)* 16:36 (32)* 17:40 (32)* 18:44 (32)* 19:48 (32)* 20:52 (32)* 21:54 (32)* 22:56 (32)* 23:58 (32)* 24:60 (32)* 25:61 (32)* 26:62 (32)* 27:63 (32)* 28:64 (64) |
| 9 | 8:6 (4) 9:8 (8) 10:10 (8)* 11:13 (8)* 12:16 (16) 13:21 (16)* 14:26 (16)* 15:34 (32)* 16:42 (32)* 17:52 (32)* 18:60 (32)* 19:68 (32)* 20:74 (64)* 21:81 (64)* 22:88 (64)* 23:96 (64)* 24:100 (64)* 25:104 (64)* 26:108 (64)* 27:112 (64)* 28:116 (64)* 29:118 (64)* 30:120 (64)* 31:122 (64)* 32:124 (64)* 33:125 (64)* 34:126 (64)* 35:127 (64)* 36:128 (128) |

The predecessor-set enumeration matches a plain enumeration of every edge set
at `n = 4, 5, 6`.

## What the table says

- **The chain is right where it fits and nowhere else.** `(7, 9) = 8` is three
  K3s and `(7, 12) = 16` two K4s, and nothing beats either. Between, the chain
  is beaten on 67 of the 77 cells with `n - 1 < m < C(n, 2)`, by 2.125x at
  worst, `(9, 19) = 68` against 32. And `(9, 20) = 74` beats two K5s' 64, so
  the chain is not even safe where it fits once the blocks are five wide.
- **The maximisers are strips.** Every witness at `n = 5` and 6 has node `j`
  joined to the nodes just before it: `(6, 10) = 10` is K4 on `0..3`, then
  `4 <- {2, 3}`, `5 <- {3, 4}`, counts 1 1 2 4 6 10. Strips, each node on the
  `k_j` nodes before it with any in-degree sequence, on at most `n` nodes,
  match the exhaustive maximum on every cell at `n = 4` to 9, 89 of 89, and
  never exceed it.
- **At two edges a node the strip is the Fibonacci numbers.** Each node on
  the two before it, `2n - 3` edges, gives `F_n`: `(5, 7) = 5`, `(6, 9) = 8`,
  `(7, 11) = 13`, `(8, 13) = 21`, `(9, 15) = 34`, every one the table's
  maximum. That is `1.618^n` against the K4 chain's `4^(n/3) = 1.587^n` at the
  same edge budget, 1786's `3^(n/3) = 1.442^n` guess, and the ladder's
  `2^(n/2) = 1.414^n`. One more edge at the start, a K4 on `0..3`, gives
  `(n, 2n - 2)`: 6, 10, 16, 26, 42.
- **Every edge buys a path from `n = 5` up.** One flat step in the whole table,
  `(4, 3)` to `(4, 4)`, both 2. I expected one at every `n`.
- **The climber is no instrument here.** Twenty restarts of 3000 edge swaps at
  `n = 13` reach 204 at `m = 24`, below the chain's 256 and the K4-start
  strip's 288, and 700 at `m = 30`, above the chain's 512 and equal to the
  best strip with windows up to three.

## At 1786's size

`n <= 20000`, `m <= 40000`, counts through 1786's own program, 0.04 s each.

| graph | n | m | digits |
|---|---|---|---|
| ladder, width 2 (1786's, at its full budget) | 20000 | 39996 | 3010 |
| layers of three | 13334 | 39993 | 2121 |
| K3 chain | 19999 | 29997 | 3010 |
| K5 chain | 16001 | 40000 | 3613 |
| K4 chain | 19999 | 39996 | 4014 |
| 6665 K4 and one K5, the best chain | 20000 | 40000 | 4014 |
| Fibonacci strip | 20000 | 39997 | 4180 |
| K4 start, four predecessors at the sink | 20000 | 40000 | 4180 |

The best chain is `2^13333` and 1786's program returns it mod `10^9 + 7`,
905610430. The strip with the three spare edges is 718693068 and matches its
exact count. 1786's ladder at `n = 15999` had 2408 digits. So the most
restricted paths at the statement's size is at least 4180 digits, and the
strip is the maximum at `n <= 9`; whether it is past that is open.

## What I had wrong

Six predictions written before the run. Three right, one half, two wrong.

- **Right:** every DAG whose nodes all reach the sink realises as a 1786
  instance with the same count. 339 of 339 and 2000 of 2000.
- **Right:** `(7, 12)` is 16 and `(7, 9)` is 8, the chains of two K4s and
  three K3s, and nothing at those cells beats them.
- **Half:** the chain is beaten on over half of the cells between, never by
  more than 2x. 67 of 77, and 2.125x.
- **Wrong:** a flat step at every `n` from 4 to 9. One in all, at `n = 4`.
- **Wrong:** the climber reaches 256 at `(13, 24)` and 512 at `(13, 30)` and
  nothing above. 204 and 700.
- **Right:** the best chain at 1786's size is 6665 K4s and one K5, `2^13333`,
  and 1786's program returns it in under a second. 0.04 s. It is not the
  maximum there, which I did not predict either way.

## Bounds

Up to `2^(n-2)` paths of up to `n` nodes, so `O(n 2^n)` output and time, and
`O(n)` stack. The predecessor-set enumeration is `2^(C(n-3, 2))` leaves with
`O(n^3)` work each, 4 s at `n = 9`.

## Files

- `python/solution.py`: the dfs, the path count by predecessor sums, the
  realisation check against 1786's program, the exhaustive maximum to
  `n = 9`, the chain and strip families, the climber and the runs above,
  about ten seconds.
