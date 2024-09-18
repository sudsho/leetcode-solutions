from typing import List

class Solution:
    def tallestBillboard(self, rods: List[int]) -> int:
        # dp[diff] = max smaller side height with this absolute diff
        dp: dict[int, int] = {0: 0}
        for r in rods:
            new = dict(dp)
            for d, lo in dp.items():
                # add to taller
                new[d + r] = max(new.get(d + r, 0), lo)
                # add to shorter
                nd = abs(d - r)
                nl = lo + min(d, r)
                new[nd] = max(new.get(nd, 0), nl)
            dp = new
        return dp.get(0, 0)
