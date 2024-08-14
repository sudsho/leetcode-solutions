from heapq import heappush, heappop
from typing import List

class Solution:
    MOD = 10 ** 9 + 7

    def getNumberOfBacklogOrders(self, orders: List[List[int]]) -> int:
        # Same heap match, but written more compactly with helper
        buys: list[list[int]] = []
        sells: list[list[int]] = []

        def take(book: list[list[int]], amt: int, cmp_price: int, is_buy: bool) -> int:
            while amt and book and (
                (is_buy and book[0][0] <= cmp_price) or
                (not is_buy and -book[0][0] >= cmp_price)
            ):
                top = book[0]
                used = min(amt, top[1])
                top[1] -= used
                amt -= used
                if top[1] == 0:
                    heappop(book)
            return amt
        for price, amount, otype in orders:
            if otype == 0:
                amount = take(sells, amount, price, True)
                if amount:
                    heappush(buys, [-price, amount])
            else:
                amount = take(buys, amount, price, False)
                if amount:
                    heappush(sells, [price, amount])
        return (sum(o[1] for o in buys) + sum(o[1] for o in sells)) % self.MOD
