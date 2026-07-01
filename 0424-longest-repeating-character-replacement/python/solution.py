class Solution:
    def characterReplacement(self, s, k):
        """Longest substring of one repeated char after replacing <= k others.

        Slide a window and track the count of each letter inside it. A window is
        valid when (window_size - most_frequent_count) <= k, i.e. everything that
        is not the dominant letter can be turned into it within the budget k.

        The trick: we never need to shrink the window aggressively. Once we have
        seen a window of some length, a shorter answer is useless, so we only ever
        slide the left edge by one when the window turns invalid. max_freq is not
        decremented on shrink - it can only be stale-high, which just means we
        stop growing, and that is exactly the behaviour we want.
        """
        count = {}
        left = 0
        max_freq = 0
        best = 0
        for right, ch in enumerate(s):
            count[ch] = count.get(ch, 0) + 1
            max_freq = max(max_freq, count[ch])
            # replacements needed to make the whole window one letter
            if (right - left + 1) - max_freq > k:
                count[s[left]] -= 1
                left += 1
            best = max(best, right - left + 1)
        return best
