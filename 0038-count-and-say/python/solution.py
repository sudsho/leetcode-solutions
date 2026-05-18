class Solution:
    def countAndSay(self, n):
        # base case: the first term is just "1"
        s = "1"
        for _ in range(n - 1):
            s = self._next(s)
        return s

    def _next(self, s):
        # run length encode s: group consecutive equal chars, then write count + char
        out = []
        i = 0
        while i < len(s):
            j = i
            while j < len(s) and s[j] == s[i]:
                j += 1
            out.append(str(j - i))
            out.append(s[i])
            i = j
        return "".join(out)


if __name__ == "__main__":
    sol = Solution()
    for k in range(1, 7):
        print(k, sol.countAndSay(k))
