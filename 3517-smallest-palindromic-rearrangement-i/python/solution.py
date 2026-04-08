from collections import Counter


class Solution:
    def smallestPalindrome(self, s: str) -> str:
        cnt = Counter(s)
        half = []
        mid = ""
        for ch in sorted(cnt):
            if cnt[ch] % 2:
                if mid:
                    return ""
                mid = ch
            half.append(ch * (cnt[ch] // 2))
        left = "".join(half)
        return left + mid + left[::-1]
