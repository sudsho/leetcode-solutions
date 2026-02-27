# alt: use itertools.permutations for sanity check on small n
from itertools import permutations
from typing import List


class Solution:
    def permute(self, n: int, k: int) -> List[int]:
        # exhaustive: only viable for n up to about 10
        target = k
        for p in permutations(range(1, n + 1)):
            ok = True
            for a, b in zip(p, p[1:]):
                if (a % 2) == (b % 2):
                    ok = False
                    break
            if ok:
                target -= 1
                if target == 0:
                    return list(p)
        return []
