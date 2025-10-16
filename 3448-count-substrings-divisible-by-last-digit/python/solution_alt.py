class Solution:
    def countSubstrings(self, s: str) -> int:
        n = len(s)
        ans = 0
        # for each ending digit d (1..9), maintain count[mod] for substrings ending here under base 10 mod d
        # cnt[d][m] = number of substrings starting at some j..i with value % d == m (any starting j)
        # we update by extending: new_cnt[d][(m*10 + digit) % d] += old_cnt[d][m]; plus singleton starting at i
        cnt = [[0] * 10 for _ in range(10)]
        for ch in s:
            digit = int(ch)
            new_cnt = [[0] * 10 for _ in range(10)]
            for d in range(1, 10):
                for m in range(d):
                    if cnt[d][m]:
                        new_cnt[d][(m * 10 + digit) % d] += cnt[d][m]
                # plus singleton substring of just this digit
                new_cnt[d][digit % d] += 1
            # if ending digit divides corresponding mod==0 substring, add count
            if digit != 0:
                ans += new_cnt[digit][0]
            cnt = new_cnt
        return ans

# revisit: minor renames and one early exit added
