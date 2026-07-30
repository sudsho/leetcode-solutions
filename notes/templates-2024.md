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
- tarjan low-link refresher.
- another way to think about kth smallest with two heaps.
- offline + sort queries trick for max-XOR-with-threshold.
- KMP failure function for shortest period type problems.
- monotonic deque for sliding window minimum.
- two pointers for "at most k distinct" then subtract.
- another reminder: when in doubt, prefix sums.
