from typing import List
from collections import Counter

class Solution:
    def minStickers(self, stickers: List[str], target: str) -> int:
        n = len(target)
        full = (1 << n) - 1
        # for each sticker, the masks reachable from each state
        sticker_chars = [Counter(s) for s in stickers]
        from functools import lru_cache
        @lru_cache(maxsize=None)
        def dp(state: int) -> int:
            if state == full:
                return 0
            best = 1 << 30
            # find first missing letter
            for j in range(n):
                if not (state >> j) & 1:
                    first = j
                    break
            for s in sticker_chars:
                if target[first] in s:
                    new_state = state
                    used = Counter()
                    for j in range(n):
                        if not (new_state >> j) & 1 and target[j] in s and used[target[j]] < s[target[j]]:
                            used[target[j]] += 1
                            new_state |= (1 << j)
                    if new_state != state:
                        nxt = dp(new_state)
                        if nxt < best:
                            best = nxt
            return best + 1 if best < (1 << 30) else best
        ans = dp(0)
        return -1 if ans >= (1 << 30) else ans
