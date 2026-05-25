class Solution:
    INT_MIN = -(2 ** 31)
    INT_MAX = 2 ** 31 - 1

    def myAtoi(self, s):
        n = len(s)
        i = 0
        while i < n and s[i] == " ":
            i += 1

        sign = 1
        if i < n and (s[i] == "+" or s[i] == "-"):
            if s[i] == "-":
                sign = -1
            i += 1

        result = 0
        while i < n and s[i].isdigit():
            result = result * 10 + (ord(s[i]) - ord("0"))
            i += 1
            if sign * result <= self.INT_MIN:
                return self.INT_MIN
            if sign * result >= self.INT_MAX:
                return self.INT_MAX

        return sign * result
