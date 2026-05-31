class Solution:
    def grayCode(self, n):
        # standard reflected binary gray code: i ^ (i >> 1)
        # adjacent codes differ by exactly one bit, and the sequence
        # is cyclic (last code differs from 0 by one bit too).
        return [i ^ (i >> 1) for i in range(1 << n)]
