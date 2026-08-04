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
