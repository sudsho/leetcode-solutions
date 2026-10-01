# graph bfs vs dfs

- digit dp: pre-compute place value contributions; saves a layer.
- recurse on `n - n//2 - 1` for the right subtree count.
- monotonic stack: keep indexes, not values, when you might need positions.
- bidirectional bfs: swap fronts when one outgrows the other.
- entry 177: small reminder.
- manacher for longest palindromic substring in linear time.
- union find rollback for offline tasks.
- bfs over an implicit dense graph: hold the equivalence classes as buckets and
  clear a bucket once you expand it. one expansion settles the whole class, so
  the clear cannot change an answer, and without it the scan is quadratic.
  that is for reachability only. counting shortest sequences, copying the pop's
  own count through the clear (or a `farthest` pointer, or a skip pointer) is the
  wrong answer (1345, 1871, 2612), and at zero cost deleting the clear is wrong
  too (3552). keep the clear and fill each count once its level is finished, as
  one sum over the part of that level that reaches it - a window of the level's
  run in 1871, the bucket's sum in 1345 and 3552, and a range of the sorted level
  in 2612, since a reversal undoes itself and a level is one parity. a
  frontier-at-a-time bfs knows when a level is finished for free. only the 0-1
  deque in 3552 needed an argument, that a letter's portals share one level.
- a bar on a second coordinate (1928, 2093, 1654, 864): when the state is
  (node, extra) and more extra is never worse, keep one bar per node, the most
  extra any arrival had, and drop an arrival that brings no more. set it at the
  pop when edge costs vary, since a push is not yet in cost order (2093's push
  bar was wrong on 73%), and at the push when every move costs 1 (1654, 864).
  when the extra is only partly ordered, {a} against {b} in 864, no single
  number stands in for it and the bar is an antichain of what was held, as
  wide as sperner allows. in python it was slower than the plain layered
  search even while it saved a third of the pops, since a bit test is free.
- dijkstra stale skip (`if d > dist[u]: continue`): plain dijkstra survives
  losing it, which says nothing about the program in front of you. go through
  each update the pop reaches and ask whether a repeat is absorbed under what it
  reads - strict `<` and max are, an overwrite only from dist[u], `+=` and a
  per-pop counter never (1976, 882).
