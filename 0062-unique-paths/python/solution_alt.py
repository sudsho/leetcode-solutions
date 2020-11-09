# combinatorial form: C(m+n-2, m-1)
from math import comb
class Solution:
    def uniquePaths(self, m, n):
        return comb(m + n - 2, m - 1)
