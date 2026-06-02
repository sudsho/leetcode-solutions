class Solution:
    def multiply(self, num1, num2):
        if num1 == "0" or num2 == "0":
            return "0"

        n, m = len(num1), len(num2)
        res = [0] * (n + m)

        for i in range(n - 1, -1, -1):
            a = ord(num1[i]) - 48
            for j in range(m - 1, -1, -1):
                b = ord(num2[j]) - 48
                total = a * b + res[i + j + 1]
                res[i + j + 1] = total % 10
                res[i + j] += total // 10

        k = 0
        while k < len(res) - 1 and res[k] == 0:
            k += 1
        return "".join(str(d) for d in res[k:])
