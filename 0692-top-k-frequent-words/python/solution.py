from collections import Counter
from typing import List
import heapq

class Solution:
    def topKFrequent(self, words: List[str], k: int) -> List[str]:
        cnt = Counter(words)
        # neg count, then word ascending for tie-break
        h = [(-c, w) for w, c in cnt.items()]
        heapq.heapify(h)
        return [heapq.heappop(h)[1] for _ in range(k)]
