from typing import List

class Solution:
    def maximumCoins(self, coins: List[List[int]], k: int) -> int:
        coins.sort()
        ans = 0
        # try each interval as a candidate left edge
        n = len(coins)
        # candidate left positions: the left endpoint of each segment
        # window covers [L, L + k - 1]
        # use two-pointer over sorted segments
        def calc(starts: List[int]) -> int:
            res = 0
            i = j = 0
            cur = 0
            for s in starts:
                e = s + k - 1
                while j < n and coins[j][0] <= e:
                    a, b, c = coins[j]
                    cur += (min(b, e) - a + 1) * c
                    j += 1
                # remove segments fully before s
                while i < j and coins[i][1] < s:
                    a, b, c = coins[i]
                    cur -= (b - a + 1) * c
                    i += 1
                # adjust partials at the front
                # recompute partial for i if it overlaps but a < s
                if i < j and coins[i][0] < s:
                    a, b, c = coins[i]
                    full = (b - a + 1) * c
                    keep = (b - s + 1) * c
                    res = max(res, cur - full + keep) if False else None  # placeholder
                # adjust partials at the back: last added segment may extend beyond e
                # compute candidate
                cand = cur
                # subtract overflow at the back
                if j > 0 and coins[j - 1][1] > e:
                    a, b, c = coins[j - 1]
                    cand -= (b - e) * c
                # subtract underflow at the front
                if i < j and coins[i][0] < s:
                    a, b, c = coins[i]
                    cand -= (s - a) * c
                if cand > res:
                    res = cand
            return res

        # candidates: left = a_i, or left = b_i - k + 1
        starts = sorted({a for a, b, c in coins} | {max(0, b - k + 1) for a, b, c in coins})
        ans = max(ans, calc(starts))
        return ans
