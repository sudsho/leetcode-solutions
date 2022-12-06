# dp version: dp[i] = farthest distance with exactly i stops
from typing import List

class Solution:
    def minRefuelStops(self, target: int, startFuel: int, stations: List[List[int]]) -> int:
        n = len(stations)
        dp = [0] * (n + 1)
        dp[0] = startFuel
        for i in range(n):
            for j in range(i, -1, -1):
                if dp[j] >= stations[i][0]:
                    dp[j + 1] = max(dp[j + 1], dp[j] + stations[i][1])
        for i, d in enumerate(dp):
            if d >= target:
                return i
        return -1
