from typing import List

class Solution:
    def findMinDifference(self, timePoints: List[str]) -> int:
        m = sorted(int(t[:2]) * 60 + int(t[3:]) for t in timePoints)
        m.append(m[0] + 24 * 60)
        return min(m[i + 1] - m[i] for i in range(len(m) - 1))
