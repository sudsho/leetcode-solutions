"""LeetCode 168 - Excel Sheet Column Title."""


class Solution:
    def convertToTitle(self, columnNumber: int) -> str:
        out = []
        n = columnNumber
        while n > 0:
            n -= 1
            out.append(chr(ord("A") + n % 26))
            n //= 26
        return "".join(reversed(out))


if __name__ == "__main__":
    s = Solution()
    cases = [(1, "A"), (26, "Z"), (27, "AA"), (28, "AB"), (52, "AZ"),
             (53, "BA"), (701, "ZY"), (702, "ZZ"), (703, "AAA")]
    for n, want in cases:
        got = s.convertToTitle(n)
        assert got == want, f"{n} -> {got}, want {want}"
    print("ok")
