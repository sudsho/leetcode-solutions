from typing import List

class Solution:
    def assignElements(self, groups: List[int], elements: List[int]) -> List[int]:
        max_v = max(groups)
        first = {}
        for i, e in enumerate(elements):
            if e == 0 or e > max_v:
                continue
            for m in range(e, max_v + 1, e):
                first.setdefault(m, i)
        return [first.get(g, -1) for g in groups]
