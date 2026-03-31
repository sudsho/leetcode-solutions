# Valid Parentheses (#20) - Easy
# Given a string with '(', ')', '{', '}', '[', ']',
# determine if the input string is valid (brackets closed in correct order).

class Solution:
    def isValid(self, s: str) -> bool:
        stack = []
        mapping = {')': '(', '}': '{', ']': '['}

        for char in s:
            if char in mapping:
                top = stack.pop() if stack else '#'
                if mapping[char] != top:
                    return False
            else:
                stack.append(char)

        return not stack


if __name__ == "__main__":
    sol = Solution()
    print(sol.isValid("()[]{}"))   # True
    print(sol.isValid("(]"))       # False
    print(sol.isValid("([)]"))     # False
    print(sol.isValid("{[]}"))     # True

# Time:  O(n)
# Space: O(n)
