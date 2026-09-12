# 1871. Jump Game VII

Difficulty: Medium
Topics  : BFS over sliding windows, and 1345's bucket clear under counting

## Problem

A binary string `s` with `s[0] == '0'`. From index `i` you may jump to any `j`
with `i + minJump <= j <= min(i + maxJump, n - 1)` and `s[j] == '0'`. Return
whether index `n - 1` is reachable.

## Approach

BFS over indices, each dequeued index scanning its window. Done plainly that is
`O(n * maxJump)`. The standard fix keeps `farthest`, the right end of the last
window scanned, and starts every new window past it.

## The line

```python
for j in range(max(i + minJump, farthest + 1), min(i + maxJump, n - 1) + 1):
    ...
farthest = i + maxJump
```

**Harmless.** Indices come off the queue in increasing order, so
`[i + minJump, farthest]` lies inside windows already scanned from lower
indices, and everything in it was taken or rejected there. Checked over every
string of length 2 to 12 starting with `'0'` and every
`1 <= minJump <= maxJump < n`, 229374 instances: reach and distances identical
with and without it, against an oracle that builds the edge list.

**Necessary.** `'0' * n` with `minJump = 1`, `maxJump = n - 1`, answer `True`
either way:

```
  n=   10  skip=     9 (n-1)   no skip=      45 (n(n-1)/2)   ratio=    5.0
  n=  200  skip=   199 (n-1)   no skip=   19900 (n(n-1)/2)   ratio=  100.0
  n= 2000  skip=  1999 (n-1)   no skip= 1999000 (n(n-1)/2)   ratio= 1000.0
```

Both asserted as identities. On random strings it charges the way 1345's clear
did, with no family to build:

```
  lo=1 hi=   2   ratio=    1.39x
  lo=1 hi=   5   ratio=    3.63x
  lo=1 hi=  20   ratio=   14.02x
  lo=1 hi= 100   ratio=   67.91x
  lo=1 hi= 500   ratio=  304.99x
```

`n = 2000` at 70% zeros, so the ratio should be about `0.7 * maxJump`. It is, to
two digits up to 100, and at 500 the windows run off the end and it is 305
against 350.

## Under counting

882's table predicted this before any of it was run. The rescan skipped here and
in 1345 only ever reaches `if not visited[j]`, which absorbs a repeat. Count the
shortest jump sequences and the same rescan reaches
`elif dist[j] == dist[i] + 1: ways[j] += ways[i]`, which does not. So the
prediction was that the direction reverses: keeping the line is the bug and
deleting it is the fix.

It reverses, on both lines.

| program                  | 1871, every instance above (68864 reachable) | 1345, 2 values to length 10 | 1345, 3 values to length 7 |
|--------------------------|----------------------------------------------|-----------------------------|----------------------------|
| keep the line, count     | **30641 wrong**                              | **104 of 1024 wrong**       | **48 of 2187 wrong**       |
| delete the line, count   | 0                                            | 0                           | 0                          |

The 1871 program is not an occasional undercount. Under the skip every index is
scanned exactly once, by its lowest reaching predecessor, so
`ways[j] = ways[i]` copies the 1 at index 0 down the whole chain and the program
returns 1 on every reachable instance, asserted per index. It is wrong exactly
when there is more than one shortest sequence, and absent rather than rare when
`minJump == maxJump`, where every index has one predecessor.

## Deleting it is right, and the cost is not forced

The skipped scan pushes in increasing index order and a bfs queue is in level
order, so the distance is non-decreasing in the index over reachable indices,
asserted on all 229374 instances. Each level is then one contiguous run, and the
predecessors of `j` one level down are the window `[j - maxJump, j - minJump]`
cut to that run, which is one prefix-sum difference. `count_by_level_runs` keeps
the skip, is `O(n)`, and matches the oracle everywhere.

So the line is wrong under counting and the counting program still does not have
to pay `n * maxJump` for dropping it. That comes from an order this problem has
and 1345 does not, and I have not looked for 1345's replacement.

## What I had wrong

Two predictions written before the run, and the explanation I reached for when
one of them failed.

**1345's clear under counting, wrong on under 10% of the small exhaustive sets.**
10.2% and 2.2%, which straddles it. Random arrays of length 60 go further:

```
  |distinct values|= 60   cleared wrong  16/300   of the 295 not solved in one jump
  |distinct values|= 20   cleared wrong  64/300   of the 278 not solved in one jump
  |distinct values|=  8   cleared wrong 124/300   of the 263 not solved in one jump
  |distinct values|=  3   cleared wrong  88/300   of the 204 not solved in one jump
```

The fall at 3 values is mostly arrays whose two ends share a value, which is one
jump and exactly one sequence. Among the rest it is 5%, 23%, 47%, 43%.

**The 1871 skip wrong on more than 80% of reachable random instances once the
window is 3 wide.** It holds at `(2, 4)` and `(3, 7)` and fails at the widest:

```
  lo=2 hi= 3   reachable 117/400   skip + counting wrong 107   mean slack  4.15
  lo=2 hi= 4   reachable 231/400   skip + counting wrong 212   mean slack  4.93
  lo=3 hi= 7   reachable 279/400   skip + counting wrong 271   mean slack  4.43
  lo=1 hi=10   reachable 269/400   skip + counting wrong 195   mean slack  4.35
```

72% at `(1, 10)`. I had a reason ready, that ten-wide jumps leave the shortest
sequences little room to differ, and put a slack column in before believing it.
The slack is 4.35 against 4.15 to 4.93 for the rest, so that is not it, and I do
not have the reason.

## Bounds

`False` whenever `s[-1] == '1'`. With the skip every window starts past the last
one's right end, so each of indices `1..n-1` is scanned at most once and the
scan is at most `n - 1`, attained on all zeros with the widest window. Without
it the scan is at most the reachable count times `maxJump - minJump + 1`. When
`n - 1` is reachable there is at least one shortest sequence, and exactly one
when `minJump == maxJump`.

## Files

- `python/solution.py`
