from typing import List

class Solution:
    def countKConstraintSubstrings(self, s: str, k: int, queries: List[List[int]]) -> List[int]:
        n = len(s)
        # for each i, smallest L[i] such that s[L[i]..i] has >= k zeros and >= k ones impossible? misread.
        # Real problem: substrings where number of 0s <= k or number of 1s <= k.
        # left[r] = smallest l such that s[l..r] is valid
        zeros = ones = 0
        L = [0] * n
        l = 0
        for r in range(n):
            if s[r] == '0':
                zeros += 1
            else:
                ones += 1
            while zeros > k and ones > k:
                if s[l] == '0':
                    zeros -= 1
                else:
                    ones -= 1
                l += 1
            L[r] = l
        # for each r, count of valid substrings ending at r is r - L[r] + 1
        # prefix sum over r
        pref = [0] * (n + 1)
        for i in range(n):
            pref[i + 1] = pref[i] + (i - L[i] + 1)
        ans: list[int] = []
        for ql, qr in queries:
            # find smallest r in [ql, qr] where L[r] >= ql
            lo, hi = ql, qr + 1
            while lo < hi:
                mid = (lo + hi) // 2
                if L[mid] >= ql:
                    hi = mid
                else:
                    lo = mid + 1
            split = lo
            # range [ql, split-1]: arithmetic sum 1..(split-ql)
            n1 = split - ql
            part1 = n1 * (n1 + 1) // 2
            part2 = pref[qr + 1] - pref[split]
            ans.append(part1 + part2)
        return ans

# revisit: minor renames and one early exit added
