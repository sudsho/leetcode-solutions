# Problem: Climbing Stairs (LeetCode #70)
# You are climbing a staircase with n steps. Each time you can climb 1 or 2 steps.
# Return the number of distinct ways to reach the top.

class Solution:
    def climbStairs(self, n: int) -> int:
        if n <= 2:
            return n

        prev2, prev1 = 1, 2
        for _ in range(3, n + 1):
            curr = prev1 + prev2
            prev2 = prev1
            prev1 = curr

        return prev1

# Time Complexity: O(n) - single pass through n steps
# Space Complexity: O(1) - only two variables maintained

if __name__ == "__main__":
    sol = Solution()
    print(sol.climbStairs(2))   # 2 (1+1, 2)
    print(sol.climbStairs(3))   # 3 (1+1+1, 1+2, 2+1)
    print(sol.climbStairs(10))  # 89
