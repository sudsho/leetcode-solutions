class Solution:
    def smallestSubsequence(self, s: str, k: int, letter: str, repetition: int) -> str:
        remain_letter = s.count(letter)
        n = len(s)
        stack: list[str] = []
        in_letter = 0
        for i, ch in enumerate(s):
            while stack and stack[-1] > ch and len(stack) - 1 + (n - i) >= k:
                if stack[-1] == letter and in_letter + remain_letter <= repetition:
                    break
                top = stack.pop()
                if top == letter:
                    in_letter -= 1
            if len(stack) < k:
                if ch == letter:
                    stack.append(ch)
                    in_letter += 1
                elif k - len(stack) > repetition - in_letter:
                    stack.append(ch)
            if ch == letter:
                remain_letter -= 1
        return "".join(stack)
# refactored helper
# tightened naming
