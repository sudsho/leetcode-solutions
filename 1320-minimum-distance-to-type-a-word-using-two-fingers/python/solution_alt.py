# simple iterative dp on (f1, f2) pairs - same complexity, less recursion
class Solution:
    def minimumDistance(self, word: str) -> int:
        def coord(c: str) -> tuple:
            i = ord(c) - ord("A")
            return divmod(i, 6)

        def cost(a: int, b: int) -> int:
            r1, c1 = coord(chr(a + ord("A")))
            r2, c2 = coord(chr(b + ord("A")))
            return abs(r1 - r2) + abs(c1 - c2)

        N = len(word)
        if N <= 1:
            return 0
        # dp[other] = best total ending with word[i] on first finger and other on second
        INF = 10 ** 9
        dp = [0] * 26
        # use the trick: cost on the same finger transition is fixed; tabulate adjustment
        first = ord(word[0]) - ord("A")
        for i in range(N - 1):
            a = ord(word[i]) - ord("A")
            b = ord(word[i + 1]) - ord("A")
            move = cost(a, b)
            new_dp = [INF] * 26
            for other in range(26):
                # case 1: continue with finger that just moved a -> b
                v = dp[other] + move
                if v < new_dp[other]:
                    new_dp[other] = v
                # case 2: move other finger to b, leave a stationary
                hop = cost(other, b)
                v = dp[other] + hop
                if v < new_dp[a]:
                    new_dp[a] = v
            dp = new_dp
        return min(dp)
