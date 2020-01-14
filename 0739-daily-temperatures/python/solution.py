class Solution:
    def dailyTemperatures(self, temperatures):
        n = len(temperatures)
        ans = [0] * n
        stack = []
        for i, t in enumerate(temperatures):
            while stack and temperatures[stack[-1]] < t:
                j = stack.pop()
                ans[j] = i - j
            stack.append(i)
        return ans
