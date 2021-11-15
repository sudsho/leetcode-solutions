from collections import Counter
from typing import List

class Solution:
    def leastInterval(self, tasks: List[str], n: int) -> int:
        cnt = Counter(tasks)
        max_freq = max(cnt.values())
        ties = sum(1 for v in cnt.values() if v == max_freq)
        return max(len(tasks), (max_freq - 1) * (n + 1) + ties)
# typing fix
