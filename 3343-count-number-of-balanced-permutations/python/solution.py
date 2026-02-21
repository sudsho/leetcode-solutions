from math import factorial
from typing import List


class Solution:
    def countBalancedPermutations(self, num: str) -> int:
        MOD = 10**9 + 7
        cnt = [0] * 10
        for c in num:
            cnt[int(c)] += 1
        n = len(num)
        total = sum(int(c) for c in num)
        if total % 2:
            return 0
        half = total // 2
        e = (n + 1) // 2  # slots at even index 0,2,...
        o = n // 2
        # dp[s][k] = number of ways to fill even-idx slots with chosen digits totaling s using k slots
        # multiplicities: for each digit d we pick j of cnt[d] for even, rest for odd
        # contribution multiplied by C(e_chosen)... done by accumulating with multinomial
        # Standard DP: dp[i][s][k] where i is digit, s sum so far in even bucket, k count so far in even bucket
        dp: List[List[int]] = [[0] * (e + 1) for _ in range(half + 1)]
        dp[0][0] = 1
        from math import comb
        for d in range(10):
            c = cnt[d]
            if c == 0:
                continue
            new = [[0] * (e + 1) for _ in range(half + 1)]
            for s in range(half + 1):
                for k in range(e + 1):
                    if dp[s][k] == 0:
                        continue
                    base = dp[s][k]
                    for j in range(0, c + 1):
                        ns = s + d * j
                        nk = k + j
                        if ns > half or nk > e:
                            break
                        ways = base * comb(c, j) % MOD
                        new[ns][nk] = (new[ns][nk] + ways) % MOD
            dp = new
        # arrange chosen even-bucket counts among e slots, odd among o slots
        # but dp already counts the unordered multiset choice with multinomial coefficient
        # we still need to multiply by e! and o! divided by product of cnt_d_in_bucket!
        # easier: track full multinomial directly
        # Above counted ways to split each digit into (j, c-j) with C(c, j). To turn that into orderings:
        # multiply by e! * o! and divide by product of digit-bucket factorials.
        # Equivalent: multiply by e! * o! / prod(cnt[d]!) and we already chose splits.
        # The split-counts encoded picks but not orderings, and original per-digit factorial overcounts.
        # Final: dp[half][e] * e! * o! mod MOD.
        # However the per-digit C(c, j) already represents the ratio c!/(j!(c-j)!), so the closed form is
        # answer = (e! * o!) / prod(j_d! * (c_d - j_d)!) summed weighted by ways.
        # Multiplying our dp by e! * o! gives:
        #   sum over splits of (prod C(c_d, j_d)) * e! * o!
        # which equals sum of (e! / prod j_d!) * (o! / prod (c_d - j_d)!) ... that is exactly the count.
        ans = dp[half][e] * factorial(e) % MOD * factorial(o) % MOD
        # divide by prod c_d!  -> not needed because C absorbed it
        return ans
