# sweep line tricks
- nit 107.
- fenwick tree (BIT) is great for inversion-style counts.
- monotonic deque for sliding window minimum.

## difference array - the actual precondition

the technique is always two writes and an accumulate. what varies is three things:

- where the closing write goes. inclusive range -> `end + 1`, half-open -> `end`. decided by the problem, never by the technique. shows up as an index offset (1109), a bisect_left/bisect_right split (2251), a strict `<` in a loop (2406), a `hi - 1` on a compressed gap (699). re-derive it every time, i have never once produced it from memory.
- what the accumulated value means. total (1109), predicate (2848), live constraint checked against a bound each step (1094), modular offset (2381), running maximum (2406). the last one is the odd entry: it needs the total kept rather than consumed at a point.
- whether the coordinate space is indexable. small fixed bound -> plain array. 10^9 -> the accumulate is a prefix count over sorted endpoints, so binary search it instead (2251).

## when it does not apply

two conditions, both required, and i only had the first one written down:

1. the updates compose commutatively. order-independent, so the pile at each position collapses to one number.
2. the updates do not read the state they modify. blind writes only.

699 breaks both - a square writes (max height underneath) + side, which is a query of the current state, and it assigns rather than increments so there is no inverse write. order matters, nothing collapses, and it needs a segment tree with lazy propagation holding real values.

so the test is not "are there range updates". it is: can two updates swap places without changing the answer, and does either need to look before writing.

## higher dimensions

2d is not a new technique, it is the 1d one run once per axis. accumulate along the rows, then down the columns; a cell ends up holding the sum of every delta weakly north-west of it. because the accumulate is separable the writes are too - the 1d pair taken per axis and multiplied out, which is the four corners:

```
+1 (r1, c1)      -1 (r1, c2+1)
-1 (r2+1, c1)    +1 (r2+1, c2+1)
```

the fourth write is the droppable one and it does not corrupt the rectangle, it corrupts everything south-east of it. small hand-checked grids have nothing there (2536).

the single-pass accumulate `g[r][c] = d[r][c] + g[r-1][c] + g[r][c-1] - g[r-1][c-1]` subtracts for the same double-count the fourth corner write fixes. same identity twice, once placing deltas and once consuming them. and it is the same four-corner shape as the 2d fenwick in 308 and the band collapse in 1074 - those are not three prefix-sum facts, they are one statement about rectangles read in different directions.

k dimensions is 2^k writes by the same argument. the row-wise alt in 2536 is the reminder that the extra axis buys nothing new, it only defers a spreading step into a sweep that was already being paid for.

## the inverse direction

the accumulate loses nothing because the difference array is a **bijection** - array with an implied 0 boundary <-> delta sequence. that is the actual license for two writes standing in for a whole range, and it makes the backwards question well-posed: given the array, what is the cheapest multiset of range updates producing it.

an op on [l, r] writes +1 to d[l] and -1 to d[r+1] and nothing else, so

```
d[i] = (ops starting at i) - (ops ending at i-1)
```

second term is never negative, every op starts exactly once, so the count is at least the sum of the positive deltas - and that is achievable, closes always pair against something already open (1526).

worth separating from everything above: this is the only one so far that gives a **lower bound** rather than a computation. nothing is swept and no state exists, the count is forced by what a single update is permitted to write. and the negative deltas being free is the same nesting fact that makes a LIFO stack the right way to reconstruct the actual ops.
