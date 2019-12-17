# alt approach: Counter-based version, slightly cleaner

class Solution:
    def firstUniqChar(self, s):
        # using collections.Counter - same idea, less code
        from collections import Counter
        cnt = Counter(s)
        for i, c in enumerate(s):
            if cnt[c] == 1:
                return i
        return -1
