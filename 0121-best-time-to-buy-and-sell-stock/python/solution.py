# revisited - cleaned up
class Solution:
    def maxProfit(self, prices):
        if not prices:
            return 0
        min_so_far = prices[0]
        best = 0
        for p in prices[1:]:
            if p < min_so_far:
                min_so_far = p
            else:
                best = max(best, p - min_so_far)
        return best

# optim: pass small inputs straight through above
# notes: tightened naming
