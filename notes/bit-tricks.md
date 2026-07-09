# bit tricks

- reverse bits: shift low bit onto result from the left, 32 times.
- reverse a byte at a time with a 256-entry table when called in a hot loop.
- n & (n-1) clears the lowest set bit; loop it to popcount.
- n & (-n) isolates the lowest set bit (fenwick tree index step).
- x ^ x = 0, so xor of all pairs leaves the single number.
- swap without temp: a ^= b; b ^= a; a ^= b.
