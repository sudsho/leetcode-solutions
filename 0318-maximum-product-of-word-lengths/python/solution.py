class Solution:
    def maxProduct(self, words):
        """Max product of lengths of two words that share no common letter.

        The words only contain lowercase letters, so the *set* of letters in a
        word fits in a 26-bit integer: bit k is set iff letter chr(ord('a')+k)
        appears. Two words are disjoint exactly when their bitmasks AND to zero,
        which turns the "do they share a letter" test into a single machine
        instruction instead of a set intersection.

        Precompute one mask per word (O(total characters)), then check every pair
        (O(n^2) cheap bit ANDs) and track the best product of lengths. Building the
        masks once up front is what keeps the pairwise loop from re-scanning
        characters, so the dominant cost is the n^2 pass, not the string work.
        """
        masks = [0] * len(words)
        for i, w in enumerate(words):
            m = 0
            for ch in w:
                m |= 1 << (ord(ch) - ord("a"))
            masks[i] = m

        best = 0
        for i in range(len(words)):
            for j in range(i + 1, len(words)):
                if masks[i] & masks[j] == 0:
                    best = max(best, len(words[i]) * len(words[j]))
        return best


if __name__ == "__main__":
    s = Solution()
    assert s.maxProduct(["abcw", "baz", "foo", "bar", "xtfn", "abcdef"]) == 16
    assert s.maxProduct(["a", "ab", "abc", "d", "cd", "bcd", "abcd"]) == 4
    assert s.maxProduct(["a", "aa", "aaa", "aaaa"]) == 0
    print("all good")
