class Solution:
    def hammingDistance(self, x, y):
        z = x ^ y
        count = 0
        while z:
            count += z & 1
            z >>= 1
        return count
