# split via parens recursion
class Solution:
    def calculate(self, s: str) -> int:
        s = s.replace(" ", "")
        self._i = 0

        def helper() -> int:
            total = 0
            sign = 1
            num = 0
            while self._i < len(s):
                ch = s[self._i]
                if ch.isdigit():
                    num = num * 10 + int(ch)
                elif ch == "(":
                    self._i += 1
                    num = helper()
                elif ch == ")":
                    return total + sign * num
                else:
                    total += sign * num
                    num = 0
                    sign = 1 if ch == "+" else -1
                self._i += 1
            return total + sign * num
        return helper()
