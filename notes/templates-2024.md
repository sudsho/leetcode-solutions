# templates-2024

rolling notes
- floyd cycle is the cleanest way for find duplicate variants.
- bitmask dp template: state = (mask, optional knapsack capacity).
- knuth optimization for matrix-chain-like O(n^3) -> O(n^2).
- segment tree with coordinate compression for range count problems.
- count by contribution rather than directly enumerate.
- lazy propagation for additive range updates.
- reroot dp template.
- prefix mod count for subarray-sum-divisible-by-k. the map value is the whole
  decision: first index to maximize a window (525, 523), frequency to count
  (560, 974, 1074), latest index to minimize a window (1590).
- difference array is the prefix sum run backwards - range add becomes two
  writes (+v at l, -v at r+1), one accumulate at the end rebuilds the values
  (1109). pick by which op is hot: hot queries -> prefix sums, hot range
  updates -> diff array, both hot -> fenwick (307, 308).
  precondition is that the update composes additively and order-independently,
  not just that it's a range update - 2381 works because letter shifts add.
  the two writes are fixed, three things vary:
  - where the close goes: inclusive range -> r+1 (1109, 2848, 2381), half-open
    -> r (1094, drop-offs happen AT end). read it per problem, don't reuse.
  - what the accumulator means: the answer (1109), a covered flag (2848), a
    live constraint checked inside the loop (1094), an offset mod 26 (2381).
  - whether the coordinate space is indexable. small fixed bound -> array;
    otherwise merge intervals (2848) or a min-heap of open ranges (1094).
- tarjan low-link refresher.
- another way to think about kth smallest with two heaps.
- offline + sort queries trick for max-XOR-with-threshold.
- KMP failure function for shortest period type problems.
- monotonic deque for sliding window minimum.
- two pointers for "at most k distinct" then subtract.
- another reminder: when in doubt, prefix sums.
