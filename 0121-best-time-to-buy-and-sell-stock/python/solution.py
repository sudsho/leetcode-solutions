# revisited - cleaned up
class Solution:
    def maxProfit(self, prices):
        """Best single buy/sell profit in one pass.

        Track the lowest price seen so far; at each later day the best profit
        ending there is price - min_so_far. Keep the running maximum. O(n) time,
        O(1) space.
        """
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
# typing fix
