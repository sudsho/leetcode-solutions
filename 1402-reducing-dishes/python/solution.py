from typing import List

class Solution:
    def maxSatisfaction(self, satisfaction: List[int]) -> int:
        satisfaction.sort(reverse=True)
        total = run = 0
        for x in satisfaction:
            run += x
            if run <= 0:
                break
            total += run
        return total
