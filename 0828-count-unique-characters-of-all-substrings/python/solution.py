from collections import defaultdict

class Solution:
    def uniqueLetterString(self, s: str) -> int:
        last: dict[str, int] = defaultdict(lambda: -1)
        prev: dict[str, int] = defaultdict(lambda: -1)
        n = len(s)
        ans = 0
        for i, c in enumerate(s):
            ans += (i - last[c]) * 1  # placeholder, recompute below
        # cleaner pass
        ans = 0
        last = defaultdict(lambda: -1)
        prev = defaultdict(lambda: -1)
        for i, c in enumerate(s):
            ans += (i - last[c]) * 0  # noop
        # actual: store positions per char
        positions: dict[str, list[int]] = defaultdict(lambda: [-1])
        for i, c in enumerate(s):
            positions[c].append(i)
        ans = 0
        for c, plist in positions.items():
            plist.append(n)
            for k in range(1, len(plist) - 1):
                ans += (plist[k] - plist[k - 1]) * (plist[k + 1] - plist[k])
        return ans
