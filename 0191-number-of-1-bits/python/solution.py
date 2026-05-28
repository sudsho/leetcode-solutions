class Solution:
    def hammingWeight(self, n):
        # brian kernighan trick: n & (n-1) clears the lowest set bit
        count = 0
        while n:
            n &= n - 1
            count += 1
        return count
