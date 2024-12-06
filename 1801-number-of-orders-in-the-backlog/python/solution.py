from heapq import heappush, heappop
from typing import List

class Solution:
    MOD = 10 ** 9 + 7
    def getNumberOfBacklogOrders(self, orders: List[List[int]]) -> int:
        buys: list[list[int]] = []   # max-heap via negation: [-price, amount]
        sells: list[list[int]] = []  # min-heap: [price, amount]
        for price, amount, otype in orders:
            if otype == 0:
                while amount and sells and sells[0][0] <= price:
                    take = min(amount, sells[0][1])
                    sells[0][1] -= take
                    amount -= take
                    if sells[0][1] == 0:
                        heappop(sells)
                if amount:
                    heappush(buys, [-price, amount])
            else:
                while amount and buys and -buys[0][0] >= price:
                    take = min(amount, buys[0][1])
                    buys[0][1] -= take
                    amount -= take
                    if buys[0][1] == 0:
                        heappop(buys)
                if amount:
                    heappush(sells, [price, amount])
        total = sum(o[1] for o in buys) + sum(o[1] for o in sells)
        return total % self.MOD
# small fix
# tightened naming
# refactored helper
