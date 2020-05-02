# track min so far in one pass
class Solution:
    def maxProfit(self, prices):
        lo = float("inf")
        best = 0
        for p in prices:
            if p < lo:
                lo = p
            elif p - lo > best:
                best = p - lo
        return best
