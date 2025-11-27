from typing import List
import heapq

class Solution:
    def maximumScore(self, nums: List[int], k: int) -> int:
        MOD = 10 ** 9 + 7
        n = len(nums)
        score = [0] * n
        for i, v in enumerate(nums):
            x = v
            d = 2
            distinct = 0
            while d * d <= x:
                if x % d == 0:
                    distinct += 1
                    while x % d == 0:
                        x //= d
                d += 1
            if x > 1:
                distinct += 1
            score[i] = distinct
        # windows where score[i] is max: monotonic stack
        left = [-1] * n
        right = [n] * n
        stack: list[int] = []
        for i in range(n):
            while stack and score[stack[-1]] < score[i]:
                stack.pop()
            left[i] = stack[-1] if stack else -1
            stack.append(i)
        stack = []
        for i in range(n - 1, -1, -1):
            while stack and score[stack[-1]] <= score[i]:
                stack.pop()
            right[i] = stack[-1] if stack else n
            stack.append(i)
        order = sorted(range(n), key=lambda i: -nums[i])
        ans = 1
        ops = k
        def power(a: int, e: int) -> int:
            r = 1
            a %= MOD
            while e:
                if e & 1:
                    r = r * a % MOD
                a = a * a % MOD
                e >>= 1
            return r
        for i in order:
            cnt = (i - left[i]) * (right[i] - i)
            use = min(cnt, ops)
            ans = ans * power(nums[i], use) % MOD
            ops -= use
            if ops == 0:
                break
        return ans

# revisit: minor renames and one early exit added
