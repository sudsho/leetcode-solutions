class Solution:
    def smallestSubsequence(self, s: str, k: int, letter: str, repetition: int) -> str:
        # DP-driven greedy: precount suffix occurrences, then walk
        n = len(s)
        suf = [0] * (n + 1)
        for i in range(n - 1, -1, -1):
            suf[i] = suf[i + 1] + (1 if s[i] == letter else 0)
        stack: list[str] = []
        in_letter = 0
        for i, ch in enumerate(s):
            while stack and stack[-1] > ch:
                rem_after = n - i
                if len(stack) - 1 + rem_after < k:
                    break
                if stack[-1] == letter and (in_letter - 1) + suf[i] < repetition:
                    break
                if stack.pop() == letter:
                    in_letter -= 1
            if len(stack) < k:
                if ch == letter:
                    stack.append(ch)
                    in_letter += 1
                elif (k - len(stack) - 1) >= repetition - in_letter:
                    stack.append(ch)
        return ''.join(stack)
