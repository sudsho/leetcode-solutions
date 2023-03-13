class Solution:
    PAIRS = (('0','0'),('1','1'),('6','9'),('8','8'),('9','6'))
    def strobogrammaticInRange(self, low: str, high: str) -> int:
        return self._count(high) - self._count(str(int(low) - 1))

    def _count(self, num: str) -> int:
        if not num or int(num) < 0:
            return 0
        n = len(num)
        total = 0
        for L in range(1, n):
            total += self._gen_count(L, L)
        # for length n we must be <= num
        return total + self._le(num)

    def _gen_count(self, length: int, total: int) -> int:
        if length == 0:
            return 1
        if length == 1:
            return 3  # 0, 1, 8
        inner = self._gen_count(length - 2, total)
        if length == total:
            return inner * 4  # no leading 0
        return inner * 5

    def _le(self, num: str) -> int:
        # count strobogrammatic numbers of len(num) that are <= num
        # easiest: generate all and compare. lengths up to ~15 ok per LC constraints.
        n = len(num)
        out = 0
        def build(left: int, right: int, cur: list[str]) -> None:
            nonlocal out
            if left > right:
                s = ''.join(cur)
                if (n == 1 or s[0] != '0') and s <= num:
                    out += 1
                return
            for a, b in Solution.PAIRS:
                if left == right and a != b:
                    continue
                cur[left], cur[right] = a, b
                build(left + 1, right - 1, cur)
        build(0, n - 1, [' '] * n)
        return out
