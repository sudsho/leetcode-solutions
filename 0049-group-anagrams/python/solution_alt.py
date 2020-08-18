from collections import defaultdict

class Solution:
    def groupAnagrams(self, strs):
        # count-tuple key avoids sort, O(n*k)
        groups = defaultdict(list)
        for s in strs:
            cnt = [0] * 26
            for ch in s:
                cnt[ord(ch) - ord("a")] += 1
            groups[tuple(cnt)].append(s)
        return list(groups.values())
