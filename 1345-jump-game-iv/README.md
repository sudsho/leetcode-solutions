# 1345. Jump Game IV

Difficulty: Hard
Topics  : BFS on an implicit dense graph, and the complexity-only guard in a second setting

## Problem

Start at index `0` of `arr`. From index `i` you may jump to `i - 1`, `i + 1`, or
any `j` with `arr[j] == arr[i]`. Return the fewest jumps to reach `n - 1`.

## Approach

Unweighted shortest path, so BFS. The graph is dense and is never built: a value
class of size `m` contributes `m(m - 1)` edges, and `[7] * n` is one class, so
the explicit adjacency list is `O(n^2)` on an input the problem allows at
`n = 5 * 10^4`.

Instead the classes are held as buckets, `by_value[v] -> [indices]`, and a whole
bucket is expanded in one step. Level-order BFS, `visited` set at enqueue time,
answer is the level at which `n - 1` comes off the queue.

## The line

```python
same = by_value[arr[i]]
for j in same:
    ...
same.clear()
```

**Harmless.** When `i` is dequeued, every index in its value class is enqueued
right there or was visited already, so the class is exhausted by that single
expansion. Every later look at the bucket finds nothing to do, and deleting it
cannot change the visited set. One line.

**Necessary.** `[7] * n` is a single class of size `n`. Without the clear, each
of the `n` dequeues rescans all `n` members, all of them visited. Both versions
return `1`.

```
  n=   10  cleared=    28 (3n-2)   uncleared=     108 (n^2+n-2)   ratio=     3.9
  n=   50  cleared=   148 (3n-2)   uncleared=    2548 (n^2+n-2)   ratio=    17.2
  n=  200  cleared=   598 (3n-2)   uncleared=   40198 (n^2+n-2)   ratio=    67.2
  n=  800  cleared=  2398 (3n-2)   uncleared=  640798 (n^2+n-2)   ratio=   267.2
  n= 2000  cleared=  5998 (3n-2)   uncleared= 4001998 (n^2+n-2)   ratio=   667.2
```

Both counts are exact rather than asymptotic and the run asserts them as
identities. Agreement about the answer is checked over every array on two values
up to length 11 and three values up to length 8, against the `O(n^2)` oracle.

## Why this problem

The 7th ended holding a thing it would not promote. 685 and 499 were both about
conventions that decide the printed answer - a tie-break sitting beside the
algorithm, or carried through a Dijkstra key and owing a monotonicity proof.
Then 1163 turned up a line, `i = max(i + k + 1, j)`, that no part of the
correctness argument mentions and that is nevertheless the whole bound: exactly
`n` against exactly `n^2 / 4 - 1` on `("ba" * m) + "aabb"`, both versions
agreeing about the answer at every size. That is a third position for a choice
to sit in, and it had one instance, found in a two-pointer scan on strings,
which is the setting the axis it came from was born in.

So this is the same position looked for as far from a lex duel as the log goes.
It is there. `same.clear()` is a line the proof never sees and the bound cannot
do without.

## Where the two come apart

Two things, and neither was in the prediction.

**The proof obligations are the mirror image.** On 1163 harmlessness was the
subtle direction - dropping the max is safe only because everything below `j`
died in an earlier round - and it took an exhaustive search over two alphabets
before I believed it, while necessity was a one-family measurement. Here it is
the other way round: harmlessness is the one-line argument above, and necessity
is the whole story. What the two nights share is the position, not the shape of
getting into it.

**They are not equally easy to miss, and this is the correction.** I had written
down before the run that a complexity-only guard is invisible to random testing,
because the 7th's was - re-elimination needs a periodic string, so random inputs
never charge for it and only a constructed family does. That is a property of
that guard and I had it filed as a property of the position.

```
  |distinct values|= 2000   uncleared/cleared =    1.35x
  |distinct values|=  500   uncleared/cleared =    2.26x
  |distinct values|=  100   uncleared/cleared =    6.29x
  |distinct values|=   20   uncleared/cleared =   19.52x
  |distinct values|=    4   uncleared/cleared =  150.95x
  |distinct values|=    1   uncleared/cleared =  667.22x
```

Random arrays of length 2000. There is no threshold and no family to construct.
The penalty is the mean class size, it rises the moment values start repeating,
and a hundred distinct values is already 6x. This guard needs a collision; the
7th's needed a period. So "you will not catch it by testing" is not what the
position implies - it depends on how rare the input that charges for it is, and
that varies by instance and not by category.

## Bounds

`0` when `n == 1`, and the start is the target. Otherwise at least `1`, and at
most `n - 1` by walking `i + 1` the whole way, which is attained when every
value is distinct - `[0, 1, 2, ..., n-1]`. The answer is never `-1`: the `i + 1`
edges alone connect the line, so the graph is connected and the BFS always
arrives. Every index is enqueued once and every bucket is scanned once, so the
work is `n` bucket members plus `2n` neighbour steps, and the `3n - 2` above is
that count exactly.

## Files

- `python/solution.py`
