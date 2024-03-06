from typing import List

class Solution:
    def maxJumps(self, arr: List[int], d: int) -> int:
        # Bottom-up by sorted heights
        n = len(arr)
        order = sorted(range(n), key=lambda i: arr[i])
        dp = [1] * n
        for i in order:
            for j in range(i + 1, min(n, i + d + 1)):
                if arr[j] >= arr[i]:
                    break
                if dp[j] + 1 > dp[i]:
                    dp[i] = dp[j] + 1
            for j in range(i - 1, max(-1, i - d - 1), -1):
                if arr[j] >= arr[i]:
                    break
                if dp[j] + 1 > dp[i]:
                    dp[i] = dp[j] + 1
        return max(dp)
